"""
predict.py — load the saved model.joblib and predict on new sample input.
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


def predict_samples(model, samples: pd.DataFrame):
    samples = samples.copy()
    samples["rooms_per_household"] = samples["total_rooms"] / samples["households"]
    samples["bedrooms_per_room"] = samples["total_bedrooms"] / samples["total_rooms"]
    samples["population_per_household"] = samples["population"] / samples["households"]
    return model.predict(samples)


if __name__ == "__main__":
    model = load_model()

    # Two real example houses (not from the training set) to predict on.
    sample_houses = pd.DataFrame([
        {
            "longitude": -122.25, "latitude": 37.85, "housing_median_age": 30.0,
            "total_rooms": 2500.0, "total_bedrooms": 450.0, "population": 900.0,
            "households": 420.0, "median_income": 5.2, "ocean_proximity": "NEAR BAY",
        },
        {
            "longitude": -119.5, "latitude": 36.6, "housing_median_age": 15.0,
            "total_rooms": 1800.0, "total_bedrooms": 350.0, "population": 800.0,
            "households": 300.0, "median_income": 2.8, "ocean_proximity": "INLAND",
        },
    ])

    preds = predict_samples(model, sample_houses)
    for i, p in enumerate(preds):
        print(f"House {i+1}: predicted median house value = ${p:,.2f}")
