import streamlit as st


def show_overview(all_data, filtered_data):

    st.subheader("📊 Overall Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Records",
        len(all_data)
    )

    col2.metric(
        "Total Spend",
        f"₹{round(all_data['price'].sum(), 2)}"
    )

    col3.metric(
        "Date Range",
        f"{all_data['date'].min().strftime('%b %Y')} → {all_data['date'].max().strftime('%b %Y')}"
    )

    st.subheader("📊 Filtered Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Records",
        len(filtered_data)
    )

    col2.metric(
        "Spend",
        f"₹{round(filtered_data['price'].sum(), 2)}"
    )

    col3.metric(
        "Date Range",
        f"{filtered_data['date'].min().strftime('%b %Y')} → {filtered_data['date'].max().strftime('%b %Y')}"
    )