"""
interpret.py
Lumexa Data Pattern Finder - Cluster Interpretation

Compares the discovered K-Means clusters against the true Iris species
labels (for educational purposes only - this comparison is not possible
in a real unsupervised problem where no true labels exist) and prints a
plain-language summary of what each cluster represents.

Run with:
    python3 src/interpret.py
(Requires src/cluster.py to have been run first to produce cluster_labels.npy)
"""

import os

import numpy as np

try:
    from data_loader import load_iris_data, FEATURE_NAMES, SPECIES_NAMES
    from cluster import LABELS_PATH
    from visualize import load_cluster_labels
except ImportError:
    from src.data_loader import load_iris_data, FEATURE_NAMES, SPECIES_NAMES
    from src.cluster import LABELS_PATH
    from src.visualize import load_cluster_labels


def build_cross_tab(cluster_labels, true_labels, num_clusters, num_species):
    """Builds a simple cross-tabulation: rows = discovered clusters,
    columns = true species, values = counts. Built with plain NumPy so
    no extra dependency (like pandas) is required.
    """
    table = np.zeros((num_clusters, num_species), dtype=int)
    for cluster_id, species_id in zip(cluster_labels, true_labels):
        table[cluster_id, species_id] += 1
    return table


def summarize_cluster_features(X_raw, cluster_labels, cluster_id):
    """Returns average feature values for all samples in a given cluster."""
    mask = cluster_labels == cluster_id
    cluster_samples = X_raw[mask]
    return cluster_samples.mean(axis=0)


def main():
    print("Loading data...")
    X_raw, X_scaled, true_labels = load_iris_data()
    cluster_labels = load_cluster_labels()

    num_clusters = len(set(cluster_labels))
    num_species = len(SPECIES_NAMES)

    cross_tab = build_cross_tab(cluster_labels, true_labels, num_clusters, num_species)

    print("\n" + "=" * 60)
    print("CLUSTER vs. TRUE SPECIES CROSS-TABULATION")
    print("(For educational comparison only - species were NOT used")
    print(" during clustering.)")
    print("=" * 60)
    header = f"{'Cluster':<10}" + "".join(f"{name:>14}" for name in SPECIES_NAMES)
    print(header)
    for cluster_id in range(num_clusters):
        row = f"{cluster_id:<10}" + "".join(
            f"{cross_tab[cluster_id, species_id]:>14}" for species_id in range(num_species)
        )
        print(row)

    print("\n" + "=" * 60)
    print("PLAIN-LANGUAGE CLUSTER INTERPRETATION")
    print("=" * 60)
    for cluster_id in range(num_clusters):
        avg_features = summarize_cluster_features(X_raw, cluster_labels, cluster_id)
        dominant_species_id = int(np.argmax(cross_tab[cluster_id]))
        dominant_species = SPECIES_NAMES[dominant_species_id]
        dominant_count = cross_tab[cluster_id, dominant_species_id]
        total_in_cluster = cross_tab[cluster_id].sum()
        match_percent = (dominant_count / total_in_cluster * 100) if total_in_cluster else 0

        print(f"\nCluster {cluster_id} ({total_in_cluster} flowers):")
        print(f"  Average measurements:")
        for name, value in zip(FEATURE_NAMES, avg_features):
            print(f"    {name}: {value:.2f} cm")
        print(f"  Most closely resembles: '{dominant_species}' "
              f"({match_percent:.0f}% of this cluster is that species)")

    print("\n" + "=" * 60)
    print("KEY TAKEAWAY: K-Means found these groupings using only the raw")
    print("measurements - it was never told which flower belonged to which")
    print("species. The fact that discovered clusters line up reasonably")
    print("well with real species is strong evidence that genuine natural")
    print("structure exists in the data, not something we imagined.")
    print("=" * 60)


if __name__ == "__main__":
    main()
