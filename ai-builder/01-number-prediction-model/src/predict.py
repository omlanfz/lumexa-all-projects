"""
predict.py
Lumexa Number Prediction Model - Inference Script

Loads the trained model and predicts a test score for one or more new
"hours studied" values passed on the command line.

Run with:
    python3 src/predict.py --hours 6.5
    python3 src/predict.py --hours 2 4 6 8 10
"""

import argparse
import os

import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.joblib")


def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No trained model found at {path}. Run 'python3 src/train.py' first."
        )
    return joblib.load(path)


def predict_scores(model, hours_list):
    """Given a list of hours-studied values, returns predicted test scores.

    Predictions are clipped to the realistic 0-100 range, since the raw
    linear model can otherwise extrapolate beyond a valid test score.
    """
    X_new = np.array(hours_list).reshape(-1, 1)
    raw_predictions = model.predict(X_new)
    clipped_predictions = np.clip(raw_predictions, 0, 100)
    return raw_predictions, clipped_predictions


def parse_args():
    parser = argparse.ArgumentParser(
        description="Predict a test score from hours studied using the trained "
                     "Lumexa Number Prediction Model."
    )
    parser.add_argument(
        "--hours",
        type=float,
        nargs="+",
        required=True,
        help="One or more hours-studied values to predict scores for, e.g. --hours 3 6.5 10",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    model = load_model()

    raw_predictions, clipped_predictions = predict_scores(model, args.hours)

    print("Lumexa Number Prediction Model - Inference")
    print("-" * 50)
    for hours, raw, clipped in zip(args.hours, raw_predictions, clipped_predictions):
        note = "" if abs(raw - clipped) < 0.01 else "  (clipped to valid 0-100 range)"
        print(f"  Hours studied: {hours:>5.1f}  ->  Predicted score: {clipped:6.1f}{note}")
    print("-" * 50)


if __name__ == "__main__":
    main()
