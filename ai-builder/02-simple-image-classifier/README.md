# Simple Image Classifier

A beginner-friendly, fully working deep learning project built for the Lumexa Python & AI Foundations course. This project trains a small convolutional neural network with TensorFlow/Keras to classify handwritten digit images (0-9) from the classic MNIST dataset.

## Overview

This project demonstrates a complete, real, end-to-end supervised machine learning (classification) workflow using deep learning:

1. Load a small, built-in image dataset (MNIST handwritten digits) via `keras.datasets`.
2. Preprocess and normalize the image data.
3. Define a small convolutional neural network (CNN).
4. Train the model for a few epochs (kept small and laptop-friendly).
5. Evaluate accuracy on a held-out test set.
6. Run inference on a single sample image and display the prediction.

It is intentionally kept small (a handful of epochs, a small model, and an optional subset of the data) so it trains quickly on a normal laptop CPU with no GPU required.

## Learning Objectives

- Understand how image data is represented numerically (pixel grids, normalization).
- Understand the difference between a dense (fully-connected) layer and a convolutional layer at a conceptual level.
- Practice a full classification workflow: load, preprocess, train, evaluate, predict.
- Interpret classification accuracy and a confusion matrix.
- Use a trained Keras model for inference on a single new image.

## Features

- Uses the built-in `keras.datasets.mnist` dataset — no external downloads or file management needed beyond Keras's own automatic caching.
- Clean separation of concerns: data loading/preprocessing, model definition, training, evaluation, and inference each live in their own script.
- Small CNN architecture (2 convolutional layers + pooling + dense output) that trains in a few minutes on CPU.
- Saves the trained model to `models/mnist_cnn.keras` so `predict.py` can run independently of training.
- Evaluation script reports accuracy, loss, and per-class breakdown.
- Inference script classifies a single sample image and prints the predicted digit with confidence.

## Project Structure

```
02-simple-image-classifier/
├── README.md
├── requirements.txt
├── models/                     # Created automatically; stores mnist_cnn.keras after training
├── src/
│   ├── data_loader.py           # Loads and preprocesses MNIST via keras.datasets
│   ├── model.py                 # Defines the CNN architecture
│   ├── train.py                 # Trains the model and saves it to models/mnist_cnn.keras
│   ├── evaluate.py               # Loads the saved model, reports test accuracy/loss
│   └── predict.py                # Loads the saved model and classifies a sample image
└── outputs/                     # Created automatically; stores sample prediction images
```

## Requirements

- Python 3.9 or newer
- pip
- Roughly 500MB of free disk space (TensorFlow itself is a fairly large package)
- See `requirements.txt` for exact pinned versions

## Installation

1. (Recommended) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

The first time you run any script, Keras will automatically download the MNIST dataset (about 11MB) and cache it locally in `~/.keras/datasets/`. This requires an internet connection on first run only.

## Configuration

All configuration lives as plain constants at the top of each script:

- `src/data_loader.py`: `SUBSET_SIZE` (set to `None` to use the full 60,000-image training set, or an integer like `6000` for a faster subset while experimenting).
- `src/train.py`: `EPOCHS`, `BATCH_SIZE`, `VALIDATION_SPLIT` control training behavior.

## Running

Run each step from the project's root folder (`02-simple-image-classifier/`), in order:

```bash
# 1. Train the model (downloads MNIST on first run, then trains and saves the model)
python3 src/train.py

# 2. Evaluate the trained model on the test set
python3 src/evaluate.py

# 3. Classify a single sample image (by test-set index)
python3 src/predict.py --index 0
python3 src/predict.py --index 42
```

Training with the default settings (full dataset, 5 epochs, small CNN) typically takes a few minutes on a modern laptop CPU.

## How It Works

1. **Data loading** (`src/data_loader.py`): loads MNIST using `tensorflow.keras.datasets.mnist.load_data()`, reshapes each 28x28 grayscale image to include an explicit channel dimension (`(28, 28, 1)`), and normalizes pixel values from the raw `0-255` range to `0.0-1.0` (a standard preprocessing step that helps neural networks train faster and more reliably).
2. **Model definition** (`src/model.py`): defines a small CNN with two convolution + max-pooling blocks, a flatten layer, a dense hidden layer with dropout for regularization, and a final dense layer with 10 outputs (one per digit) using a softmax activation.
3. **Training** (`src/train.py`): compiles the model with the Adam optimizer and sparse categorical cross-entropy loss (appropriate for integer class labels), trains for a small number of epochs while holding out a validation split, and saves the trained model to `models/mnist_cnn.keras`.
4. **Evaluation** (`src/evaluate.py`): loads the saved model and reports test-set accuracy and loss, plus a per-digit breakdown of how many test images were correctly classified.
5. **Prediction** (`src/predict.py`): loads the saved model, picks one image from the test set by index, displays the model's predicted digit and confidence score, and saves a labeled image showing the digit alongside the prediction.

## Common Problems

- **`ModuleNotFoundError: No module named 'tensorflow'`**: run `pip install -r requirements.txt` inside your active virtual environment.
- **TensorFlow install fails or is very slow**: TensorFlow is a large package; ensure you have a stable internet connection and at least 500MB free disk space. On some older machines, installing `tensorflow-cpu` instead of `tensorflow` can be faster if you don't need GPU support (edit `requirements.txt` if needed).
- **`FileNotFoundError: models/mnist_cnn.keras`**: run `python3 src/train.py` before running `evaluate.py` or `predict.py`.
- **Training seems slow**: reduce `SUBSET_SIZE` in `src/data_loader.py` to a smaller number (e.g., `6000`) while experimenting, then switch back to `None` for a final full-accuracy run.
- **First run seems to hang**: this is usually the automatic MNIST download; it should complete within a minute on a normal connection and is cached afterward.
- **Warnings about CPU instructions (AVX2, oneDNN, etc.) printed at startup**: these are informational TensorFlow messages, not errors, and can be safely ignored.

## Extensions

- Swap MNIST for `keras.datasets.fashion_mnist` (clothing item images) and update the class label names accordingly.
- Add data augmentation (small rotations/shifts) using `tf.keras.layers.RandomRotation` to improve robustness.
- Add a confusion matrix visualization using `sklearn.metrics.confusion_matrix` and Matplotlib.
- Track and plot training vs. validation accuracy per epoch to visually spot overfitting, connecting back to Lesson 7's concepts.
- Extend `predict.py` to accept an arbitrary external PNG file (resized and normalized to 28x28 grayscale) instead of only test-set indices.
