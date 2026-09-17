# Data Pattern Finder

A beginner-friendly, fully working unsupervised machine learning project built for the Lumexa Python & AI Foundations course. This project uses K-Means clustering on the classic Iris flower dataset to automatically discover natural groupings in data with no labels provided during training.

## Overview

This project demonstrates a complete, real, end-to-end unsupervised machine learning (clustering) workflow:

1. Load the Iris dataset (150 flower measurements) via `sklearn.datasets`.
2. Explore and standardize the feature data.
3. Apply K-Means clustering to discover natural groupings, without using the true species labels during clustering.
4. Visualize the discovered clusters.
5. Compare the discovered clusters against the true species labels (for learning purposes only) to interpret how well clustering found real structure.
6. Print a plain-language interpretation of what each cluster represents.

## Learning Objectives

- Understand the difference between supervised learning (Lessons 5-8's regression/classification projects) and unsupervised learning.
- Understand why and how features are standardized before clustering.
- Use scikit-learn's `KMeans` to discover groups in unlabeled data.
- Use the "elbow method" to help choose a reasonable number of clusters.
- Visualize multi-dimensional clusters in 2D using selected features or PCA.
- Interpret discovered clusters in plain language.

## Features

- Uses the built-in `sklearn.datasets.load_iris()` dataset — no external downloads needed.
- Clean separation of concerns: data loading, clustering, visualization, and interpretation each live in their own script.
- Standardizes features using `StandardScaler` before clustering (important since K-Means is distance-based).
- Includes an elbow-method script to help choose the number of clusters (`k`).
- Visualizes clusters in 2D (using two of the four features, and separately using PCA for a full-feature view).
- Compares discovered clusters to true species labels for educational interpretation (this comparison is for learning only — real unsupervised problems have no true labels to check against).
- Includes a complete, runnable Jupyter notebook walking through the entire analysis interactively.

## Project Structure

```
03-data-pattern-finder/
├── README.md
├── requirements.txt
├── notebooks/
│   └── pattern_finder_walkthrough.ipynb
├── src/
│   ├── data_loader.py          # Loads the Iris dataset and standardizes features
│   ├── elbow_method.py          # Helps choose a good value of k
│   ├── cluster.py                # Runs K-Means clustering
│   ├── visualize.py              # Produces cluster visualization charts
│   └── interpret.py              # Prints a plain-language cluster interpretation
└── outputs/                     # Created automatically; stores charts
```

## Requirements

- Python 3.9 or newer
- pip
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

## Configuration

All configuration lives as plain constants at the top of each script:

- `src/cluster.py`: `NUM_CLUSTERS` (default 3, matching the 3 known Iris species — though the algorithm is never told this), `RANDOM_SEED`.
- `src/elbow_method.py`: `MAX_K` controls how many candidate values of k are tested.

## Running

Run each step from the project's root folder (`03-data-pattern-finder/`), in order:

```bash
# 1. (Optional but recommended) Run the elbow method to explore choices of k
python3 src/elbow_method.py

# 2. Run K-Means clustering
python3 src/cluster.py

# 3. Visualize the discovered clusters
python3 src/visualize.py

# 4. Print a plain-language interpretation of each cluster
python3 src/interpret.py
```

Alternatively, open `notebooks/pattern_finder_walkthrough.ipynb` in Jupyter to run the entire analysis interactively, cell by cell:

```bash
jupyter notebook notebooks/pattern_finder_walkthrough.ipynb
```

## How It Works

1. **Data loading** (`src/data_loader.py`): loads the Iris dataset (150 samples, 4 features: sepal length, sepal width, petal length, petal width) using `sklearn.datasets.load_iris()`, and standardizes the features with `StandardScaler` so no single feature dominates the distance calculations K-Means relies on.
2. **Elbow method** (`src/elbow_method.py`): runs K-Means for a range of `k` values (1 through `MAX_K`) and plots each one's "inertia" (within-cluster sum of squared distances), helping identify the "elbow" point where adding more clusters stops meaningfully improving the fit.
3. **Clustering** (`src/cluster.py`): runs `KMeans` with a chosen number of clusters on the standardized features only — the true species labels are never shown to the algorithm during clustering — and saves the resulting cluster assignments.
4. **Visualization** (`src/visualize.py`): produces two charts — a 2D scatter plot using petal length and petal width (the two most visually separable features), and a PCA-reduced 2D scatter plot representing all four features at once — both colored by discovered cluster.
5. **Interpretation** (`src/interpret.py`): compares the discovered cluster assignments against the true species labels (using `pandas`-free cross-tabulation) purely as an educational check, and prints a plain-language summary of what each cluster tends to represent (e.g., "Cluster 0 contains mostly small flowers, closely matching the setosa species").

## Common Problems

- **`ModuleNotFoundError: No module named 'sklearn'`**: run `pip install -r requirements.txt` inside your active virtual environment.
- **Clusters don't perfectly match species**: this is expected and educational — K-Means never sees the species labels, and two of the three Iris species (versicolor and virginica) have naturally overlapping measurements, so some misalignment is a genuine, realistic result, not a bug.
- **Different cluster numbers/order across runs**: K-Means assigns arbitrary cluster ID numbers (0, 1, 2) that can differ between runs unless `random_state` is fixed — this project fixes `RANDOM_SEED` for reproducibility, but the specific IDs (which cluster is called "0" vs "1") are still not meaningful on their own; only the groupings themselves matter.
- **Chart doesn't display in a headless environment**: charts are saved to disk with `plt.savefig()` regardless of display availability; open the resulting PNG file directly.

## Extensions

- Try different values of `NUM_CLUSTERS` (e.g., 2 or 4) and observe how the groupings change.
- Apply the same pipeline to a different built-in dataset, such as `sklearn.datasets.load_wine()`.
- Try a different clustering algorithm, such as `sklearn.cluster.DBSCAN` or `AgglomerativeClustering`, and compare results.
- Add a silhouette score calculation (`sklearn.metrics.silhouette_score`) as a second, more rigorous way to evaluate cluster quality beyond the elbow method.
- Extend `interpret.py` to generate a short natural-language paragraph summarizing each cluster's typical feature ranges (min/max/average per feature).
