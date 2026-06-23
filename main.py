"""Shared finance setup used by the Streamlit pages and optional CLI usage."""

import streamlit as st
from functools import lru_cache
import os

from ai_service import generate_answer_with_memory
from data_curation import refresh_finance
from data_loader import load_data
from embedder import create_embeddings
from rag_engine import VectorDB
from utils.embedding_cache import load_embeddings_cache, save_embeddings_cache


CURATED_FILE_PATH = r"G:\My Drive\Finanace\finance_curated.csv"


@st.cache_resource
def setup(data_file=CURATED_FILE_PATH):
    """Setup finance data with Streamlit caching for persistence."""
    try:
        with st.spinner("📊 Loading financial data..."):
            refresh_finance()

        with st.spinner("📄 Processing documents..."):
            documents, all_data = load_data(data_file)

        with st.spinner("🤖 Creating AI embeddings (this may take a minute)..."):
            # Try to load cached embeddings first
            embeddings = load_embeddings_cache(data_file)
            
            if embeddings is None:
                # No cache, create new embeddings
                embeddings = create_embeddings(documents)
                # Save to cache for next time
                save_embeddings_cache(embeddings, data_file)
            else:
                st.info("⚡ Using cached embeddings - much faster!")

        with st.spinner("🔍 Building search index..."):
            db = VectorDB(embeddings, documents)

        st.success("✅ Data loaded successfully!")
        return db, all_data
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        raise


# Alternative setup for CLI (non-Streamlit)
@lru_cache(maxsize=1)
def setup_cli(data_file=CURATED_FILE_PATH):
    """Setup for CLI usage (doesn't use Streamlit)."""
    refresh_finance()
    documents, all_data = load_data(data_file)
    
    # Try cache for CLI too
    embeddings = load_embeddings_cache(data_file)
    if embeddings is None:
        embeddings = create_embeddings(documents)
        save_embeddings_cache(embeddings, data_file)
    
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
    run_cli()
