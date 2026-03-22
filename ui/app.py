import streamlit as st
import pandas as pd
import joblib

# Load model and feature order
model = joblib.load("models/lightgbm_fraud_model.pkl")
features = joblib.load("models/model_features.pkl")

st.title("Fraud Detection System")

st.write("Enter transaction details")

step = st.number_input("Step (time index)", min_value=1, value=1)
amount = st.number_input("Transaction Amount", min_value=0.0)
oldbalanceOrg = st.number_input("Old Balance (Origin)", min_value=0.0)
newbalanceOrig = st.number_input("New Balance (Origin)", min_value=0.0)
oldbalanceDest = st.number_input("Old Balance (Destination)", min_value=0.0)
newbalanceDest = st.number_input("New Balance (Destination)", min_value=0.0)

transaction_type = st.selectbox(
    "Transaction Type",
    ["CASH_IN", "CASH_OUT", "TRANSFER", "PAYMENT", "DEBIT"]
)

isFlaggedFraud = st.selectbox("System Flagged Fraud", [0,1])

# One-hot encoding
type_CASH_OUT = 1 if transaction_type == "CASH_OUT" else 0
type_TRANSFER = 1 if transaction_type == "TRANSFER" else 0
type_PAYMENT = 1 if transaction_type == "PAYMENT" else 0
type_DEBIT = 1 if transaction_type == "DEBIT" else 0

# Feature engineering
balance_diff_orig = oldbalanceOrg - newbalanceOrig
balance_diff_dest = oldbalanceDest - newbalanceDest
amount_balance_ratio_orig = amount / (balance_diff_orig + 1)
balance_error = (oldbalanceOrg - amount) - newbalanceOrig

if st.button("Predict Fraud"):

    transaction = {
        "step":step,
        "amount":amount,
        "oldbalanceOrg":oldbalanceOrg,
        "newbalanceOrig":newbalanceOrig,
        "oldbalanceDest":oldbalanceDest,
        "newbalanceDest":newbalanceDest,
        "isFlaggedFraud":isFlaggedFraud,
        "balance_diff_orig":balance_diff_orig,
        "balance_diff_dest":balance_diff_dest,
        "amount_balance_ratio_orig":amount_balance_ratio_orig,
        "balance_error":balance_error,
        "type_CASH_OUT":type_CASH_OUT,
        "type_TRANSFER":type_TRANSFER,
        "type_PAYMENT":type_PAYMENT,
        "type_DEBIT":type_DEBIT
    }


    df = pd.DataFrame([transaction])
    df = df[features]

    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    if pred == 1:
        st.error(f"Fraud Detected (probability : {prob:.4f})")
    else:
        st.success(f"Legitimate Transaction (probability: {prob:.4f})")