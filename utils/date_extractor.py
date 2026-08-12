"""Extract date information from natural language queries."""

import re
from datetime import datetime
import pandas as pd

MONTHS = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12,
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
    'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
    'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}

MONTH_NAME_PATTERN = r'(?:' + '|'.join(sorted(set(MONTHS.keys()), key=len, reverse=True)) + r')'
DATE_PATTERN_DAY_FIRST = re.compile(
    rf'\b([0-3]?\d)(?:st|nd|rd|th)?\s+({MONTH_NAME_PATTERN})(?:,?\s*(20\d{{2}}|[0-9]{{2}}))?\b',
    re.IGNORECASE,
)
DATE_PATTERN_MONTH_FIRST = re.compile(
    rf'\b({MONTH_NAME_PATTERN})\s+([0-3]?\d)(?:st|nd|rd|th)?(?:,?\s*(20\d{{2}}))?\b',
    re.IGNORECASE,
)
ISO_DATE_PATTERN = re.compile(r'\b(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b')


def _normalize_year(year_str):
    year = int(year_str)
    if year < 100:
        year = 2000 + year if year < 50 else 1900 + year
    return year


def extract_date_filter(query):
    """Extract month/year/day from a natural language query."""
    query_lower = query.lower()
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    if re.search(r'\b(this month|current month)\b', query_lower):
        return current_month, current_year, None

    if re.search(r'\blast month\b', query_lower):
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        return prev_month, prev_year, None

    iso_match = ISO_DATE_PATTERN.search(query_lower)
    if iso_match:
        year = int(iso_match.group(1))
        month = int(iso_match.group(2))
        day = int(iso_match.group(3))
        return month, year, day

    day_first_match = DATE_PATTERN_DAY_FIRST.search(query_lower)
    if day_first_match:
        day = int(day_first_match.group(1))
        month = MONTHS[day_first_match.group(2).lower()]
        year_str = day_first_match.group(3)
        year = _normalize_year(year_str) if year_str else current_year
        return month, year, day

    month_first_match = DATE_PATTERN_MONTH_FIRST.search(query_lower)
    if month_first_match:
        month = MONTHS[month_first_match.group(1).lower()]
        day = int(month_first_match.group(2))
        year_str = month_first_match.group(3)
        year = _normalize_year(year_str) if year_str else current_year
        return month, year, day

    for month_name, month_num in MONTHS.items():
        if month_name in query_lower:
            year_match = re.search(r'\b(20\d{2}|[0-9]{1,2})\b', query_lower)
            year = _normalize_year(year_match.group(1)) if year_match else current_year
            return month_num, year, None

    return None, None, None


def filter_by_date(df, month, year, day=None):
    """Filter dataframe by month, year, and optional day."""
    if month is None or year is None:
        return df

    filtered = df[
        (df['date'].dt.month == month) &
        (df['date'].dt.year == year)
    ]

    if day is not None:
        filtered = filtered[filtered['date'].dt.day == day]

    return filtered


def get_month_year_text(month, year):
    if month is None or year is None:
        return "all time"

    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    return f"{month_names.get(month, 'Unknown')} {year}"


def get_day_month_year_text(month, year, day=None):
    if month is None or year is None:
        return "all time"

    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    if day is not None:
        return f"{day} {month_names.get(month, 'Unknown')} {year}"
    return f"{month_names.get(month, 'Unknown')} {year}"
