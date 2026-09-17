"""
predict.py
Lumexa Simple Image Classifier - Inference Script

Loads the trained model, classifies a single image from the MNIST test
set (selected by index), prints the predicted digit and confidence, and
saves a labeled image showing the digit alongside the prediction.

Run with:
    python3 src/predict.py --index 0
    python3 src/predict.py --index 123
"""

import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras

try:
    from data_loader import load_mnist_data
except ImportError:
    from src.data_loader import load_mnist_data

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "mnist_cnn.keras")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")


def load_trained_model(path=MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No trained model found at {path}. Run 'python3 src/train.py' first."
        )
    return keras.models.load_model(path)


def predict_single_image(model, image):
    """Given a single preprocessed image (shape (28, 28, 1)), returns the
    predicted digit and the model's confidence (probability) for it.
    """
    batch = np.expand_dims(image, axis=0)  # model expects a batch dimension
    probabilities = model.predict(batch, verbose=0)[0]
    predicted_digit = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_digit])
    return predicted_digit, confidence, probabilities


def save_prediction_image(image, true_label, predicted_digit, confidence, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(4, 4))
    plt.imshow(image.squeeze(), cmap="gray")
    plt.title(
        f"True: {true_label}  |  Predicted: {predicted_digit} "
        f"({confidence * 100:.1f}% confident)"
    )
    plt.axis("off")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Classify a single MNIST test-set image using the trained "
                     "Lumexa Simple Image Classifier."
    )
    parser.add_argument(
        "--index",
        type=int,
        default=0,
        help="Index of the test-set image to classify (0-9999). Default: 0",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("Loading test data...")
    (_, _), (X_test, y_test) = load_mnist_data()

    if not (0 <= args.index < len(X_test)):
        raise ValueError(
            f"--index must be between 0 and {len(X_test) - 1}, got {args.index}"
        )

    print("Loading trained model...")
    model = load_trained_model()

    image = X_test[args.index]
    true_label = int(y_test[args.index])

    predicted_digit, confidence, probabilities = predict_single_image(model, image)

    print("\nLumexa Simple Image Classifier - Inference")
    print("-" * 50)
    print(f"  Image index: {args.index}")
    print(f"  True label: {true_label}")
    print(f"  Predicted digit: {predicted_digit}")
    print(f"  Confidence: {confidence * 100:.1f}%")
    print(f"  Correct: {'YES' if predicted_digit == true_label else 'NO'}")
    print("-" * 50)
    print("  Full probability breakdown:")
    for digit, probability in enumerate(probabilities):
        print(f"    digit {digit}: {probability * 100:5.1f}%")

    output_path = os.path.join(OUTPUT_DIR, f"prediction_index_{args.index}.png")
    save_prediction_image(image, true_label, predicted_digit, confidence, output_path)
    print(f"\nLabeled image saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
