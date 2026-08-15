"""A polished Streamlit dashboard for the curated finance data.

Run with: streamlit run financer_dashboard.py
Set FINANCE_DATA_FILE to use a different CSV/XLSX source.
"""

import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from data_loader import load_data


DEFAULT_DATA_FILE = r"G:\My Drive\Finanace\finance_curated.csv"
COLORS = ["#635BFF", "#14B8A6", "#F59E0B", "#EC4899", "#3B82F6", "#8B5CF6", "#22C55E"]

# Only reliable rules are included here. Names that cannot be reliably inferred
# remain in "Needs review" rather than being assigned a misleading category.
EXACT_CATEGORY_FIXES = {
    "splitwise": "shared expenses", "deposit": "housing", "buds": "shopping",
    "trends": "shopping", "flipkart": "shopping", "myntra": "shopping",
    "zudio": "shopping", "cutting": "food", "khana": "food",
    "mcdonald's": "food", "7/12 hotel": "food", "cylinder": "utilities",
    "tv repair": "home maintenance", "washing machine repair": "home maintenance",
    "wallputti": "home maintenance", "pesticide": "home maintenance",
    "wet & joy": "leisure", "movie": "leisure", "go karting": "leisure",
    "marathon": "fitness", "run": "fitness", "gift": "gifts & events",
    "marriage": "gifts & events", "fair": "gifts & events", "festival": "gifts & events",
    "insurance": "financial fees", "anna pancard": "financial fees",
    "debit card charge": "financial fees", "debit card fee": "financial fees",
    "annual maintaince": "financial fees", "ticket": "transport",
    "car wash": "transport", "return to pune": "transport", "pune": "transport",
}


def apply_theme():
    st.markdown("""<style>
    .stApp { background: #f6f7fb; color: #172033; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg,#121b35,#263961); }
    [data-testid="stSidebar"] * { color: #f8fafc; }
    [data-testid="stSidebar"] div[data-baseweb="select"] * { color: #172033; }
    .hero { padding: 1.7rem 2rem; border-radius: 22px; color: white;
      background: linear-gradient(115deg,#4f46e5,#7c3aed 58%,#0f766e); box-shadow: 0 16px 36px #4f46e533; }
    .hero h1 { margin:0; font-size:2.25rem; } .hero p { margin:.55rem 0 0; opacity:.88; }
    .eyebrow { color:#635bff; font-weight:700; font-size:.75rem; letter-spacing:.1em; text-transform:uppercase; margin:1.4rem 0 .4rem; }
    div[data-testid="stMetric"] { background:#fff; padding:.9rem 1rem; border:1px solid #e6e8f0; border-radius:15px; box-shadow:0 4px 14px #1720330d; }
    .stPlotlyChart { background:#fff; border:1px solid #e6e8f0; border-radius:15px; padding:.3rem; }
    </style>""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_data(data_file, file_mtime):
    _, data = load_data(data_file)
    data = data[~data["expense"].str.startswith("total", na=False)].copy()
    data["category"] = data.apply(clean_category, axis=1)
    data["month_label"] = data["date"].dt.strftime("%b %Y")
    return data


def clean_category(row):
    expense = str(row["expense"]).strip().lower()
    if expense in EXACT_CATEGORY_FIXES:
        return EXACT_CATEGORY_FIXES[expense]
    if row["category"] != "unrecognized":
        return row["category"]
    if any(word in expense for word in ("marriage", "farewell", "pooja", "gift")):
        return "gifts & events"
    if any(word in expense for word in ("hotel", "nasta", "snaks", "restaurant")):
        return "food"
    if any(word in expense for word in ("repair", "home key", "room key")):
        return "home maintenance"
    return "needs review"


def money(value):
    return f"₹{value:,.0f}"


def main():
    st.set_page_config(page_title="Financer AI", page_icon="💸", layout="wide")
    apply_theme()
    data_file = os.getenv("FINANCE_DATA_FILE", DEFAULT_DATA_FILE)
    if not Path(data_file).exists():
        st.error(f"Finance data was not found: {data_file}")
        st.stop()
    data = get_data(data_file, Path(data_file).stat().st_mtime_ns)

    st.sidebar.title("💸 Financer AI")
    st.sidebar.caption("Your personal spending cockpit")
    st.sidebar.divider()
    years = sorted(data.date.dt.year.unique(), reverse=True)
    selected_years = st.sidebar.multiselect("Years", years, default=years)
    available = data[data.date.dt.year.isin(selected_years)]
    categories = sorted(available.category.unique())
    selected_categories = st.sidebar.multiselect("Categories", categories, default=categories)
    start, end = st.sidebar.date_input("Date range", (available.date.min().date(), available.date.max().date()))
    view = available[
        available.category.isin(selected_categories)
        & available.date.between(pd.Timestamp(start), pd.Timestamp(end))
    ].copy()

    st.markdown("""<div class="hero"><h1>💸 A calmer view of your money</h1>
    <p>Explore patterns, understand your categories, and find the next smart saving opportunity.</p></div>""", unsafe_allow_html=True)
    st.markdown('<p class="eyebrow">Your selected period</p>', unsafe_allow_html=True)
    months = view.date.dt.to_period("M").nunique()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total spend", money(view.price.sum()))
    c2.metric("Transactions", f"{len(view):,}")
    c3.metric("Monthly average", money(view.price.sum() / months if months else 0))
    c4.metric("Top category", view.groupby("category").price.sum().idxmax().title() if not view.empty else "—")

    if view.empty:
        st.warning("No transactions match these filters.")
        st.stop()

    category = view.groupby("category", as_index=False).price.sum().sort_values("price", ascending=False)
    monthly = (
        view.assign(month=view["date"].dt.to_period("M"))
        .groupby("month", as_index=False)["price"]
        .sum()
    )
    monthly["month"] = monthly["month"].astype(str)
    left, right = st.columns([1.28, 1])
    with left:
        st.markdown('<p class="eyebrow">Spending momentum</p>', unsafe_allow_html=True)
        fig = px.area(monthly, x="month", y="price", markers=True, color_discrete_sequence=[COLORS[0]])
        fig.update_layout(xaxis_title=None, yaxis_title="Spend", margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown('<p class="eyebrow">Category mix</p>', unsafe_allow_html=True)
        pie = px.pie(category.head(8), names="category", values="price", hole=.6, color_discrete_sequence=COLORS)
        pie.update_layout(margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(pie, use_container_width=True)

    st.markdown('<p class="eyebrow">Category leaderboard</p>', unsafe_allow_html=True)
    bar = px.bar(category.head(12), x="price", y="category", orientation="h", text_auto=".3s", color="price", color_continuous_scale=["#c7d2fe", "#635bff"])
    bar.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Spend", yaxis_title=None, coloraxis_showscale=False, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(bar, use_container_width=True)

    review = view[view.category.eq("needs review")][["date", "expense", "price"]].sort_values("price", ascending=False)
    with st.expander(f"Review {len(review)} ambiguous transactions", expanded=False):
        st.caption("These labels are deliberately not guessed. Add a rule when you know what they represent.")
        st.dataframe(review, use_container_width=True, hide_index=True)

    st.markdown('<p class="eyebrow">Recent transactions</p>', unsafe_allow_html=True)
    recent = view.sort_values("date", ascending=False)[["date", "expense", "category", "price"]].head(20)
    st.dataframe(recent, use_container_width=True, hide_index=True, column_config={"price": st.column_config.NumberColumn("Amount", format="₹%d")})


if __name__ == "__main__":
    main()
