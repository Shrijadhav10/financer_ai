import streamlit as st
import plotly.express as px


def show_category_drilldown(filtered_data, category):

    st.subheader("🔍 Explore Category Details")

    selected_category = st.selectbox(
        "Select Category",
        category.index.tolist()
    )

    category_data = filtered_data[
        filtered_data['category'] == selected_category
    ]

    st.metric(
        f"Total Spend in {selected_category}",
        f"₹{round(category_data['price'].sum(), 2)}"
    )

    item_breakdown = (
        category_data.groupby('expense')['price']
        .sum()
        .sort_values(ascending=False)
    )

    st.write(f"### 📌 Items inside {selected_category}")

    st.dataframe(item_breakdown)

    item_df = item_breakdown.reset_index()
    item_df.columns = ['Expense', 'Spend']

    fig = px.bar(
        item_df,
        x='Expense',
        y='Spend',
        text_auto=True,
        title=f'{selected_category} Breakdown'
    )

    st.plotly_chart(fig, use_container_width=True)