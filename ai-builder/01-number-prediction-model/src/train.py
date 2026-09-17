"""
train.py
Lumexa Number Prediction Model - Model Training

Trains a LinearRegression model on the prepared training data and saves
the trained model to models/model.joblib for later evaluation and
inference.

Run with:
    python3 src/train.py
"""

import os

import joblib
from sklearn.linear_model import LinearRegression

# Support running as `python3 src/train.py` (script) or as a package import.
try:
    from data_prep import prepare_train_test_data
except ImportError:
    from src.data_prep import prepare_train_test_data

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

TEST_SIZE = 0.2
RANDOM_SEED = 42


def train_model():
    """Trains a LinearRegression model and returns it along with the
    train/test split used, so evaluate.py can reuse the exact same split.
    """
    X_train, X_test, y_train, y_test = prepare_train_test_data(
        test_size=TEST_SIZE, seed=RANDOM_SEED
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_train, X_test, y_train, y_test


def save_model(model, path=MODEL_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)


def main():
    model, X_train, X_test, y_train, y_test = train_model()

    print("Model trained successfully.")
    print(f"  Learned slope (coefficient): {model.coef_[0]:.4f}")
    print(f"  Learned intercept: {model.intercept_:.4f}")
    print(f"  Formula: test_score = {model.intercept_:.2f} + "
          f"{model.coef_[0]:.2f} * hours_studied")
    print(f"  Trained on {len(X_train)} samples, held out {len(X_test)} for testing.")

    save_model(model)
    print(f"Model saved to: {os.path.abspath(MODEL_PATH)}")


if __name__ == "__main__":
    main()
