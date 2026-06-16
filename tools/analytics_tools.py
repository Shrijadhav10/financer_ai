def detect_overspending(category_data, total_spend):

    alerts = []

    for category, value in category_data.items():

        pct = (value / total_spend) * 100

        if pct > 40:

            alerts.append(
                f"High spending detected in {category}: {round(pct,2)}%"
            )

    return alerts


def savings_suggestions(category_data):

    suggestions = []

    for category, value in category_data.items():

        suggested = value * 0.15

        suggestions.append(
            f"Reduce {category} by 15% → Save ₹{round(suggested,2)}"
        )

    return suggestions