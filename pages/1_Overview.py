import streamlit as st

from data_loader import load_data
from embedder import create_embeddings
from rag_engine import VectorDB

from components.filters import apply_filters
from components.overview import show_overview
from components.charts import (
    show_monthly_trend,
    show_category_chart
)
from components.insights import show_smart_insights

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
# DATE PARTS
# ---------------------------
all_data['year'] = all_data['date'].dt.year
all_data['month'] = all_data['date'].dt.month
all_data['day'] = all_data['date'].dt.day

# ---------------------------
# FILTERS
# ---------------------------
filtered_data = apply_filters(all_data)

# ---------------------------
# PAGE TITLE
# ---------------------------
st.title("📊 Overview")

# ---------------------------
# OVERVIEW
# ---------------------------
show_overview(all_data, filtered_data)

# ---------------------------
# CHARTS
# ---------------------------
category = show_category_chart(filtered_data)

show_monthly_trend(filtered_data)

# ---------------------------
# INSIGHTS
# ---------------------------
show_smart_insights(filtered_data, category)