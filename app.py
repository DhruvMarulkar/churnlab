import streamlit as st
import requests
import plotly.graph_objects as go


st.set_page_config(
    page_title="ChurnLab - Customer Risk Intelligence",
    page_icon="📊",
    layout="wide"
)


# API URL 

API_URL = "https://churnlab.onrender.com/predict/batch"


st.title("📊 ChurnLab")
st.subheader("Customer Churn Risk & Revenue Intelligence System")

st.markdown("""
Analyze churn probability, estimate annual revenue at risk, 
and receive actionable retention strategies.
""")

st.divider()


st.markdown("## 🧾 Customer Profile")

col1, col2 = st.columns(2)

with col1:
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=72, value=12)
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.0)
    contract_type = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

with col2:
    tech_support = st.selectbox("Tech Support", ["Yes", "No"])
    payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])



contract_month = 1 if contract_type == "Month-to-month" else 0
tech_no = 1 if tech_support == "No" else 0
payment_elec = 1 if payment_method == "Electronic check" else 0


if st.button("🔍 Analyze Churn Risk", use_container_width=True):

    payload = {
        "data": [{
            "tenure": tenure,
            "MonthlyCharges": monthly_charges,
            "Contract_Month-to-month": contract_month,
            "TechSupport_No": tech_no,
            "PaymentMethod_Electronic check": payment_elec
        }]
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code != 200:
            st.error("API Error. Please check if backend is running.")
        else:
            result = response.json()["results"][0]

            st.divider()
            st.markdown("## 📈 Risk Analysis Results")

           
            risk = result["risk"]

            if risk == "High":
                st.error(f"⚠️ HIGH RISK CUSTOMER")
            elif risk == "Medium":
                st.warning(f"⚠️ MEDIUM RISK CUSTOMER")
            else:
                st.success(f"✅ LOW RISK CUSTOMER")

            col1, col2, col3 = st.columns(3)

            col1.metric("Churn Probability", f"{result['probability']*100:.2f}%")
            col2.metric("Annual Revenue at Risk", f"${result['annual_at_risk']}")
            col3.metric("Best Strategy", result["best_strategy"])

           
            prob = result["probability"] * 100

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob,
                title={'text': "Churn Probability (%)"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'steps': [
                        {'range': [0, 40], 'color': "green"},
                        {'range': [40, 70], 'color': "orange"},
                        {'range': [70, 100], 'color': "red"}
                    ],
                }
            ))

            st.plotly_chart(fig, use_container_width=True)


            st.markdown("### 📌 Recommended Retention Actions")

            for action in result["recommendations"]:
                st.markdown(f"- {action}")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")


st.divider()
st.markdown("Built with FastAPI, XGBoost & Streamlit | ChurnLab Intelligence System")