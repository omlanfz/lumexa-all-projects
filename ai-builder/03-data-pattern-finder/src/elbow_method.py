"""
elbow_method.py
Lumexa Data Pattern Finder - Elbow Method for Choosing k

Runs K-Means for a range of cluster counts (k) and plots each one's
inertia, helping visually identify a reasonable number of clusters to use.

Run with:
    python3 src/elbow_method.py
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

try:
    from data_loader import load_iris_data
except ImportError:
    from src.data_loader import load_iris_data

MAX_K = 10
RANDOM_SEED = 42

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
CHART_PATH = os.path.join(OUTPUT_DIR, "elbow_method.png")


def compute_inertias(X_scaled, max_k=MAX_K, seed=RANDOM_SEED):
    """Runs K-Means for k = 1..max_k and returns a list of inertia values."""
    inertias = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=seed, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
    return inertias


def plot_elbow(inertias, output_path=CHART_PATH):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    k_values = list(range(1, len(inertias) + 1))

    plt.figure(figsize=(8, 5))
    plt.plot(k_values, inertias, marker="o", color="steelblue", linewidth=2)
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Inertia (within-cluster sum of squared distances)")
    plt.title("Lumexa Data Pattern Finder: Elbow Method for Choosing k")
    plt.xticks(k_values)
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    print("Loading data...")
    _, X_scaled, _ = load_iris_data()

    print(f"Running K-Means for k = 1 to {MAX_K}...")
    inertias = compute_inertias(X_scaled)

    print(f"\n{'k':<6}{'Inertia':>12}")
    for k, inertia in enumerate(inertias, start=1):
        print(f"{k:<6}{inertia:>12.2f}")

    chart_path = plot_elbow(inertias)
    print(f"\nElbow chart saved to: {os.path.abspath(CHART_PATH)}")
    print("\nLook for the 'elbow' - the point where adding more clusters")
    print("stops meaningfully reducing inertia. For Iris, this is typically")
    print("around k=3, matching the 3 known species (though K-Means was")
    print("never told this).")


if __name__ == "__main__":
    main()
