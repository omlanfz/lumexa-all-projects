"""
data_loader.py
Lumexa Simple Image Classifier - Data Loading and Preprocessing

Loads the MNIST handwritten digit dataset via keras.datasets, normalizes
pixel values, and reshapes images for use with a convolutional neural
network.
"""

import numpy as np
from tensorflow import keras

# Set to an integer (e.g. 6000) to train on a smaller subset for speed while
# experimenting, or None to use the full training set (60,000 images).
SUBSET_SIZE = None

NUM_CLASSES = 10
IMAGE_SHAPE = (28, 28, 1)


def load_mnist_data(subset_size=SUBSET_SIZE):
    """Loads and preprocesses the MNIST dataset.

    Returns:
        (X_train, y_train), (X_test, y_test): preprocessed NumPy arrays.
        X arrays have shape (n, 28, 28, 1) with float pixel values in [0, 1].
        y arrays have shape (n,) with integer digit labels 0-9.
    """
    (X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

    if subset_size is not None:
        X_train = X_train[:subset_size]
        y_train = y_train[:subset_size]

    # Normalize pixel values from [0, 255] to [0.0, 1.0].
    X_train = X_train.astype("float32") / 255.0
    X_test = X_test.astype("float32") / 255.0

    # Add an explicit channel dimension: (28, 28) -> (28, 28, 1).
    # Convolutional layers expect a channel axis even for grayscale images.
    X_train = np.expand_dims(X_train, axis=-1)
    X_test = np.expand_dims(X_test, axis=-1)

    return (X_train, y_train), (X_test, y_test)


if __name__ == "__main__":
    (X_train, y_train), (X_test, y_test) = load_mnist_data()
    print(f"Training images: {X_train.shape}")
    print(f"Training labels: {y_train.shape}")
    print(f"Test images: {X_test.shape}")
    print(f"Test labels: {y_test.shape}")
    print(f"Pixel value range: [{X_train.min():.2f}, {X_train.max():.2f}]")
    print(f"Unique labels: {sorted(set(y_train.tolist()))}")
