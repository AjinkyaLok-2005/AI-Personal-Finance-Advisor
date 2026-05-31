import streamlit as st

from utils.data_loader import load_kaggle_dataset
from ml_layer.feature_engineering import create_features

from dl_layer.preprocessing import aggregate_monthly
from dl_layer.sequence_builder import prepare_lstm_data
from dl_layer.lstm_model import load_lstm_model
from dl_layer.lstm_model import predict_next_month

from nlp_layer.sms_parser import parse_sms_transaction

from agent_layer.budget_agent import analyze_budget_advanced
from agent_layer.financial_agent import financial_agent




st.set_page_config(
    page_title="AI Personal Finance Advisor",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI-Powered Personal Finance Advisor")

st.markdown(
    "Predict future spending, analyze SMS transactions and receive intelligent financial recommendations."
)



df = load_kaggle_dataset("data/raw/budget_data.csv")
df = create_features(df)
monthly_df = aggregate_monthly(df)



st.sidebar.header("Prediction Settings")

category = st.sidebar.selectbox(
    "Select Category",
    monthly_df["category"].unique()
)

budget_limit = st.sidebar.number_input(
    "Monthly Budget",
    min_value=0,
    value=25
)



X, y, scaler = prepare_lstm_data(
    monthly_df,
    category_name=category
)

lstm_model = load_lstm_model()

prediction = predict_next_month(
    lstm_model,
    X,
    scaler
)



st.header("📈 Spending Forecast")

difference = prediction - budget_limit

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Predicted Spending",
        f"₹{prediction:.2f}"
    )

with col2:
    st.metric(
        "Budget",
        f"₹{budget_limit}"
    )

with col3:
    st.metric(
        "Difference",
        f"₹{difference:.2f}"
    )


budget_result = analyze_budget_advanced(
    category_name=category,
    predicted_spending=prediction,
    monthly_budget=budget_limit,
    monthly_df=monthly_df
)

st.header("💰 Budget Analysis")

if budget_result["status"] == "Safe":
    st.success(f"Status: {budget_result['status']}")
else:
    st.error(f"Status: {budget_result['status']}")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Risk Level",
        budget_result["risk_level"]
    )

with col2:
    st.metric(
        "Historical Average",
        f"₹{float(budget_result['historical_avg']):.2f}"
    )

st.info(
    budget_result["suggestion"]
)


agent_report = financial_agent(
    category_name=category,
    predicted_spending=prediction,
    monthly_budget=budget_limit,
    monthly_df=monthly_df
)

st.header("🤖 Financial Agent")

st.warning(
    f"Overall Status: {agent_report['overall_status']}"
)

risk_analysis = agent_report["risk_analysis"]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Risk Level",
        risk_analysis["risk_level"]
    )

with col2:
    st.metric(
        "Volatility",
        f"{float(risk_analysis['volatility']):.2f}"
    )

with st.expander("Agent Reasoning Process"):
    for step in agent_report["reasoning_trace"]:
        st.write("•", step)

st.subheader("Agent Recommendations")

for rec in agent_report["recommendations"]:
    st.info(rec)

st.header("📩 SMS Transaction Parser")

sms_text = st.text_area(
    "Paste Bank SMS",
    value="Rs. 540 debited from A/C XXXX1234 on 12-02-2024 at Amazon. Avl Bal: Rs. 12,450",
    height=120
)

if st.button("Parse SMS"):

    parsed_df = parse_sms_transaction(sms_text)

    st.success("Transaction Extracted Successfully")

    st.dataframe(parsed_df)


st.header("📊 Financial Insights")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Monthly Spending Trend")

    monthly_chart = (
        monthly_df.groupby("year_month")["amount"]
        .sum()
        .reset_index()
    )

    monthly_chart["year_month"] = (
        monthly_chart["year_month"]
        .astype(str)
    )

    st.line_chart(
        monthly_chart.set_index("year_month")
    )

with col2:

    st.subheader("Category-wise Spending")

    category_chart = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_chart)