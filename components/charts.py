import streamlit as st
import plotly.express as px
import pandas as pd


def show_monthly_trend(filtered_data):

    st.subheader("📈 Monthly Spending Trend")

    monthly = (
        filtered_data
        .groupby(filtered_data['date'].dt.to_period('M'))['price']
        .sum()
    )

    monthly.index = monthly.index.astype(str)

    monthly_df = monthly.reset_index()
    monthly_df.columns = ['Month', 'Spend']

    fig = px.line(
        monthly_df,
        x='Month',
        y='Spend',
        markers=True,
        title='Monthly Spending Trend'
    )

    st.plotly_chart(fig, use_container_width=True)


def show_category_chart(filtered_data):

    st.subheader("📊 Category-wise Spending")

    category = (
        filtered_data.groupby('category')['price']
        .sum()
        .sort_values(ascending=False)
    )

    category_df = category.reset_index()
    category_df.columns = ['Category', 'Spend']

    # -------------------------
    # TOP 10 + OTHERS
    # -------------------------
    top_10 = category_df.head(10)

    others_value = category_df.iloc[10:]['Spend'].sum()

    if others_value > 0:

        others_row = pd.DataFrame({
            'Category': ['Others'],
            'Spend': [others_value]
        })

        top_10 = pd.concat(
            [top_10, others_row],
            ignore_index=True
        )

    # -------------------------
    # BAR CHART
    # -------------------------
    fig = px.bar(
        top_10,
        x='Category',
        y='Spend',
        text_auto=True,
        title='Top Category Spending'
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # PIE CHART
    # -------------------------
    pie_fig = px.pie(
        top_10,
        names='Category',
        values='Spend',
        title='Category Distribution'
    )

    st.plotly_chart(pie_fig, use_container_width=True)

    return category