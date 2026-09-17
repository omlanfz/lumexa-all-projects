"""
train.py — Customer Churn Predictor (Project 08)
Data: IBM Telco Customer Churn dataset from
https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv

Pipeline: load -> clean (fix blank TotalCharges) -> feature engineer ->
encode categoricals -> split -> train (Logistic Regression + Random Forest
+ XGBoost) -> evaluate -> tune -> save best model with joblib.
"""
import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                              precision_score, recall_score)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(HERE, "data", "Telco-Customer-Churn.csv")
MODEL_PATH = os.path.join(HERE, "models", "model.joblib")
METRICS_PATH = os.path.join(HERE, "models", "metrics.json")


def load_and_clean():
    df = pd.read_csv(DATA_PATH)

    # Real quirk: TotalCharges is stored as a string and has 11 blank " "
    # values for customers with tenure == 0 (brand-new customers). Coerce to
    # numeric and fill those with 0.0 (no charges billed yet).
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(0.0)

    df = df.drop(columns=["customerID"])
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    return df


def engineer_features(df):
    df = df.copy()
    df["avg_monthly_spend"] = df["TotalCharges"] / df["tenure"].replace(0, 1)
    df["tenure_years"] = df["tenure"] / 12.0
    return df


def build_pipeline(numeric_features, categorical_features, model):
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ])
    return Pipeline([("preprocess", preprocessor), ("model", model)])


def evaluate(name, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred).tolist()
    print(f"[{name}] Acc={acc:.4f} Prec={prec:.4f} Rec={rec:.4f} F1={f1:.4f}")
    print(f"  Confusion matrix: {cm}")
    return {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "confusion_matrix": cm}


def main():
    df = load_and_clean()
    df = engineer_features(df)

    target = "Churn"
    y = df[target]
    X = df.drop(columns=[target])

    categorical_features = [
        c for c in X.columns
        if X[c].dtype == object or pd.api.types.is_string_dtype(X[c])
    ]
    numeric_features = [c for c in X.columns if c not in categorical_features]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    results = {}
    candidates = {}

    # --- Logistic Regression baseline ---
    log_pipeline = build_pipeline(
        numeric_features, categorical_features,
        LogisticRegression(max_iter=2000, random_state=42),
    )
    log_pipeline.fit(X_train, y_train)
    log_pred = log_pipeline.predict(X_test)
    results["logistic_regression"] = evaluate("LogisticRegression", y_test, log_pred)
    candidates["logistic_regression"] = log_pipeline

    # --- Random Forest ---
    rf_pipeline = build_pipeline(
        numeric_features, categorical_features,
        RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1),
    )
    rf_pipeline.fit(X_train, y_train)
    rf_pred = rf_pipeline.predict(X_test)
    results["random_forest"] = evaluate("RandomForest", y_test, rf_pred)
    candidates["random_forest"] = rf_pipeline

    # --- XGBoost ---
    xgb_pipeline = build_pipeline(
        numeric_features, categorical_features,
        XGBClassifier(
            n_estimators=300, max_depth=4, learning_rate=0.05,
            eval_metric="logloss", random_state=42, n_jobs=-1,
        ),
    )
    xgb_pipeline.fit(X_train, y_train)
    xgb_pred = xgb_pipeline.predict(X_test)
    results["xgboost"] = evaluate("XGBoost (untuned)", y_test, xgb_pred)
    candidates["xgboost"] = xgb_pipeline

    # --- Tune XGBoost with GridSearchCV (small grid) ---
    param_grid = {
        "model__max_depth": [3, 4, 6],
        "model__n_estimators": [200, 300],
        "model__learning_rate": [0.03, 0.1],
    }
    search = GridSearchCV(
        xgb_pipeline, param_grid=param_grid, cv=3, scoring="f1", n_jobs=-1
    )
    search.fit(X_train, y_train)
    best_xgb = search.best_estimator_
    best_pred = best_xgb.predict(X_test)
    results["xgboost_tuned"] = evaluate("XGBoost (tuned)", y_test, best_pred)
    results["xgboost_tuned"]["best_params"] = search.best_params_
    candidates["xgboost_tuned"] = best_xgb
    print("Best params:", search.best_params_)

    best_name = max(results, key=lambda k: results[k]["f1"])
    best_model = candidates[best_name]
    print(f"\nBest model: {best_name} (F1={results[best_name]['f1']:.4f})")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({
        "model": best_model,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "best_model_name": best_name,
    }, MODEL_PATH)

    with open(METRICS_PATH, "w") as f:
        json.dump({"best_model": best_name, "results": results}, f, indent=2, default=str)

    print(f"\nSaved best model ({best_name}) to {MODEL_PATH}")


if __name__ == "__main__":
    main()
