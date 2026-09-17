"""
evaluate.py
Lumexa Number Prediction Model - Model Evaluation

Loads the trained model (from models/model.joblib) and reports honest
performance metrics (MSE and R^2) on both the training and test sets,
flagging possible overfitting or underfitting.

Run with:
    python3 src/evaluate.py
"""

import os

import joblib
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

try:
    from data_prep import prepare_train_test_data
except ImportError:
    from src.data_prep import prepare_train_test_data

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.joblib")

TEST_SIZE = 0.2
RANDOM_SEED = 42

OVERFIT_GAP_THRESHOLD = 0.15
GOOD_FIT_R2_THRESHOLD = 0.6


def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No trained model found at {path}. Run 'python3 src/train.py' first."
        )
    return joblib.load(path)


def evaluate_model(model, X_train, X_test, y_train, y_test):
    """Computes MSE and R^2 for both training and test sets."""
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    train_mse = mean_squared_error(y_train, train_predictions)
    test_mse = mean_squared_error(y_test, test_predictions)
    train_r2 = r2_score(y_train, train_predictions)
    test_r2 = r2_score(y_test, test_predictions)

    return {
        "train_mse": train_mse,
        "test_mse": test_mse,
        "train_rmse": np.sqrt(train_mse),
        "test_rmse": np.sqrt(test_mse),
        "train_r2": train_r2,
        "test_r2": test_r2,
    }


def interpret_results(metrics):
    """Returns a plain-language verdict string based on the metrics."""
    gap = metrics["train_r2"] - metrics["test_r2"]

    if metrics["test_r2"] >= GOOD_FIT_R2_THRESHOLD and gap < OVERFIT_GAP_THRESHOLD:
        return "GOOD FIT: The model generalizes well to unseen data."
    elif gap >= OVERFIT_GAP_THRESHOLD:
        return ("POSSIBLE OVERFITTING: Training performance is notably "
                "better than test performance.")
    else:
        return ("POSSIBLE UNDERFITTING: The model is not capturing the "
                "pattern well, even on training data.")


def main():
    model = load_model()
    X_train, X_test, y_train, y_test = prepare_train_test_data(
        test_size=TEST_SIZE, seed=RANDOM_SEED
    )

    metrics = evaluate_model(model, X_train, X_test, y_train, y_test)
    verdict = interpret_results(metrics)

    print("=" * 60)
    print("MODEL EVALUATION REPORT")
    print("=" * 60)
    print(f"Training set size: {len(X_train)}  |  Test set size: {len(X_test)}")
    print()
    print(f"{'Metric':<15}{'Training':>15}{'Test':>15}")
    print(f"{'MSE':<15}{metrics['train_mse']:>15.2f}{metrics['test_mse']:>15.2f}")
    print(f"{'RMSE':<15}{metrics['train_rmse']:>15.2f}{metrics['test_rmse']:>15.2f}")
    print(f"{'R^2':<15}{metrics['train_r2']:>15.3f}{metrics['test_r2']:>15.3f}")
    print()
    print(f"R^2 gap (train - test): {metrics['train_r2'] - metrics['test_r2']:.3f}")
    print()
    print(verdict)
    print("=" * 60)


if __name__ == "__main__":
    main()
