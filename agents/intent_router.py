"""Classify user queries into finance-agent intents.

Previously this used an ordered chain of `if "keyword" in query` checks,
which broke down whenever a query legitimately contained keywords for two
different intents (e.g. "which food categories should I save on?" contains
both "food" and "save", and whichever `if` came first in the file silently
won, regardless of what the user actually meant).

This version asks the LLM to classify the query into exactly one of the
existing intent labels. The set of valid labels is unchanged from before —
every label finance_agent.py already matches on (including the
DATE_SPEND/MONTHLY_SPEND split and the OVESPENDING spelling) still works
without any changes to finance_agent.py.

DATE_SPEND vs MONTHLY_SPEND is still resolved using the existing regex-based
extract_date_filter(), not the LLM, since "is there a specific day in this
query" is a parsing problem the regex already solves reliably -- asking an
LLM to do date extraction would be a downgrade, not an improvement.
"""

import os
from groq import Groq
from dotenv import load_dotenv

from utils.date_extractor import extract_date_filter

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Every label finance_agent.py's if/elif chain checks for. Keep this list
# and finance_agent.py's checks in sync if either one changes.
VALID_INTENTS = [
    "PURCHASE_ADVICE",
    "FINANCIAL_ADVICE",
    "TOTAL_SPEND",
    "FORECAST",
    "TOP_CATEGORY_SPEND",
    "CATEGORY_SPEND",
    "ITEM_SPEND",
    "SAVINGS",
    "OVESPENDING",
    "DATE_QUERY",   # internal-only label; resolved to DATE_SPEND/MONTHLY_SPEND below
    "RAG",
]

# Safe default if the LLM call fails or returns something unparseable.
# RAG is the catch-all fallback path in finance_agent.py, so defaulting
# here is always a valid choice even when classification goes wrong.
FALLBACK_INTENT = "RAG"

CLASSIFICATION_PROMPT = """You are an intent classifier for a personal finance chatbot. \
Classify the user's query into EXACTLY ONE of these labels. Reply with ONLY the label, nothing else -- no explanation, no punctuation.

PURCHASE_ADVICE - asking if they can afford to buy/purchase a specific item (bike, car, laptop, phone, house, etc.), usually with a price mentioned
FINANCIAL_ADVICE - asking for general financial advice, suggestions, or recommendations about their finances overall
TOTAL_SPEND - asking for their all-time total spending, with no specific month/category mentioned
FORECAST - asking to predict/forecast future spending
TOP_CATEGORY_SPEND - asking which category/categories they spend the most on, or for a ranked breakdown by category
CATEGORY_SPEND - asking specifically about food spending
ITEM_SPEND - asking about spending on a specific item/product (e.g. "athithi", "banana", "ola", "gym", etc.) that is not a category
SAVINGS - asking how to save money or for savings suggestions (not asking to forecast or buy something)
OVESPENDING - asking about overspending or where they are overspending
DATE_QUERY - asking about spending on a specific date, day, month, or time period (e.g. "June 2026", "last month", "yesterday")
RAG - anything else: open-ended questions, follow-ups, or questions that don't clearly match another label above

Rules:
- If the query mentions buying/affording a specific priced item, always choose PURCHASE_ADVICE, even if it also mentions saving or a date.
- If the query asks "which/where/what category do I spend most on", choose TOP_CATEGORY_SPEND even if "food" is also mentioned.
- Only choose CATEGORY_SPEND if food is the clear subject and no ranking ("top", "which", "most") is being asked for.
- Only choose ITEM_SPEND if asking about a specific product/item name (like a restaurant, food item, app, etc.), NOT a category.
- If uncertain, prefer RAG over guessing a structured intent.

User query: "{query}"

Label:"""


def _classify_with_llm(query):
    """Call Groq to classify the query. Returns a raw label string."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,  # deterministic classification, not creative text
        max_tokens=20,
        messages=[
            {"role": "user", "content": CLASSIFICATION_PROMPT.format(query=query)}
        ],
    )
    raw = response.choices[0].message.content or ""
    return raw.strip().upper()


def detect_intent(query):
    """Classify a query into one of finance_agent.py's known intent strings."""
    try:
        label = _classify_with_llm(query)
    except Exception as e:
        print(f"Warning: intent classification failed ({e}); defaulting to {FALLBACK_INTENT}")
        return FALLBACK_INTENT

    # The model is told to reply with only the label, but defensively handle
    # extra words/punctuation by checking containment against known labels.
    matched = next((intent for intent in VALID_INTENTS if intent in label), None)

    if matched is None:
        return FALLBACK_INTENT

    if matched == "DATE_QUERY":
        # Reuse the existing reliable regex-based date parser to decide
        # DATE_SPEND (specific day mentioned) vs MONTHLY_SPEND (month only).
        # If no date can actually be parsed out of a query the LLM thought
        # was date-related, fall back to RAG rather than guessing.
        month, year, day = extract_date_filter(query)
        if month is None:
            return FALLBACK_INTENT
        return "DATE_SPEND" if day is not None else "MONTHLY_SPEND"

    return matched