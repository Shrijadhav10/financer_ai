import numpy as np
import pandas as pd


def detect_overspending(category_data, total_spend):
    alerts = []

    for category, value in category_data.items():
        pct = (value / total_spend) * 100 if total_spend else 0
        if pct > 40:
            alerts.append(
                f"High spending detected in {category}: {round(pct, 2)}%"
            )

    return alerts


def savings_suggestions(category_data):
    suggestions = []

    for category, value in category_data.items():
        suggested = value * 0.15
        suggestions.append(
            f"Reduce {category} by 15% → Save ₹{round(suggested, 2)}"
        )

    return suggestions


def get_monthly_spend_series(df):
    if df.empty:
        return df['price'].astype(float)

    monthly = (
        df.groupby(df['date'].dt.to_period('M'))['price']
        .sum()
        .sort_index()
    )
    monthly.index = monthly.index.astype(str)
    return monthly


def forecast_spending(df, periods=6):
    monthly = get_monthly_spend_series(df)
    if len(monthly) < 3:
        return []

    x = np.arange(len(monthly))
    y = monthly.values
    slope, intercept = np.polyfit(x, y, 1)

    last_period = pd.Period(monthly.index[-1], freq='M')
    forecast = []
    for i in range(1, periods + 1):
        future_period = last_period + i
        predicted = intercept + slope * (len(monthly) + i - 1)
        forecast.append((str(future_period), round(max(predicted, 0), 2)))

    return forecast


def spending_trend(df, months=6):
    monthly = get_monthly_spend_series(df).tail(months)
    if len(monthly) < 2:
        return "Not enough data to determine a trend."

    x = np.arange(len(monthly))
    y = monthly.values
    slope = np.polyfit(x, y, 1)[0]
    direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
    avg_change = round(abs(slope), 2)
    return f"Spending is {direction}, changing by about ₹{avg_change} per month over the last {len(monthly)} months."


def calculate_purchase_affordability(df, target_price, months_until_purchase=1):
    if df.empty:
        return None

    avg_monthly = df['price'].sum() / max(len(df.groupby(df['date'].dt.to_period('M'))), 1)
    avg_monthly = round(avg_monthly, 2)
    monthly_needed = round(target_price / months_until_purchase, 2)
    monthly_surplus = round(avg_monthly - (target_price / months_until_purchase), 2)

    return {
        "target_price": target_price,
        "months": months_until_purchase,
        "avg_monthly_spend": avg_monthly,
        "monthly_needed_to_save": monthly_needed,
        "monthly_surplus": monthly_surplus,
        "is_affordable": monthly_surplus >= 0,
        "total_available_months": round(target_price / avg_monthly, 1) if avg_monthly > 0 else float('inf'),
    }

