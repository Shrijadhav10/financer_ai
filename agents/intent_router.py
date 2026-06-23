from utils.date_extractor import extract_date_filter

DATE_QUERY_KEYWORDS = [
    "spend",
    "spent",
    "expense",
    "expenses",
    "cost",
    "paid",
    "payment",
]


def detect_intent(query):
    query_lower = query.lower()

    if any(word in query_lower for word in ["buy", "purchase", "afford", "plan", "save for", "can i get"]):
        if any(word in query_lower for word in ["bike", "car", "laptop", "phone", "house", "rupees", "rs"]):
            return "PURCHASE_ADVICE"

    if "advice" in query_lower or "suggest" in query_lower or "recommend" in query_lower:
        return "FINANCIAL_ADVICE"

    if "total spend" in query_lower and not any(
        month in query_lower
        for month in [
            'january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december',
            'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct',
            'nov', 'dec', 'month'
        ]
    ):
        return "TOTAL_SPEND"

    if "forecast" in query_lower or ("future" in query_lower and any(keyword in query_lower for keyword in ["spend", "expense", "expenses"])):
        return "FORECAST"

    if any(word in query_lower for word in ["which", "where", "most", "top"]) and "spend" in query_lower:
        return "TOP_CATEGORY_SPEND"

    if "food" in query_lower:
        return "CATEGORY_SPEND"

    if "save" in query_lower:
        return "SAVINGS"

    if "overspending" in query_lower or "overspend" in query_lower:
        return "OVESPENDING"

    if any(keyword in query_lower for keyword in DATE_QUERY_KEYWORDS):
        month, year, day = extract_date_filter(query_lower)
        if month is not None:
            return "DATE_SPEND" if day is not None else "MONTHLY_SPEND"

    return "RAG"