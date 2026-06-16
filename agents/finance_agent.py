from agents.intent_router import detect_intent

from tools.expense_tools import (
    get_total_spend,
    get_category_spend,
    get_top_categories
)

from tools.analytics_tools import (
    detect_overspending,
    savings_suggestions
)

from ai_service import generate_answer_with_memory


def run_finance_agent(query, df, db, history):

    intent = detect_intent(query)

    # --------------------------
    # TOTAL SPEND
    # --------------------------
    if intent == "TOTAL_SPEND":

        total = get_total_spend(df)

        return f"Your total spending is ₹{total}"

    # --------------------------
    # CATEGORY SPEND
    # --------------------------
    elif intent == "CATEGORY_SPEND":

        food_spend = get_category_spend(
            df,
            "food"
        )

        return f"Your food spending is ₹{food_spend}"

    # --------------------------
    # SAVINGS
    # --------------------------
    elif intent == "SAVINGS":

        categories = get_top_categories(df)

        suggestions = savings_suggestions(categories)

        return "\n".join(suggestions)

    # --------------------------
    # OVERSPENDING
    # --------------------------
    elif intent == "OVESPENDING":

        categories = get_top_categories(df)

        total = get_total_spend(df)

        alerts = detect_overspending(
            categories,
            total
        )

        return "\n".join(alerts)

    # --------------------------
    # FALLBACK → RAG
    # --------------------------
    else:

        return generate_answer_with_memory(
            query,
            db,
            df,
            history
        )