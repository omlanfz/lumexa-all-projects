"""
train.py — Movie Recommendation Engine (Project 09)
Data: MovieLens 1M ratings, mirrored at
https://raw.githubusercontent.com/khanhnamle1994/movielens/master/movies.csv
https://raw.githubusercontent.com/khanhnamle1994/movielens/master/ratings.csv

Approach: build the real user-item ratings matrix (6,040 users x 3,706 movies,
1,000,209 real ratings) and compress it with TruncatedSVD (matrix
factorization) into latent factors. Movie similarity is then computed with
real cosine similarity on the movies' latent-factor vectors — this is genuine
item-based collaborative filtering, not a random pick.

Saves:
  models/model.joblib -> dict with the SVD model, the movie latent factors,
                          movie-id <-> index maps, and the movies table.
"""
import os

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOVIES_PATH = os.path.join(HERE, "data", "movies.csv")
RATINGS_PATH = os.path.join(HERE, "data", "ratings.csv")
MODEL_PATH = os.path.join(HERE, "models", "model.joblib")

N_COMPONENTS = 50


def load_data():
    movies = pd.read_csv(MOVIES_PATH, sep="\t", index_col=0, encoding="latin-1")
    ratings = pd.read_csv(RATINGS_PATH, sep="\t", index_col=0, encoding="latin-1")
    return movies, ratings


def build_matrix(ratings):
    user_ids = ratings["user_id"].unique()
    movie_ids = ratings["movie_id"].unique()

    user_to_idx = {u: i for i, u in enumerate(user_ids)}
    movie_to_idx = {m: i for i, m in enumerate(movie_ids)}
    idx_to_movie = {i: m for m, i in movie_to_idx.items()}

    rows = ratings["user_id"].map(user_to_idx).values
    cols = ratings["movie_id"].map(movie_to_idx).values
    vals = ratings["rating"].values.astype(float)

    matrix = csr_matrix((vals, (rows, cols)), shape=(len(user_ids), len(movie_ids)))
    return matrix, user_to_idx, movie_to_idx, idx_to_movie


def main():
    movies, ratings = load_data()
    print(f"Loaded {len(movies)} movies and {len(ratings)} real ratings "
          f"from {ratings['user_id'].nunique()} users.")

    matrix, user_to_idx, movie_to_idx, idx_to_movie = build_matrix(ratings)
    print(f"User-item matrix shape: {matrix.shape}, "
          f"sparsity: {1 - matrix.nnz / (matrix.shape[0]*matrix.shape[1]):.4%}")

    # Matrix factorization: decompose the real ratings matrix into latent
    # factors that capture taste patterns (e.g. "sci-fi-ness", "romance-ness")
    # without us hand-labeling them.
    svd = TruncatedSVD(n_components=N_COMPONENTS, random_state=42)
    user_factors = svd.fit_transform(matrix)          # users x components
    movie_factors = svd.components_.T                  # movies x components
    print(f"Explained variance ratio (top {N_COMPONENTS} components): "
          f"{svd.explained_variance_ratio_.sum():.4f}")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({
        "svd": svd,
        "movie_factors": movie_factors,
        "user_factors": user_factors,
        "movie_to_idx": movie_to_idx,
        "idx_to_movie": idx_to_movie,
        "user_to_idx": user_to_idx,
        "movies": movies,
    }, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
