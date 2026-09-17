"""
train.py
Lumexa Simple Image Classifier - Model Training

Loads MNIST, builds the CNN, trains it for a small number of epochs, and
saves the trained model to models/mnist_cnn.keras.

Run with:
    python3 src/train.py
"""

import os

try:
    from data_loader import load_mnist_data
    from model import build_model
except ImportError:
    from src.data_loader import load_mnist_data
    from src.model import build_model

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "mnist_cnn.keras")

EPOCHS = 5
BATCH_SIZE = 64
VALIDATION_SPLIT = 0.1
RANDOM_SEED = 42


def main():
    print("Loading and preprocessing MNIST data...")
    (X_train, y_train), (X_test, y_test) = load_mnist_data()
    print(f"  Training images: {X_train.shape[0]}")
    print(f"  Test images: {X_test.shape[0]}")

    print("\nBuilding model...")
    model = build_model()
    model.summary()

    print(f"\nTraining for {EPOCHS} epochs (batch size {BATCH_SIZE})...")
    history = model.fit(
        X_train,
        y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=VALIDATION_SPLIT,
        verbose=2,
    )

    final_train_acc = history.history["accuracy"][-1]
    final_val_acc = history.history["val_accuracy"][-1]
    print(f"\nFinal training accuracy: {final_train_acc:.4f}")
    print(f"Final validation accuracy: {final_val_acc:.4f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save(MODEL_PATH)
    print(f"\nModel saved to: {os.path.abspath(MODEL_PATH)}")


if __name__ == "__main__":
    main()
