CATEGORY_MAP = {
    "food": ["lunch", "dinner", "breakfast", "poha", "thali", "zomato", "swiggy", "banana"],
    "rent": ["rent", "room rent"],
    "transport": ["bus", "uber", "petrol", "fuel"],
}

def categorize(expense):
    expense_lower = str(expense).lower()

    for category, keywords in CATEGORY_MAP.items():
        if any(word in expense_lower for word in keywords):
            return category

    # ✅ fallback → keep original
    return expense_lower