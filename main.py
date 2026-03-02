from utils.data_loader import load_kaggle_dataset
from ml_layer.feature_engineering import create_features
from ml_layer.train_model import train_random_forest
from dl_layer.preprocessing import aggregate_monthly
from dl_layer.sequence_builder import prepare_lstm_data
from dl_layer.lstm_model import build_and_train_lstm
from dl_layer.lstm_model import load_lstm_model
from dl_layer.lstm_model import predict_next_month
from nlp_layer.sms_parser import parse_sms_transaction
from agent_layer.budget_agent import analyze_budget_advanced
from agent_layer.financial_agent import FinancialAgent

df = load_kaggle_dataset("data/raw/budget_data.csv")

df = create_features(df)

monthly_df = aggregate_monthly(df)

model, encoder = train_random_forest(df)

# print(monthly_df["category"].unique())

# print(monthly_df.groupby("category")["year_month"].count())

X, y, scaler = prepare_lstm_data(monthly_df, category_name = "Transport")

# lstm_model = build_and_train_lstm(X, y, epochs = 50)
lstm_model = load_lstm_model()

predicted_value = predict_next_month(lstm_model, X, scaler)

budget_limit = 25

budget_analysis = analyze_budget_advanced(
    category_name = "Transport",
    monthly_df = monthly_df,
    predicted_spending = predicted_value,
    monthly_budget = budget_limit
)

sample_sms = "Rs. 540 debited from A/C XXXX1234 on 12-02-2024 at Amazon. Avl Bal: Rs. 12,450"

parsed_df = parse_sms_transaction(sample_sms)

agent = FinancialAgent(monthly_df)

financial_report = agent.evaluate(
    category_name = "Transport",
    predicted_spending = predicted_value,
    monthly_budget = 25
)

# print(monthly_df.head())

# print("X shape: ", X.shape)
# print("y shape: ", y.shape)

print("\nPredicted Next Month Transport Spending:", predicted_value)

print("\nParsed SMS Transaction:")
print(parsed_df)

print("\nBudget Analysis:")
print(budget_analysis)

print("\nFinancial Agent Report:")
print(financial_report)