import streamlit as st

from data_loader import load_data
from components.filters import apply_filters
from components.charts import show_category_chart
from components.category_drilldown import show_category_drilldown

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_resource
def setup():

    documents, all_data = load_data("expense.xlsx")

    return all_data


all_data = setup()

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
# TITLE
# ---------------------------
st.title("📂 Category Analysis")

# ---------------------------
# CHARTS
# ---------------------------
category = show_category_chart(filtered_data)

# ---------------------------
# DRILLDOWN
# ---------------------------
show_category_drilldown(
    filtered_data,
    category
)