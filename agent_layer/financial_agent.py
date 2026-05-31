def financial_agent(
    category_name,
    predicted_spending,
    monthly_budget,
    monthly_df
):

    category_data = monthly_df[
        monthly_df["category"] == category_name
    ]

    historical_avg = category_data["amount"].mean()

    volatility = (
        category_data["amount"].std() /
        historical_avg
        if historical_avg > 0
        else 0
    )

    difference = predicted_spending - monthly_budget

    if difference > 0:
        status = "Financial Attention Required"
    else:
        status = "Healthy"

    if volatility > 0.50:
        risk_level = "High"
    elif volatility > 0.25:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    reasoning_trace = [
        "Analyzed predicted spending.",
        "Compared spending against budget.",
        "Evaluated historical volatility.",
        f"Determined risk level: {risk_level}.",
        f"Final status: {status}."
    ]

    recommendations = []

    if difference > 0:
        recommendations.append(
            f"Your projected {category_name} spending exceeds the budget by ₹{difference:.2f}. Consider reducing discretionary purchases."
        )

    if volatility > 0.50:
        recommendations.append(
            f"Historical spending in {category_name} is highly volatile. Monitor expenses weekly to avoid sudden spikes."
        )

    if historical_avg > monthly_budget:
        recommendations.append(
            f"Average {category_name} spending is already above your budget. Consider increasing the budget or reducing expenses."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Current spending pattern appears healthy."
        )

    return {
        "overall_status": status,

        "forecast": {
            "predicted_spending": float(predicted_spending),
            "budget": monthly_budget,
            "difference": float(difference)
        },

        "risk_analysis": {
            "risk_level": risk_level,
            "historical_avg": round(historical_avg, 2),
            "volatility": round(volatility, 2)
        },

        "reasoning_trace": reasoning_trace,

        "recommendations": recommendations
    }