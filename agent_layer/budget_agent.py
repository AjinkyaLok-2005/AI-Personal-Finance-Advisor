import numpy as np

def analyze_budget_advanced(category_name, monthly_df, predicted_spending, monthly_budget):

    category_data = monthly_df[monthly_df["category"] == category_name]["amount"]

    historical_mean = np.mean(category_data)
    historical_std = np.std(category_data)

    difference = predicted_spending - monthly_budget

    voilatility_ratio = historical_std / historical_mean if historical_mean != 0 else 0

    if difference > 0:
        if voilatility_ratio > 0.5:
            risk_level = "High Voilatility Risk"
        else:
            risk_level = "Moderate Risk"

        return {
            "status": "Overspending Risk",
            "risk_level": risk_level,
            "predicted": round(predicted_spending, 2),
            "budget": monthly_budget,
            "difference": round(difference, 2),
            "historical_avg": round(historical_mean, 2),
            "voilatility": round(voilatility_ratio, 2),
            "suggestion": f"Reduce {category_name} spending or increase allocated budget."
        }
    
    return {
        "status": "Safe",
        "risk_level": "Low",
        "predicted": round(predicted_spending, 2),
        "budget": monthly_budget,
        "historical_avg": round(historical_mean, 2),
        "voilatility": round(voilatility_ratio, 2),
        "suggestion": "Spending pattern is stable."
    }