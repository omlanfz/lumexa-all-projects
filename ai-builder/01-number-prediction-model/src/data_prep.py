"""
data_prep.py
Lumexa Number Prediction Model - Data Preparation

Loads the study_scores.csv dataset, converts it to NumPy arrays shaped
correctly for scikit-learn, and splits it into training and test sets.
"""

import csv
import os

import numpy as np
from sklearn.model_selection import train_test_split

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "study_scores.csv")

TEST_SIZE = 0.2
RANDOM_SEED = 42


def load_dataset(csv_path=DATA_PATH):
    """Loads the CSV dataset into two NumPy arrays: hours_studied and test_score.

    Raises:
        FileNotFoundError: if the CSV file does not exist yet (run
            data/generate_data.py first).
    """
    csv_path = os.path.abspath(csv_path)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. "
            "Run 'python3 data/generate_data.py' first to create it."
        )

    hours_studied = []
    test_scores = []

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hours_studied.append(float(row["hours_studied"]))
            test_scores.append(float(row["test_score"]))

    return np.array(hours_studied), np.array(test_scores)


def prepare_train_test_data(csv_path=DATA_PATH, test_size=TEST_SIZE, seed=RANDOM_SEED):
    """Loads the dataset and returns a properly split, correctly shaped
    train/test dataset ready for scikit-learn.

    Returns:
        X_train, X_test, y_train, y_test (all np.ndarray)
    """
    hours_studied, test_scores = load_dataset(csv_path)

    # scikit-learn expects X (features) to be a 2D array: (n_samples, n_features)
    X = hours_studied.reshape(-1, 1)
    y = test_scores

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = prepare_train_test_data()
    print(f"Loaded dataset and split into:")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")
    print(f"  X_train shape: {X_train.shape}")
    print(f"  y_train shape: {y_train.shape}")
