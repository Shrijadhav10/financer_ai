import streamlit as st


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