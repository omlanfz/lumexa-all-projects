"""
api.py — Flask API that serves the trained house-price model.

Run:
    python3 api.py
Then POST JSON to http://127.0.0.1:5000/predict

Example request body:
{
  "longitude": -122.25, "latitude": 37.85, "housing_median_age": 30.0,
  "total_rooms": 2500.0, "total_bedrooms": 450.0, "population": 900.0,
  "households": 420.0, "median_income": 5.2, "ocean_proximity": "NEAR BAY"
}
"""
import os

import joblib
import pandas as pd
from flask import Flask, jsonify, request

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(HERE, "models", "model.joblib")

app = Flask(__name__)

_bundle = joblib.load(MODEL_PATH)
MODEL = _bundle["model"]

REQUIRED_FIELDS = [
    "longitude", "latitude", "housing_median_age", "total_rooms",
    "total_bedrooms", "population", "households", "median_income",
    "ocean_proximity",
]

VALID_OCEAN_PROXIMITY = {"<1H OCEAN", "INLAND", "NEAR OCEAN", "NEAR BAY", "ISLAND"}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": _bundle.get("best_model_name")})


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    missing = [f for f in REQUIRED_FIELDS if f not in payload]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    if payload["ocean_proximity"] not in VALID_OCEAN_PROXIMITY:
        return jsonify({
            "error": f"ocean_proximity must be one of {sorted(VALID_OCEAN_PROXIMITY)}"
        }), 400

    try:
        row = {f: payload[f] for f in REQUIRED_FIELDS}
        df = pd.DataFrame([row])
        df["rooms_per_household"] = df["total_rooms"] / df["households"]
        df["bedrooms_per_room"] = df["total_bedrooms"] / df["total_rooms"]
        df["population_per_household"] = df["population"] / df["households"]
        prediction = float(MODEL.predict(df)[0])
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"Prediction failed: {exc}"}), 400

    return jsonify({
        "predicted_median_house_value": round(prediction, 2),
        "model": _bundle.get("best_model_name"),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
