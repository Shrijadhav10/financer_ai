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


def get_item_spend(df, item_name):
    """Get total spending for a specific item."""
    filtered = df[
        df['expense'].str.contains(item_name.lower(), case=False, na=False)
    ]
    
    total_amount = round(filtered['price'].sum(), 2)
    count = len(filtered)
    
    return {
        "total": total_amount,
        "count": count,
        "average": round(total_amount / count, 2) if count > 0 else 0
    }


def get_item_spend_detailed(df, item_name):
    """Get detailed spending for a specific item with transaction details and dates."""
    filtered = df[
        df['expense'].str.contains(item_name.lower(), case=False, na=False)
    ].copy()
    
    if filtered.empty:
        return None
    
    # Sort by date descending (most recent first)
    filtered = filtered.sort_values('date', ascending=False)
    
    total_amount = round(filtered['price'].sum(), 2)
    count = len(filtered)
    
    # Get transaction details
    transactions = []
    for idx, row in filtered.iterrows():
        transactions.append({
            "date": row['date'],
            "amount": row['price'],
            "expense": row['expense'],
            "category": row['category']
        })
    
    return {
        "total": total_amount,
        "count": count,
        "average": round(total_amount / count, 2) if count > 0 else 0,
        "transactions": transactions
    }