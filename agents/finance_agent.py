from agents.intent_router import detect_intent
from utils.date_extractor import (
    extract_date_filter,
    filter_by_date,
    get_month_year_text,
    get_day_month_year_text,
)

from tools.expense_tools import (
    get_total_spend,
    get_category_spend,
    get_top_categories,
    get_item_spend,
    get_item_spend_detailed,
)

from tools.analytics_tools import (
    detect_overspending,
    savings_suggestions,
    forecast_spending,
    calculate_purchase_affordability,
    spending_trend,
)

from ai_service import generate_answer_with_memory


def run_finance_agent(query, df, db, history):
    # Check if user wants to use LLM directly
    use_llm_keywords = ["use llm", "use ai", "llm", "ask ai", "ai answer"]
    should_use_llm = any(keyword in query.lower() for keyword in use_llm_keywords)
    
    if should_use_llm:
        # Skip intent routing and go directly to LLM
        month, year, day = extract_date_filter(query)
        filtered_df = filter_by_date(df, month, year, day)
        # Remove the "use llm" keyword from the query before sending to LLM
        cleaned_query = query.lower()
        for keyword in use_llm_keywords:
            cleaned_query = cleaned_query.replace(keyword, "").strip()
        
        response = generate_answer_with_memory(
            cleaned_query if cleaned_query else query, 
            db, 
            filtered_df, 
            history, 
            month, 
            year, 
            day
        )
        return response
    
    intent = detect_intent(query)

    if intent == "TOTAL_SPEND":
        total = get_total_spend(df)
        return f"Your total spending is ₹{total}"

    elif intent == "DATE_SPEND":
        month, year, day = extract_date_filter(query)
        filtered_df = filter_by_date(df, month, year, day)

        if filtered_df.empty:
            date_text = get_day_month_year_text(month, year, day)
            return f"No spending data found for {date_text}."

        total = get_total_spend(filtered_df)
        date_text = get_day_month_year_text(month, year, day)
        return f"Your spending on {date_text} is ₹{total}"

    elif intent == "MONTHLY_SPEND":
        month, year, day = extract_date_filter(query)
        filtered_df = filter_by_date(df, month, year, day)

        if filtered_df.empty:
            date_text = get_month_year_text(month, year)
            return f"No spending data found for {date_text}."

        total = get_total_spend(filtered_df)
        date_text = get_month_year_text(month, year)
        return f"Your spending in {date_text} is ₹{total}"

    elif intent == "CATEGORY_SPEND":
        food_spend = get_category_spend(df, "food")
        return f"Your food spending is ₹{food_spend}"

    elif intent == "ITEM_SPEND":
        import re
        # Extract item name from query
        # Try to find quoted text first
        quoted_match = re.search(r'["\']([^"\']+)["\']', query)
        item_name = quoted_match.group(1) if quoted_match else None
        
        # If no quotes, try to extract common patterns like "on X", "for X", "spent on X"
        if not item_name:
            patterns = [
                r'spent on (\w+)',
                r'spent on ([^\?\.\!]+?)(?:\?|$)',
                r'on (\w+)',
                r'for (\w+)',
                r'how much.*?(\w+)',
                r'how much.*?(\w[\w\s]*)',
            ]
            for pattern in patterns:
                match = re.search(pattern, query.lower())
                if match:
                    item_name = match.group(1).strip()
                    break
        
        if not item_name:
            # Try to use context from history if available
            if history and "on " in query.lower():
                return "I couldn't identify which item you're asking about. Try asking like: 'How much did I spend on athithi?' or 'What's my spending on banana?'"
            return "I couldn't identify which item you're asking about. Try asking like: 'How much did I spend on athithi?' or 'What's my spending on banana?'"
        
        month, year, day = extract_date_filter(query)
        
        # If no date in current query, try to extract from history context
        if month is None and year is None and history:
            # Look for date references in recent history
            if "june" in history.lower() and "2026" in history.lower():
                month, year = 6, 2026
            elif "last month" in history.lower():
                from datetime import datetime, timedelta
                today = datetime.now()
                last_month = today - timedelta(days=30)
                month, year = last_month.month, last_month.year
        
        filtered_df = filter_by_date(df, month, year, day)
        
        # Check if user is asking for dates/details
        asking_for_dates = any(keyword in query.lower() for keyword in [
            "when", "date", "dates", "which date", "on what date", 
            "specific date", "all dates", "list", "transactions", "details", "breakdown"
        ])
        
        if asking_for_dates:
            # Use detailed transaction data
            item_data = get_item_spend_detailed(filtered_df, item_name)
            
            if not item_data:
                date_period = get_day_month_year_text(month, year, day) if day else (get_month_year_text(month, year) if month else "overall")
                return f"No spending found for '{item_name}' {date_period}."
            
            date_period = get_day_month_year_text(month, year, day) if day else (get_month_year_text(month, year) if month else "overall")
            
            response = f"**Detailed Spending on '{item_name.title()}' ({date_period}):**\n\n"
            response += f"📊 **Summary:**\n"
            response += f"- Total: ₹{item_data['total']}\n"
            response += f"- Transactions: {item_data['count']}\n"
            response += f"- Average per transaction: ₹{item_data['average']}\n\n"
            
            response += f"📋 **Transaction Details:**\n"
            for i, txn in enumerate(item_data['transactions'], 1):
                date_str = txn['date'].strftime('%d-%b-%Y') if hasattr(txn['date'], 'strftime') else str(txn['date'])
                response += f"\n{i}. **{date_str}** - ₹{txn['amount']} ({txn['expense']})"
            
            return response
        else:
            # Use summary data (faster)
            item_data = get_item_spend(filtered_df, item_name)
            
            if item_data["count"] == 0:
                date_period = get_day_month_year_text(month, year, day) if day else (get_month_year_text(month, year) if month else "overall")
                return f"No spending found for '{item_name}' {date_period}."
            
            date_period = get_day_month_year_text(month, year, day) if day else (get_month_year_text(month, year) if month else "overall")
            
            response = f"**Spending on '{item_name.title()}' ({date_period}):**\n\n"
            response += f"- Total: ₹{item_data['total']}\n"
            response += f"- Transactions: {item_data['count']}\n"
            response += f"- Average per transaction: ₹{item_data['average']}"
            
            if item_data['count'] > 0:
                response += f"\n\n💡 _Tip: Ask 'When did I spend on {item_name}?' for dates_"
            
            return response

    elif intent == "TOP_CATEGORY_SPEND":
        month, year, day = extract_date_filter(query)
        filtered_df = filter_by_date(df, month, year, day)
        categories = get_top_categories(filtered_df)

        if categories.empty:
            return "No spending categories found in the selected period."

        top_items = list(categories.items())[:5]
        top_lines = [f"{cat}: ₹{round(val, 2)}" for cat, val in top_items]
        period_text = get_day_month_year_text(month, year, day) if day else get_month_year_text(month, year) if month else "all time"
        return f"Top spending categories for {period_text}:\n" + "\n".join(top_lines)

    elif intent == "FORECAST":
        month, year, day = extract_date_filter(query)
        filtered_df = filter_by_date(df, month, year, day)
        forecast = forecast_spending(filtered_df, periods=6)

        if not forecast:
            return "Not enough historical spending data to generate a forecast."

        forecast_lines = [f"{period}: ₹{amount}" for period, amount in forecast]
        return "Spending forecast for the next 6 months:\n" + "\n".join(forecast_lines)

    elif intent == "SAVINGS":
        categories = get_top_categories(df)
        suggestions = savings_suggestions(categories)
        return "\n".join(suggestions)

    elif intent == "OVESPENDING":
        categories = get_top_categories(df)
        total = get_total_spend(df)
        alerts = detect_overspending(categories, total)
        return "\n".join(alerts)

    elif intent == "PURCHASE_ADVICE":
        import re
        from datetime import datetime

        price_match = re.search(r'(\d+(?:,\d{3})*(?:\.\d{2})?)', query.replace(',', ''))
        target_price = float(price_match.group(1)) if price_match else None

        if not target_price:
            return "I couldn't find the price of the item. Please mention the price clearly (e.g., '269000 Rs' or '2,69,000')."

        month, year, day = extract_date_filter(query)
        months_until = 1
        if month is not None and year is not None:
            today = datetime.now()
            target_date = datetime(year, month, 1)
            if target_date > today:
                delta = (target_date - today).days
                months_until = max(1, round(delta / 30))

        affordability = calculate_purchase_affordability(df, target_price, months_until)
        if not affordability:
            return "Not enough spending data to analyze affordability."

        trend = spending_trend(df, 6)
        total_spend = get_total_spend(df)
        avg_monthly = affordability["avg_monthly_spend"]

        response = f"""
**Purchase Analysis: Item Price ₹{int(target_price)}**

**Your Spending Profile:**
- Average monthly spend: ₹{int(avg_monthly)}
- Total historical spend: ₹{int(total_spend)}
- {trend}

**Affordability Check ({months_until} month{'s' if months_until > 1 else ''} to save):**
- Monthly savings needed: ₹{int(affordability['monthly_needed_to_save'])}
- Your current monthly surplus: ₹{int(affordability['monthly_surplus'])}

**Recommendation:**
"""

        if affordability["is_affordable"]:
            response += f"✅ **You CAN afford this purchase!** Your current spending allows you to save ₹{int(affordability['monthly_surplus'])} extra per month. You can buy the bike in {months_until} month(s) by reducing discretionary spending slightly."
        else:
            shortfall = abs(affordability["monthly_surplus"])
            months_needed = round(target_price / avg_monthly)
            response += f"❌ **Currently tight.** You'd need to save ₹{int(affordability['monthly_needed_to_save'])}/month, but currently spend ₹{int(avg_monthly)}/month. You can afford it in about {int(months_needed)} months if you:"
            response += f"\n  1. Cut unnecessary expenses by ₹{int(shortfall)}/month\n  2. Redirect that towards savings\n  3. Or wait {int(months_needed)} months and buy from regular savings"

        response += f"\n\n**Action Steps:**\n1. Track discretionary spending (dining out, entertainment)\n2. Set automatic savings of ₹{int(affordability['monthly_needed_to_save'])} per month\n3. Monitor progress monthly"

        return response

    elif intent == "FINANCIAL_ADVICE":
        if df.empty:
            return "I need expense data to provide financial advice. Please upload your expense data."

        total = get_total_spend(df)
        categories = get_top_categories(df)
        trend = spending_trend(df, 6)
        months_of_data = len(df.groupby(df['date'].dt.to_period('M')))
        avg_monthly = total / max(months_of_data, 1)

        suggestions = savings_suggestions(categories)
        alerts = detect_overspending(categories, total)

        response = f"""
**Your Financial Overview:**

📊 **Spending Summary:**
- Total spend: ₹{int(total)}
- Average monthly: ₹{int(avg_monthly)}
- Data period: {months_of_data} months
- {trend}

**Top Spending Categories:**
"""
        for i, (cat, val) in enumerate(list(categories.items())[:5], 1):
            pct = (val / total * 100) if total else 0
            response += f"\n{i}. {cat.title()}: ₹{int(val)} ({pct:.1f}%)"

        if alerts:
            response += "\n\n⚠️ **Overspending Alerts:**\n" + "\n".join(alerts)

        if suggestions:
            response += "\n\n💡 **Savings Opportunities:**\n" + "\n".join(suggestions[:3])

        response += "\n\n✅ **Recommendations:**\n1. Focus on the top 3 categories for cost reduction\n2. Set monthly budget 10-15% below current average\n3. Track discretionary vs essential spending separately"

        return response

    else:
        month, year, day = extract_date_filter(query)
        filtered_df = filter_by_date(df, month, year, day)
        return generate_answer_with_memory(query, db, filtered_df, history, month, year, day)


