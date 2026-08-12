from groq import Groq
from embedder import model
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def _document_matches_period(doc, month, year, day=None):
    if month is None or year is None:
        return True

    try:
        abbr_month = datetime(year, month, 1).strftime("%b")
    except ValueError:
        return True

    doc_lower = doc.lower()

    if day is not None:
        date_label = f"on {day:02d} {abbr_month} {year}".lower()
        return date_label in doc_lower

    return f" {abbr_month.lower()} {year}" in doc_lower


def _build_summary(all_data):
    top_categories = (
        all_data.groupby('category')['price']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    top_summary = "; ".join(
        f"{cat}: ₹{round(val, 2)}" for cat, val in top_categories.items()
    ) or "No category data available."

    monthly = (
        all_data.groupby(all_data['date'].dt.to_period('M'))['price']
        .sum()
        .sort_index()
    )
    monthly_summary = "; ".join(
        f"{period}: ₹{round(val, 2)}" for period, val in monthly.tail(6).items()
    ) or "No monthly data available."

    return top_summary, monthly_summary


def generate_answer_with_memory(query, db, all_data, history="", month=None, year=None, day=None):
    if all_data.empty:
        period_text = "this period" if month else "the dataset"
        return f"I found no expense records for {period_text}."

    if month is not None and year is not None and not all_data.empty:
        context_rows = []
        for _, row in all_data.sort_values('date').iterrows():
            date_str = row['date'].strftime("%d %b %Y")
            context_rows.append(
                f"on {date_str}, spent ₹{row['price']} on {row['expense']} in category {row['category']}"
            )
        context = "\n".join(context_rows[:50])
    else:
        query_embedding = model.encode([query])
        k = min(50, len(all_data)) if len(all_data) > 0 else 1
        results = db.search(query_embedding, k)
        context = "\n".join(results[:20])

    top_summary, monthly_summary = _build_summary(all_data)

    date_context = ""
    period_text = "all available data"
    if month is not None and year is not None:
        month_name = datetime(year, month, 1).strftime("%B")
        if day is not None:
            date_context = (
                f"The user is asking specifically about {day} {month_name} {year}. "
                "Only use data from that exact date."
            )
            period_text = f"{day} {month_name} {year}"
        else:
            date_context = (
                f"The user is asking specifically about {month_name} {year}. "
                "Only use data from that month and year."
            )
            period_text = f"{month_name} {year}"

    summary = f"""
    Total records in selected period: {len(all_data)}
    Date range: {all_data['date'].min()} to {all_data['date'].max()}
    Total spend: ₹{round(all_data['price'].sum(), 2)}
    Top categories: {top_summary}
    Recent monthly spending: {monthly_summary}
    """

    prompt = f"""
    You are a financial analyst.

    IMPORTANT:
    - The dataset provided is FILTERED and complete for the requested period.
    - Do NOT assume missing data or reference information outside the provided period.
    - If the user asks for a specific date or month, answer precisely using the provided records.
    {date_context}

    DATA SUMMARY:
    {summary}

    Conversation history:
    {history}

    SAMPLE DATA:
    {context}

    Question: {query}

    Provide:
    1. A concise and accurate answer
    2. Spending patterns or insights for the selected period
    3. Practical suggestions if appropriate
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
