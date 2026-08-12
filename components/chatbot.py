import streamlit as st
from agents.finance_agent import run_finance_agent



def show_chatbot(db, all_data):

    st.subheader("🤖 Finance AI Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    query = st.chat_input("Ask about your expenses...")

    st.markdown(
        "**Try questions like:**\n"
        "- How much did I spend in June 2026?\n"
        "- Which categories cost me the most?\n"
        "- Forecast my spending for the next 6 months.\n"
        "- How can I save more this month?"
    )

    if query:

        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("user"):
            st.write(query)

        history = "\n".join([
            f"{m['role']}: {m['content']}"
            for m in st.session_state.messages[-5:]
        ])

        with st.chat_message("assistant"):
            with st.spinner("Analyzing financial behavior..."):

                answer = run_finance_agent(
                    query,
                    all_data,
                    db,
                    history
                )

                st.write(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })