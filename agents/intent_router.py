def detect_intent(query):

    query = query.lower()

    if "total spend" in query:
        return "TOTAL_SPEND"

    elif "food" in query:
        return "CATEGORY_SPEND"

    elif "save" in query:
        return "SAVINGS"

    elif "overspending" in query:
        return "OVESPENDING"

    else:
        return "RAG"