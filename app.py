import streamlit as st

from main import setup

st.set_page_config(
    page_title="Finance AI",
    layout="wide"
)

db, all_data = setup()
all_data = all_data.copy()

all_data["year"] = all_data["date"].dt.year
all_data["month"] = all_data["date"].dt.month
all_data["day"] = all_data["date"].dt.day

st.title("💰 Personal Finance AI")

st.subheader("Home")
st.write("This is the main Streamlit entry page. Use the sidebar to open the analysis pages.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total records", len(all_data))

with col2:
    st.metric("Total spend", f"₹{all_data['price'].sum():,.0f}")

with col3:
    st.metric(
        "Date range",
        f"{all_data['date'].min().date()} to {all_data['date'].max().date()}"
    )

st.info(
    "Pages available in the sidebar: Overview, Category Analysis, and AI Assistant."
)

st.caption("The shared data setup is loaded from main.py, so all pages use the same curated dataset and vector DB.")