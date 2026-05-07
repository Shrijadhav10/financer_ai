import streamlit as st


def apply_filters(all_data):

    st.sidebar.header("📌 Filters")

    # -------------------
    # YEAR
    # -------------------
    years = sorted(all_data['year'].dropna().unique())

    selected_year = st.sidebar.selectbox(
        "Select Year",
        ["All"] + list(years)
    )

    if selected_year != "All":
        year_filtered = all_data[
            all_data['year'] == selected_year
        ]
    else:
        year_filtered = all_data

    # -------------------
    # MONTH
    # -------------------
    available_months = sorted(
        year_filtered['month'].dropna().unique()
    )

    selected_month = st.sidebar.selectbox(
        "Select Month",
        ["All"] + list(available_months)
    )

    if selected_month != "All":
        month_filtered = year_filtered[
            year_filtered['month'] == selected_month
        ]
    else:
        month_filtered = year_filtered

    # -------------------
    # DAY
    # -------------------
    available_days = sorted(
        month_filtered['day'].dropna().unique()
    )

    selected_day = st.sidebar.selectbox(
        "Select Day",
        ["All"] + list(available_days)
    )

    filtered_data = month_filtered

    if selected_day != "All":
        filtered_data = filtered_data[
            filtered_data['day'] == selected_day
        ]

    return filtered_data