"""
cluster.py
Lumexa Data Pattern Finder - K-Means Clustering

Runs K-Means clustering on the standardized Iris features (no labels
used) and saves the resulting cluster assignments to disk as a NumPy
file for use by visualize.py and interpret.py.

Run with:
    python3 src/cluster.py
"""

import os

import numpy as np
from sklearn.cluster import KMeans

try:
    from data_loader import load_iris_data
except ImportError:
    from src.data_loader import load_iris_data

NUM_CLUSTERS = 3
RANDOM_SEED = 42

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
LABELS_PATH = os.path.join(OUTPUT_DIR, "cluster_labels.npy")


def run_kmeans(X_scaled, num_clusters=NUM_CLUSTERS, seed=RANDOM_SEED):
    """Fits K-Means on standardized features and returns the fitted model
    and its cluster assignments. The true species labels are never passed
    to this function - this is unsupervised learning.
    """
    kmeans = KMeans(n_clusters=num_clusters, random_state=seed, n_init=10)
    cluster_assignments = kmeans.fit_predict(X_scaled)
    return kmeans, cluster_assignments


def main():
    print("Loading data...")
    X_raw, X_scaled, true_labels = load_iris_data()

    print(f"Running K-Means with k={NUM_CLUSTERS} clusters...")
    print("(Note: the true species labels are NOT used during clustering.)")
    kmeans, cluster_assignments = run_kmeans(X_scaled)

    print(f"\nCluster assignments for first 10 samples: {cluster_assignments[:10]}")
    print(f"Cluster sizes: {np.bincount(cluster_assignments)}")
    print(f"Final inertia: {kmeans.inertia_:.2f}")
    print(f"Cluster centers (in standardized feature space):")
    for i, center in enumerate(kmeans.cluster_centers_):
        print(f"  Cluster {i}: {np.round(center, 3)}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    np.save(LABELS_PATH, cluster_assignments)
    print(f"\nCluster assignments saved to: {os.path.abspath(LABELS_PATH)}")


if __name__ == "__main__":
    main()
