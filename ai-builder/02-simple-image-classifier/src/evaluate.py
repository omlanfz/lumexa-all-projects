"""
evaluate.py
Lumexa Simple Image Classifier - Model Evaluation

Loads the trained model and reports test-set accuracy and loss, plus a
per-digit breakdown of classification performance.

Run with:
    python3 src/evaluate.py
"""

import os

import numpy as np
from tensorflow import keras

try:
    from data_loader import load_mnist_data
except ImportError:
    from src.data_loader import load_mnist_data

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "mnist_cnn.keras")


def load_trained_model(path=MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No trained model found at {path}. Run 'python3 src/train.py' first."
        )
    return keras.models.load_model(path)


def per_class_accuracy(y_true, y_pred, num_classes=10):
    """Returns a dict mapping each digit (0-9) to its classification accuracy."""
    results = {}
    for digit in range(num_classes):
        mask = y_true == digit
        total = mask.sum()
        if total == 0:
            results[digit] = None
            continue
        correct = (y_pred[mask] == digit).sum()
        results[digit] = correct / total
    return results


def main():
    print("Loading test data...")
    (_, _), (X_test, y_test) = load_mnist_data()

    print("Loading trained model...")
    model = load_trained_model()

    print("\nEvaluating on test set...")
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"  Test loss: {test_loss:.4f}")
    print(f"  Test accuracy: {test_accuracy:.4f} ({test_accuracy * 100:.1f}%)")

    print("\nComputing per-digit accuracy...")
    probabilities = model.predict(X_test, verbose=0)
    predicted_labels = np.argmax(probabilities, axis=1)

    class_accuracies = per_class_accuracy(y_test, predicted_labels)
    print(f"\n{'Digit':<8}{'Accuracy':>12}{'Test Count':>14}")
    for digit, accuracy in class_accuracies.items():
        count = int((y_test == digit).sum())
        if accuracy is None:
            print(f"{digit:<8}{'N/A':>12}{count:>14}")
        else:
            print(f"{digit:<8}{accuracy * 100:>11.1f}%{count:>14}")

    misclassified = int((predicted_labels != y_test).sum())
    print(f"\nTotal misclassified images: {misclassified} out of {len(y_test)}")


if __name__ == "__main__":
    main()
