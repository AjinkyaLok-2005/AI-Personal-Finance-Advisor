import numpy as np

class FinancialAgent:
    def __init__(self, monthly_df):
        self.monthly_df = monthly_df
        self.goal = "Evaluate overall financial health and detect risk."

    def _analyze_forecast(self, category_name, predicted_spending, budget):

        difference = predicted_spending - budget

        if difference > 0:
            return {
                "budget_status": "Overspending Risk",
                "difference": float(round(difference, 2))
            }
        else:
            return {
                "budget_status": "Within Budget",
                "difference": float(round(difference, 2))
            }
        
    def _analyze_volatility(self, category_name):

        category_data = self.monthly_df[
            self.monthly_df["category"] == category_name
            ]["amount"]
        
        historical_mean = np.mean(category_data)
        historical_std = np.std(category_data)

        volatility_ratio = (
            historical_std / historical_mean if historical_mean != 0 else 0
        )

        if volatility_ratio > 0.5:
            risk_level = "High"
        elif volatility_ratio > 0.2:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        return {
            "risk_level": risk_level,
            "historical_avg": float(round(historical_mean, 2)),
            "volatility": float(round(volatility_ratio, 2))
        }
    
    def evaluate(self, category_name, predicted_spending, monthly_budget):

        reasoning_log = []
        reasoning_log.append(f"Goal: {self.goal}")

        forecast_result = self._analyze_forecast(category_name, predicted_spending, monthly_budget)

        reasoning_log.append(f"Forecast analysis complete. Budget status: {forecast_result['budget_status']}.")

        volatility_result = self._analyze_volatility(category_name)

        reasoning_log.append(f"Volatility analysis complete. Risk level: {volatility_result['risk_level']}.")

        if forecast_result["budget_status"] == "Overspending Risk":
            if volatility_result["risk_level"] in ["High", "Moderate"]:
                overall_status = "Financial Attention Required"
            else:
                overall_status = "Monitor Spending Closely"
        else:
            overall_status = "Financially Stable" 

        reasoning_log.append(f"Final Decision: {overall_status}")

        return {
            "overall_status": overall_status,
            "forecast": {
                "predicted_spending": float(round(predicted_spending, 2)),
                "budget": monthly_budget,
                "difference": forecast_result["difference"],
                "status": forecast_result["budget_status"]
            },
            "risk_analysis": volatility_result,
            "reasoning_trace": reasoning_log
        }