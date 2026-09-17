"""
model.py
Lumexa Simple Image Classifier - CNN Model Definition

Defines a small, laptop-friendly convolutional neural network for
classifying 28x28 grayscale digit images into 10 classes (0-9).
"""

from tensorflow import keras
from tensorflow.keras import layers

try:
    from data_loader import IMAGE_SHAPE, NUM_CLASSES
except ImportError:
    from src.data_loader import IMAGE_SHAPE, NUM_CLASSES


def build_model(input_shape=IMAGE_SHAPE, num_classes=NUM_CLASSES):
    """Builds and compiles a small CNN for digit classification.

    Architecture:
        Conv2D(16) -> MaxPooling -> Conv2D(32) -> MaxPooling ->
        Flatten -> Dense(64) -> Dropout -> Dense(num_classes, softmax)
    """
    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Conv2D(16, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dense(64, activation="relu"),
            layers.Dropout(0.3),
            layers.Dense(num_classes, activation="softmax"),
        ],
        name="lumexa_digit_classifier",
    )

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


if __name__ == "__main__":
    model = build_model()
    model.summary()
