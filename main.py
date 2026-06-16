"""Shared finance setup used by the Streamlit pages and optional CLI usage."""

from functools import lru_cache

from ai_service import generate_answer_with_memory
from data_curation import refresh_finance
from data_loader import load_data
from embedder import create_embeddings
from rag_engine import VectorDB


CURATED_FILE_PATH = r"G:\My Drive\Finanace\finance_curated.csv"


@lru_cache(maxsize=1)
def setup(data_file=CURATED_FILE_PATH):
    refresh_finance()

    documents, all_data = load_data(data_file)

    embeddings = create_embeddings(documents)

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
