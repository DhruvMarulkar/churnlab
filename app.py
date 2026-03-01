import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIG
# -----------------------------
API_URL = "http://127.0.0.1:8000/predict/batch"

st.set_page_config(page_title="Customer Churn Prediction", layout="wide")

# -----------------------------
# UI HEADER
# -----------------------------
st.title("📉 Customer Churn Prediction System")
st.write("Predict churn risk and visualize business impact")

# -----------------------------
# INPUT FORM
# -----------------------------
st.subheader("🔍 Customer Details")

col1, col2 = st.columns(2)

with col1:
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
    monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=75.9)

with col2:
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    payment = st.selectbox("Payment Method", ["Electronic check", "Credit card", "Bank transfer"])
    tech_support = st.selectbox("Tech Support", ["Yes", "No"])

# -----------------------------
# ENCODING (MATCH TRAINING)
# -----------------------------
contract_month = 1 if contract == "Month-to-month" else 0
payment_elec = 1 if payment == "Electronic check" else 0
tech_no = 1 if tech_support == "No" else 0

# -----------------------------
# PREDICT BUTTON
# -----------------------------
if st.button("🔮 Predict Churn"):
    payload = {
        "data": [
            {
                "tenure": tenure,
                "MonthlyCharges": monthly_charges,
                "Contract_Month-to-month": contract_month,
                "PaymentMethod_Electronic check": payment_elec,
                "TechSupport_No": tech_no
            }
        ]
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()["results"][0]

            prob = result["probability"]
            risk = result["risk"]
            revenue = result["annual_at_risk"]
            strategy = result["best_strategy"]

            # -----------------------------
            # RESULTS
            # -----------------------------
            st.success("✅ Prediction Successful")

            c1, c2, c3 = st.columns(3)
            c1.metric("Churn Probability", f"{prob:.2%}")
            c2.metric("Risk Level", risk)
            c3.metric("Annual Revenue at Risk", f"₹ {revenue:,.2f}")

            st.subheader("🎯 Recommended Strategy")
            st.info(strategy)

            # -----------------------------
            # CHARTS
            # -----------------------------
            st.subheader("📊 Visual Insights")

            chart_df = pd.DataFrame({
                "Metric": ["Churn Probability", "Retention Confidence"],
                "Value": [prob, 1 - prob]
            })

            fig = px.bar(
                chart_df,
                x="Metric",
                y="Value",
                text="Value",
                color="Metric",
                title="Churn Risk Breakdown"
            )

            fig.update_traces(texttemplate='%{text:.2%}', textposition='outside')
            fig.update_layout(yaxis_tickformat=".0%", showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("❌ API Error")
            st.code(response.text)

    except Exception as e:
        st.error("⚠️ Unable to connect to API")
        st.code(str(e))