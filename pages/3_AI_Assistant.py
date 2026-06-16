import streamlit as st

from main import setup

from components.chatbot import show_chatbot

db, all_data = setup()
all_data = all_data.copy()

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