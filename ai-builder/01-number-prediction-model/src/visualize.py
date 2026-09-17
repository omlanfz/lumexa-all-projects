"""
visualize.py
Lumexa Number Prediction Model - Results Visualization

Loads the trained model and produces a labeled scatter plot showing
training data, test data, and the model's prediction line, saved to
outputs/results_chart.png.

Run with:
    python3 src/visualize.py
"""

import os

import joblib
import matplotlib
matplotlib.use("Agg")  # Ensures the script works in headless/no-display environments
import matplotlib.pyplot as plt
import numpy as np

try:
    from data_prep import prepare_train_test_data
except ImportError:
    from src.data_prep import prepare_train_test_data

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.joblib")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
CHART_PATH = os.path.join(OUTPUT_DIR, "results_chart.png")

TEST_SIZE = 0.2
RANDOM_SEED = 42


def build_chart(model, X_train, X_test, y_train, y_test, output_path=CHART_PATH):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    test_predictions = model.predict(X_test)

    # Sort test points by X so the prediction line draws cleanly left-to-right.
    sort_order = np.argsort(X_test.flatten())
    X_test_sorted = X_test[sort_order]
    predictions_sorted = test_predictions[sort_order]

    plt.figure(figsize=(9, 6))
    plt.scatter(X_train, y_train, color="lightgray", label="Training data", alpha=0.7)
    plt.scatter(X_test, y_test, color="steelblue", label="Test data (actual)", s=55)
    plt.plot(X_test_sorted, predictions_sorted, color="darkorange", linewidth=2.5,
              label="Model prediction")

    plt.xlabel("Hours Studied")
    plt.ylabel("Test Score")
    plt.title("Lumexa Number Prediction Model: Study Hours vs. Test Score")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 105)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    return output_path


def main():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"No trained model found at {MODEL_PATH}. Run 'python3 src/train.py' first."
        )
    model = joblib.load(MODEL_PATH)

    X_train, X_test, y_train, y_test = prepare_train_test_data(
        test_size=TEST_SIZE, seed=RANDOM_SEED
    )

    chart_path = build_chart(model, X_train, X_test, y_train, y_test)
    print(f"Chart saved to: {os.path.abspath(chart_path)}")


if __name__ == "__main__":
    main()
