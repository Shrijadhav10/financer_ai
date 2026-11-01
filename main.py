"""Shared finance setup used by the Streamlit pages and optional CLI usage."""

import streamlit as st
from functools import lru_cache
from pathlib import Path
import tempfile

from ai_service import generate_answer_with_memory
from data_curation import refresh_finance
from data_loader import load_data
from embedder import create_embeddings
from rag_engine import VectorDB
from utils.embedding_cache import load_embeddings_cache, save_embeddings_cache
from utils.deployment import get_secret_section
from utils.google_drive import download_drive_file


CURATED_FILE_PATH = r"G:\My Drive\Finanace\finance_curated.csv"


def _file_state(data_file):
    """A cheap fingerprint of the data file's current size+mtime.

    Passed into setup() below so that st.cache_resource's cache key
    changes whenever the underlying file changes. Without this,
    @st.cache_resource caches (db, all_data) for the life of the running
    Streamlit process and setup() body never re-runs again, no matter
    how stale the embedding cache itself becomes.
    """
    try:
        stat = Path(data_file).resolve().stat()
        return f"{stat.st_size}_{stat.st_mtime_ns}"
    except FileNotFoundError:
        return "missing"


@st.cache_resource
def _setup_cached(
    data_file=CURATED_FILE_PATH,
    file_state_signal=None,
    drive_file_id=None,
    _service_account_info=None,
):
    """Setup finance data with Streamlit caching for persistence.

    file_state_signal is not used inside the function body — its only
    job is to be part of the cache key, so that st.cache_resource treats
    a changed file as a fresh call rather than returning the old cached
    (db, all_data) forever. Call setup() below, not this function
    directly, so the signal gets filled in automatically.
    """
    try:
        with st.spinner("📊 Loading financial data..."):
            if drive_file_id:
                if not _service_account_info:
                    raise RuntimeError(
                        "Google Drive service-account credentials are missing. "
                        "Configure them in Streamlit secrets."
                    )

                data_path = Path(data_file)
                source_path = data_path.with_name("expense.xlsx")
                download_drive_file(
                    drive_file_id,
                    _service_account_info,
                    source_path,
                )
                refresh_finance(
                    input_file=str(source_path),
                    output_file=str(data_path),
                )
            else:
                refresh_finance()

        with st.spinner("📄 Processing documents..."):
            documents, all_data = load_data(data_file)

        with st.spinner("🤖 Creating AI embeddings (this may take a minute)..."):
            # Try to load cached embeddings first. The cache key now reflects
            # the data file's size+mtime, so if finance_curated.csv changed
            # since the cache was written, this automatically misses and
            # falls through to regenerating fresh embeddings below.
            embeddings, cached_documents = load_embeddings_cache(data_file)

            if embeddings is None:
                # No cache (or stale cache for this file version): create new
                embeddings = create_embeddings(documents)
                # Save embeddings together WITH the documents they came from,
                # so a future load can never pair them with mismatched text.
                save_embeddings_cache(embeddings, documents, data_file)
            else:
                # Use the documents that were cached alongside these
                # embeddings, not the freshly-loaded `documents` list, to
                # guarantee embeddings[i] <-> documents[i] stay paired.
                documents = cached_documents
                st.info("⚡ Using cached embeddings - much faster!")

        with st.spinner("🔍 Building search index..."):
            db = VectorDB(embeddings, documents)

        st.success("✅ Data loaded successfully!")
        return db, all_data
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        raise


def setup(data_file=CURATED_FILE_PATH):
    """Public entry point — same call signature as before (no args needed).

    Computes the data file's current size+mtime and passes it through to
    _setup_cached so Streamlit's cache_resource correctly detects when the
    underlying file has changed and reruns setup instead of returning a
    stale (db, all_data) from earlier in the app's lifetime.
    """
    drive_settings = get_secret_section("google_drive")
    if drive_settings is not None:
        drive_file_id = drive_settings.get("file_id")
        service_account_info = drive_settings.get("service_account")
        if not drive_file_id or not service_account_info:
            raise RuntimeError(
                "Configure google_drive.file_id and "
                "google_drive.service_account in Streamlit secrets."
            )

        data_path = (
            Path(tempfile.gettempdir())
            / "financer_ai"
            / "finance_curated.csv"
        )
        cache_signal = f"drive:{drive_file_id}"
        return _setup_cached(
            str(data_path),
            cache_signal,
            drive_file_id=drive_file_id,
            _service_account_info=dict(service_account_info),
        )

    if not Path(r"G:\My Drive\Finanace\expense.xlsx").exists():
        raise RuntimeError(
            "Google Drive secrets are required when the local G: drive "
            "source file is unavailable."
        )

    return _setup_cached(
        data_file,
        file_state_signal=_file_state(data_file),
    )


# Alternative setup for CLI (non-Streamlit)
@lru_cache(maxsize=1)
def setup_cli(data_file=CURATED_FILE_PATH):
    """Setup for CLI usage (doesn't use Streamlit)."""
    refresh_finance()
    documents, all_data = load_data(data_file)
    
    # Try cache for CLI too
    embeddings, cached_documents = load_embeddings_cache(data_file)
    if embeddings is None:
        embeddings = create_embeddings(documents)
        save_embeddings_cache(embeddings, documents, data_file)
    else:
        documents = cached_documents
    
    db = VectorDB(embeddings, documents)
    return db, all_data


def run_cli():
    db, all_data = setup()

    while True:
        query = input("👉 Ask: ")

        if query.strip().lower() in {"exit", "quit"}:
            break

        answer = generate_answer_with_memory(query, db, all_data)
        print("\n💡 Answer:\n", answer)


if __name__ == "__main__":
    # `streamlit run main.py` is the primary application entry point.
    # The CLI remains available via: python main.py --cli
    import sys

    if "--cli" in sys.argv:
        run_cli()
    else:
        from financer_dashboard import main as run_dashboard
        run_dashboard()
