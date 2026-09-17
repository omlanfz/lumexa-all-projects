"""
Emotion (facial expression) classification model for the Lumexa
Real-Time Emotion Detector.

Contains:
  - build_model(): the CNN architecture definition.
  - train_from_directory(): a real, runnable training script for anyone
    who supplies their own labeled dataset.
  - ExpressionClassifier: the inference-time wrapper used by main.py.

IMPORTANT (responsible AI): this model classifies visible facial
expression PATTERNS in pixel data. It does not detect, measure, or
know a person's true internal feelings. Confidence scores reflect
similarity to training data, not certainty about reality. See the
project README's disclaimer for full details.
"""

import argparse
import logging
import os

import cv2
import numpy as np

logger = logging.getLogger("emotion_detector.emotion_model")

EMOTION_LABELS = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]
IMG_SIZE = 48


def build_model(num_classes=7):
    """Defines the CNN architecture used for facial expression classification."""
    from tensorflow.keras import layers, models

    model = models.Sequential([
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 1)),

        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model


def train_from_directory(data_dir, output_path, epochs=30, batch_size=32):
    """
    Trains the emotion classification CNN on a labeled image dataset.

    Expects this folder structure under data_dir:
        train/<ClassName>/*.jpg
        validation/<ClassName>/*.jpg

    Class subfolder names should match EMOTION_LABELS (order does not
    need to match on disk -- Keras infers class order alphabetically
    and we remap it below to match EMOTION_LABELS for the saved model's
    documented output order).
    """
    import tensorflow as tf

    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "validation")

    if not os.path.isdir(train_dir) or not os.path.isdir(val_dir):
        raise FileNotFoundError(
            f"Expected '{train_dir}' and '{val_dir}' folders. "
            "See the project README's Configuration section for the required layout."
        )

    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        labels="inferred",
        label_mode="categorical",
        color_mode="grayscale",
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=batch_size,
        shuffle=True,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        labels="inferred",
        label_mode="categorical",
        color_mode="grayscale",
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=batch_size,
        shuffle=False,
    )

    class_names = train_ds.class_names
    logger.info(f"Discovered classes (alphabetical, from folder names): {class_names}")

    normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

    model = build_model(num_classes=len(class_names))
    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
    ]

    model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=callbacks)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    model.save(output_path)
    logger.info(f"Model saved to {output_path}")
    logger.warning(
        "IMPORTANT: verify that 'class_names' above matches EMOTION_LABELS order "
        "in this file. If your dataset's alphabetical folder order differs from "
        "['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise'], rename your "
        "class folders to match, or update EMOTION_LABELS accordingly, before "
        "deploying this model in the real-time app."
    )
    return model


class ExpressionClassifier:
    """Inference-time wrapper: loads a trained model and classifies face crops."""

    def __init__(self, config):
        self.config = config
        self.model = None
        self._load_model()

    def _load_model(self):
        path = self.config.MODEL_PATH
        if not os.path.isfile(path):
            logger.warning(
                f"No emotion model found at '{path}'. Running in detection-only mode. "
                "See models/README.md for how to train or supply a model."
            )
            return
        try:
            from tensorflow.keras.models import load_model
            self.model = load_model(path)
            logger.info(f"Emotion classification model loaded from '{path}'.")
        except Exception as exc:
            logger.error(f"Failed to load model at '{path}': {exc}")
            self.model = None

    def is_available(self):
        return self.model is not None

    def preprocess(self, face_crop_bgr):
        gray = cv2.cvtColor(face_crop_bgr, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)
        normalized = resized.astype("float32") / 255.0
        return normalized.reshape(1, IMG_SIZE, IMG_SIZE, 1)

    def classify(self, face_crop_bgr):
        """
        Returns (label, confidence). If no model is loaded, returns
        ("Model not loaded", 0.0). If confidence is below the configured
        threshold, returns ("Uncertain", confidence) rather than forcing
        a possibly-misleading confident label.
        """
        if self.model is None:
            return "Model not loaded", 0.0

        tensor = self.preprocess(face_crop_bgr)
        predictions = self.model.predict(tensor, verbose=0)[0]
        best_index = int(np.argmax(predictions))
        confidence = float(predictions[best_index])

        if confidence < self.config.EMOTION_CONFIDENCE_THRESHOLD:
            return "Uncertain", confidence

        label = EMOTION_LABELS[best_index] if best_index < len(EMOTION_LABELS) else "Unknown"
        return label, confidence


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(description="Train the Lumexa emotion classification model.")
    parser.add_argument("--train", action="store_true", help="Run training.")
    parser.add_argument("--data-dir", type=str, help="Path to dataset root (with train/ and validation/ subfolders).")
    parser.add_argument("--epochs", type=int, default=30, help="Number of training epochs.")
    parser.add_argument("--batch-size", type=int, default=32, help="Training batch size.")
    parser.add_argument("--output", type=str, default="models/emotion_model.h5", help="Output model file path.")
    args = parser.parse_args()

    if args.train:
        if not args.data_dir:
            parser.error("--data-dir is required when using --train")
        train_from_directory(args.data_dir, args.output, epochs=args.epochs, batch_size=args.batch_size)
    else:
        parser.print_help()
