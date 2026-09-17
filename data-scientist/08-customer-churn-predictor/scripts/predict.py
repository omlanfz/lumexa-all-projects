"""
predict.py — load the saved churn model and predict on new sample customers.
Run: python3 scripts/predict.py
"""
import os

import joblib
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(HERE, "models", "model.joblib")


def load_model():
    bundle = joblib.load(MODEL_PATH)
    return bundle["model"]


def engineer_features(df):
    df = df.copy()
    df["avg_monthly_spend"] = df["TotalCharges"] / df["tenure"].replace(0, 1)
    df["tenure_years"] = df["tenure"] / 12.0
    return df


if __name__ == "__main__":
    model = load_model()

    sample_customers = pd.DataFrame([
        {
            "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
            "tenure": 2, "PhoneService": "Yes", "MultipleLines": "No",
            "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
            "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
            "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check", "MonthlyCharges": 85.0, "TotalCharges": 170.0,
        },
        {
            "gender": "Male", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "Yes",
            "tenure": 60, "PhoneService": "Yes", "MultipleLines": "Yes",
            "InternetService": "DSL", "OnlineSecurity": "Yes", "OnlineBackup": "Yes",
            "DeviceProtection": "Yes", "TechSupport": "Yes", "StreamingTV": "Yes",
            "StreamingMovies": "Yes", "Contract": "Two year", "PaperlessBilling": "No",
            "PaymentMethod": "Bank transfer (automatic)", "MonthlyCharges": 65.0,
            "TotalCharges": 3900.0,
        },
    ])

    features = engineer_features(sample_customers)
    preds = model.predict(features)
    probs = model.predict_proba(features)[:, 1]
    for i, (pred, prob) in enumerate(zip(preds, probs)):
        label = "WILL CHURN" if pred == 1 else "will stay"
        print(f"Customer {i+1}: {label}  (churn probability = {prob:.2%})")
