"""Test script to verify date extraction logic works correctly."""

# Simulate the date extraction without requiring pandas
from datetime import datetime

MONTHS = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
    'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
    'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}

def extract_date_filter(query):
    """
    Extract month/year from query.
    Returns: (month, year) or (None, None)
    """
    import re
    query_lower = query.lower()
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Check for "this month" / "current month"
    if re.search(r'\b(this month|current month)\b', query_lower):
        return (current_month, current_year)
    
    # Check for "last month"
    if re.search(r'\blast month\b', query_lower):
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        return (prev_month, prev_year)
    
    # Check for explicit month name
    for month_name, month_num in MONTHS.items():
        if month_name in query_lower:
            # Try to extract year
            year_match = re.search(r'\b(20\d{2}|2\d|[0-9]{1,2})\b', query_lower)
            if year_match:
                year_str = year_match.group(1)
                year = int(year_str)
                # Handle 2-digit years
                if year < 100:
                    year = 2000 + year if year < 50 else 1900 + year
            else:
                year = current_year
            
            return (month_num, year)
    
    return (None, None)


# Test cases
test_queries = [
    "how much did I spend in june 2026",
    "spending on june",
    "what did I spend last month",
    "this month spending",
    "expenses in december 2025",
    "how much for july",
]

print("Testing date extraction:")
print("-" * 50)
for query in test_queries:
    month, year = extract_date_filter(query)
    if month:
        month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                      7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        print(f"✓ '{query}' -> {month_names[month]} {year}")
    else:
        print(f"✗ '{query}' -> No date detected")

print("\nAll tests completed!")
