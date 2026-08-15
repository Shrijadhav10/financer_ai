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
- How much did I spend on athithi?
- Which month was expensive?
- How can I save money?

💡 **Pro Tip:** Add "use llm" or "use ai" to any question to get AI-powered insights!
- Example: "Use llm - analyze my spending patterns"
- Example: "Use ai - give insights on my food spending"
""")

# ---------------------------
# CHATBOT
# ---------------------------
show_chatbot(db, all_data)