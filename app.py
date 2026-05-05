import streamlit as st
from data_loader import load_data
from embedder import create_embeddings
from rag_engine import VectorDB
from ai_service import  generate_answer_with_memory

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Finance AI", layout="wide")
st.title("💰 Personal Finance AI Advisor")

# ---------------------------
# LOAD DATA (CACHED)
# ---------------------------
@st.cache_resource
def setup():
    documents, all_data = load_data("expense.xlsx")
    embeddings = create_embeddings(documents)
    db = VectorDB(embeddings, documents)
    return db, all_data

db, all_data = setup()
all_data['year'] = all_data['date'].dt.year
all_data['month'] = all_data['date'].dt.month
all_data['day'] = all_data['date'].dt.day
# ---------------------------
# FILTERS
# ---------------------------
st.sidebar.header("📌 Filters")

years = sorted(all_data['year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

months = list(range(1, 13))
selected_month = st.sidebar.selectbox("Select Month", ["All"] + months)

days = list(range(1, 32))
selected_day = st.sidebar.selectbox("Select Day", ["All"] + days)

# Apply filters
filtered_data = all_data[all_data['year'] == selected_year]

if selected_month != "All":
    filtered_data = filtered_data[filtered_data['month'] == selected_month]

if selected_day != "All":
    filtered_data = filtered_data[filtered_data['day'] == selected_day]

# ---------------------------
# SUMMARY
# ---------------------------
st.subheader("📊 Overall Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(all_data))
col2.metric("Total Spend", f"₹{round(all_data['price'].sum(), 2)}")
col3.metric(
    "Date Range",
    f"{all_data['date'].min().date()} : {all_data['date'].max().date()}"
)

# ---------------------------
# Filtered Overview
# ---------------------------
st.subheader("📊 Filtered Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Records", len(filtered_data))
col2.metric("Spend", f"₹{round(filtered_data['price'].sum(), 2)}")
col3.metric(
    "Range",
    f"{filtered_data['date'].min().date()} : {filtered_data['date'].max().date()}"
)
# ---------------------------
# MONTHLY TREND
# ---------------------------
st.subheader("📈 Monthly Spending")

monthly = filtered_data.groupby(filtered_data['date'].dt.to_period('M'))['price'].sum()
monthly.index = monthly.index.astype(str)

st.line_chart(monthly)

# ---------------------------
# CATEGORY ANALYSIS
# ---------------------------
st.subheader("📊 Top Categories")

category = (
    filtered_data.groupby('category')['price']
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category.head(10))

# ---------------------------
# SMART INSIGHTS (NO LLM)
# ---------------------------
st.subheader("🧠 Smart Insights")

if not category.empty:
    top_category = category.idxmax()
    top_value = category.max()

    st.success(f"💡 Highest spending: {top_category} (₹{round(top_value,2)})")

    # Rule-based alert
    total_spend = filtered_data['price'].sum()
    if total_spend > 0:
        percentage = (top_value / total_spend) * 100

        if percentage > 40:
            st.warning(f"⚠️ {top_category} takes {round(percentage,2)}% of your spending. Consider reducing it.")

# finance chatbot
st.subheader("🤖 Finance Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
query = st.chat_input("Ask about your expenses...")

if query:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    # 🔥 Build conversation context
    history = "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]]
    )

    # 🔥 Modify your AI call
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            answer = generate_answer_with_memory(query, db, all_data, history)

            st.write(answer)

    # Store assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})