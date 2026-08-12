import streamlit as st

from main import setup
from components.overview import show_overview
from components.charts import (
    show_monthly_trend,
    show_category_chart,
    show_yearly_trend
)
from components.insights import show_advisor_dashboard, show_smart_insights

st.set_page_config(
    page_title="Finance AI Advisor",
    layout="wide"
)

db, all_data = setup()
all_data = all_data.copy()

all_data["year"] = all_data["date"].dt.year
all_data["month"] = all_data["date"].dt.month
all_data["day"] = all_data["date"].dt.day

all_data = all_data.sort_values("date")

total_spend = all_data["price"].sum()
months_covered = all_data["date"].dt.to_period("M").nunique()
avg_monthly = total_spend / months_covered if months_covered else 0
years_covered = len(sorted(all_data["year"].unique()))

st.title("💼 Finance AI Advisor Dashboard")
st.markdown(
    "Welcome to your financial advisor dashboard — track 3 years of expenses, review category trends, and get smart recommendations in one place."
)

# ---------------------------
# KPI CARDS
# ---------------------------
metrics = st.columns(5)
metrics[0].metric("Total Records", len(all_data))
metrics[1].metric("Total Spend", f"₹{total_spend:,.0f}")
metrics[2].metric("Years Covered", years_covered)
metrics[3].metric("Avg Monthly", f"₹{round(avg_monthly, 0):,}")
metrics[4].metric("Months Covered", months_covered)

st.markdown("---")

# ---------------------------
# Advisor and overview panels
# ---------------------------
show_advisor_dashboard(all_data)

st.markdown("---")

# ---------------------------
# Trend charts
# ---------------------------
trend_left, trend_right = st.columns(2)
with trend_left:
    show_yearly_trend(all_data)
with trend_right:
    show_monthly_trend(all_data)

st.markdown("---")

# ---------------------------
# Category and insights
# ---------------------------
chart_col, insight_col = st.columns([3, 2])
with chart_col:
    category = show_category_chart(all_data)
with insight_col:
    show_smart_insights(all_data, category)

st.markdown("---")

st.info("Use the left sidebar to jump between Overview, Category Analysis, and AI Assistant pages.")