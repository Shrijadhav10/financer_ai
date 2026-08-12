import streamlit as st
import pandas as pd


def show_advisor_dashboard(all_data):
    st.subheader("🧠 Financial Advisor Summary")

    if all_data.empty:
        st.info("No expense data is available to show advisor insights.")
        return

    latest_date = all_data['date'].max()
    three_years_ago = latest_date - pd.DateOffset(years=3)
    last_3_years = all_data[all_data['date'] >= three_years_ago]

    total_3y = last_3_years['price'].sum()
    months_covered = last_3_years['date'].dt.to_period('M').nunique()
    avg_monthly = total_3y / months_covered if months_covered else 0

    yearly = (
        last_3_years
        .groupby(last_3_years['date'].dt.year)['price']
        .sum()
        .sort_index()
    )

    current_year = yearly.index.max()
    previous_year = current_year - 1
    yoy_change = None

    if previous_year in yearly.index:
        yoy_change = (yearly.loc[current_year] - yearly.loc[previous_year]) / max(yearly.loc[previous_year], 1) * 100

    top_category = (
        last_3_years
        .groupby('category')['price']
        .sum()
        .sort_values(ascending=False)
    )

    top_category_name = top_category.index[0]
    top_category_value = top_category.iloc[0]
    top_share = top_category_value / total_3y * 100 if total_3y else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("3Y Spend", f"₹{round(total_3y, 0):,}")
    col2.metric("Avg Monthly", f"₹{round(avg_monthly, 0):,}")
    col3.metric("Top Category", f"{top_category_name}")

    if yoy_change is not None:
        arrow = "↗️" if yoy_change >= 0 else "↘️"
        st.write(f"**Year-over-year change:** {arrow} {round(yoy_change, 1)}%")

    st.markdown(
        f"**Top category share:** {round(top_share,1)}% ({top_category_name})"
    )

    suggestions = []

    if top_share > 35:
        suggestions.append(
            f"Your spending on **{top_category_name}** is high — consider trimming it to keep your budget balanced."
        )

    if avg_monthly > 0 and yoy_change is not None and yoy_change > 10:
        suggestions.append(
            "Spending is growing faster than last year. Review recurring expenses and look for savings in your biggest categories."
        )

    if avg_monthly < 20000:
        suggestions.append(
            "Your monthly spending is moderate. Keep tracking recurring categories and allocate some savings each month."
        )

    if not suggestions:
        suggestions.append(
            "Expense behavior looks stable. Keep monitoring category trends and avoid one-off high-cost items."
        )

    st.subheader("💬 Advisor Recommendations")
    for item in suggestions:
        st.write(f"- {item}")


def show_smart_insights(filtered_data, category):

    st.subheader("🧠 Smart Insights")

    if category.empty:
        st.info("No data available")
        return

    top_category = category.idxmax()
    top_value = category.max()

    st.success(
        f"💡 Highest spending category: {top_category} (₹{round(top_value,2)})"
    )

    total_spend = filtered_data['price'].sum()

    if total_spend > 0:
        percentage = (top_value / total_spend) * 100

        if percentage > 40:
            st.warning(
                f"⚠️ {top_category} takes {round(percentage,2)}% of total spending"
            )

        if percentage > 50:
            st.error(
                f"🚨 Overspending detected in {top_category}"
            )