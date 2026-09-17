"""
visualize.py
Lumexa Data Pattern Finder - Cluster Visualization

Produces two charts:
  1. A 2D scatter plot using petal length and petal width, colored by
     discovered cluster.
  2. A PCA-reduced 2D scatter plot representing all four features at
     once, colored by discovered cluster.

Run with:
    python3 src/visualize.py
(Requires src/cluster.py to have been run first to produce cluster_labels.npy)
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

try:
    from data_loader import load_iris_data, FEATURE_NAMES
    from cluster import LABELS_PATH, OUTPUT_DIR
except ImportError:
    from src.data_loader import load_iris_data, FEATURE_NAMES
    from src.cluster import LABELS_PATH, OUTPUT_DIR

PETAL_CHART_PATH = os.path.join(OUTPUT_DIR, "clusters_petal_view.png")
PCA_CHART_PATH = os.path.join(OUTPUT_DIR, "clusters_pca_view.png")


def load_cluster_labels(path=LABELS_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No cluster assignments found at {path}. Run 'python3 src/cluster.py' first."
        )
    return np.load(path)


def plot_petal_view(X_raw, cluster_labels, output_path=PETAL_CHART_PATH):
    """Plots petal length vs. petal width (indices 2 and 3), colored by cluster."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        X_raw[:, 2], X_raw[:, 3], c=cluster_labels, cmap="viridis", s=60, edgecolor="k", alpha=0.8
    )
    plt.xlabel(FEATURE_NAMES[2])
    plt.ylabel(FEATURE_NAMES[3])
    plt.title("Lumexa Data Pattern Finder: Discovered Clusters (Petal Measurements)")
    legend = plt.legend(*scatter.legend_elements(), title="Cluster")
    plt.gca().add_artist(legend)
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_pca_view(X_scaled, cluster_labels, output_path=PCA_CHART_PATH):
    """Reduces all 4 standardized features to 2D via PCA and plots the
    result, colored by cluster, so the full feature space can be viewed
    even though it has more than 2 dimensions.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    explained_variance = pca.explained_variance_ratio_.sum() * 100

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        X_pca[:, 0], X_pca[:, 1], c=cluster_labels, cmap="viridis", s=60, edgecolor="k", alpha=0.8
    )
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title(
        f"Lumexa Data Pattern Finder: Discovered Clusters (PCA View, "
        f"{explained_variance:.1f}% variance explained)"
    )
    legend = plt.legend(*scatter.legend_elements(), title="Cluster")
    plt.gca().add_artist(legend)
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    print("Loading data and cluster assignments...")
    X_raw, X_scaled, _ = load_iris_data()
    cluster_labels = load_cluster_labels()

    plot_petal_view(X_raw, cluster_labels)
    print(f"Petal-view chart saved to: {os.path.abspath(PETAL_CHART_PATH)}")

    plot_pca_view(X_scaled, cluster_labels)
    print(f"PCA-view chart saved to: {os.path.abspath(PCA_CHART_PATH)}")


if __name__ == "__main__":
    main()
