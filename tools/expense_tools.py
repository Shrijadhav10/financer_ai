def get_total_spend(df):

    return round(df['price'].sum(), 2)


def get_category_spend(df, category):

    filtered = df[
        df['category'] == category.lower()
    ]

    return round(filtered['price'].sum(), 2)


def get_monthly_spend(df):

    return (
        df.groupby(df['date'].dt.to_period('M'))['price']
        .sum()
    )


def get_top_categories(df, top_n=5):

    return (
        df.groupby('category')['price']
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )