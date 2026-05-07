import streamlit as st

from data_loader import load_data
from embedder import create_embeddings
from rag_engine import VectorDB

from components.chatbot import show_chatbot

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_resource
def setup():

    documents, all_data = load_data("expense.xlsx")

    embeddings = create_embeddings(documents)

    db = VectorDB(
        embeddings,
        documents
    )

    return db, all_data


db, all_data = setup()

# ---------------------------
# PAGE TITLE
# ---------------------------
st.title("🤖 AI Financial Assistant")

st.info("""
Ask questions like:
- Where do I spend the most?
- How much did I spend on food?
- Which month was expensive?
- How can I save money?
""")

# ---------------------------
# CHATBOT
# ---------------------------
show_chatbot(db, all_data)