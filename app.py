import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go


st.set_page_config(
    page_title="ChurnLab - Customer Risk Intelligence",
    page_icon="📊",
    layout="wide"
)



@st.cache_resource
def load_model():
    return joblib.load("model/churn_model.pkl")

model = load_model()


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

    input_data = np.array([[

        tenure,
        monthly_charges,
        contract_month,
        tech_no,
        payment_elec

    ]])

    prob = model.predict_proba(input_data)[0][1]

    churn_probability = prob * 100

    annual_at_risk = monthly_charges * 12 * prob


    if churn_probability > 70:
        risk = "High"
        strategy = "Offer retention discount"
    elif churn_probability > 40:
        risk = "Medium"
        strategy = "Upsell add-ons"
    else:
        risk = "Low"
        strategy = "Maintain rewards"


    st.divider()
    st.markdown("## 📈 Risk Analysis Results")

    if risk == "High":
        st.error("⚠️ HIGH RISK CUSTOMER")
    elif risk == "Medium":
        st.warning("⚠️ MEDIUM RISK CUSTOMER")
    else:
        st.success("✅ LOW RISK CUSTOMER")

    col1, col2, col3 = st.columns(3)

    col1.metric("Churn Probability", f"{churn_probability:.2f}%")
    col2.metric("Annual Revenue at Risk", f"${annual_at_risk:.2f}")
    col3.metric("Best Strategy", strategy)


    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=churn_probability,
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


st.divider()
st.markdown("Built with XGBoost & Streamlit | ChurnLab Intelligence System")
