"""
data_loader.py
Lumexa Data Pattern Finder - Data Loading and Preprocessing

Loads the Iris dataset and standardizes its features so no single
feature dominates distance-based clustering.
"""

import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

FEATURE_NAMES = [
    "sepal_length_cm",
    "sepal_width_cm",
    "petal_length_cm",
    "petal_width_cm",
]

SPECIES_NAMES = ["setosa", "versicolor", "virginica"]


def load_iris_data():
    """Loads the Iris dataset and returns raw features, standardized
    features, and the true species labels (for educational comparison only
    - never used during clustering itself).

    Returns:
        X_raw (np.ndarray): shape (150, 4), original feature values.
        X_scaled (np.ndarray): shape (150, 4), standardized feature values
            (mean 0, standard deviation 1 per feature).
        true_labels (np.ndarray): shape (150,), integer species labels 0-2,
            used only afterward to interpret/check clustering results.
    """
    iris = load_iris()
    X_raw = iris.data
    true_labels = iris.target

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)

    return X_raw, X_scaled, true_labels


if __name__ == "__main__":
    X_raw, X_scaled, true_labels = load_iris_data()
    print(f"Dataset shape: {X_raw.shape}")
    print(f"Features: {FEATURE_NAMES}")
    print(f"Species: {SPECIES_NAMES}")
    print(f"\nFirst 3 raw samples:\n{X_raw[:3]}")
    print(f"\nFirst 3 standardized samples:\n{np.round(X_scaled[:3], 3)}")
    print(f"\nTrue species counts: {np.bincount(true_labels)}")
