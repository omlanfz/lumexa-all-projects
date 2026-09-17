"""
Train.py — House Price Predictor (Project 07)
Data: California Housing dataset (1990 census, StatLib), from
https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv

Pipeline: load -> clean -> feature engineer -> split -> train (Linear Regression
and Random Forest) -> evaluate -> tune Random Forest with RandomizedSearchCV ->
save best model with joblib.
"""
import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(HERE, "data", "housing.csv")
MODEL_PATH = os.path.join(HERE, "models", "model.joblib")
METRICS_PATH = os.path.join(HERE, "models", "metrics.json")


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def engineer_features(df):
    df = df.copy()
    # total_bedrooms has 207 missing values in the real dataset - handled by
    # the SimpleImputer in the pipeline below, not dropped, so we keep all rows.
    df["rooms_per_household"] = df["total_rooms"] / df["households"]
    df["bedrooms_per_room"] = df["total_bedrooms"] / df["total_rooms"]
    df["population_per_household"] = df["population"] / df["households"]
    return df


def build_pipeline(numeric_features, categorical_features, model):
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features),
    ])
    return Pipeline([("preprocess", preprocessor), ("model", model)])


def evaluate(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    print(f"[{name}] MAE={mae:,.2f}  MSE={mse:,.2f}  RMSE={rmse:,.2f}  R2={r2:.4f}")
    return {"MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2}


def main():
    df = load_data()
    df = engineer_features(df)

    target = "median_house_value"
    y = df[target]
    X = df.drop(columns=[target])

    categorical_features = ["ocean_proximity"]
    numeric_features = [c for c in X.columns if c not in categorical_features]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    results = {}

    # --- Linear Regression baseline ---
    lin_pipeline = build_pipeline(numeric_features, categorical_features, LinearRegression())
    lin_pipeline.fit(X_train, y_train)
    lin_pred = lin_pipeline.predict(X_test)
    results["linear_regression"] = evaluate("LinearRegression", y_test, lin_pred)

    # --- Random Forest ---
    rf_pipeline = build_pipeline(
        numeric_features, categorical_features,
        RandomForestRegressor(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1),
    )
    rf_pipeline.fit(X_train, y_train)
    rf_pred = rf_pipeline.predict(X_test)
    results["random_forest"] = evaluate("RandomForest (untuned)", y_test, rf_pred)

    # --- Tune Random Forest with RandomizedSearchCV ---
    param_dist = {
        "model__n_estimators": [100, 150, 200],
        "model__max_depth": [10, 15, 20, 25],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", "log2", None],
    }
    search = RandomizedSearchCV(
        rf_pipeline,
        param_distributions=param_dist,
        n_iter=10,
        cv=3,
        scoring="neg_mean_squared_error",
        random_state=42,
        n_jobs=-1,
    )
    search.fit(X_train, y_train)
    best_rf = search.best_estimator_
    best_pred = best_rf.predict(X_test)
    results["random_forest_tuned"] = evaluate("RandomForest (tuned)", y_test, best_pred)
    results["random_forest_tuned"]["best_params"] = search.best_params_
    print("Best params:", search.best_params_)

    # Pick best model by RMSE
    candidates = {
        "linear_regression": lin_pipeline,
        "random_forest": rf_pipeline,
        "random_forest_tuned": best_rf,
    }
    best_name = min(results, key=lambda k: results[k]["RMSE"])
    best_model = candidates[best_name]
    print(f"\nBest model: {best_name} (RMSE={results[best_name]['RMSE']:,.2f})")

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
