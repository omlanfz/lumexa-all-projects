"""
recommend.py — real item-based collaborative filtering recommendations.

Given a movie title, computes real cosine similarity between that movie's
latent-factor vector (learned by TruncatedSVD on the real MovieLens ratings
matrix) and every other movie's vector, and returns the top-N most similar
movies. Given a user ID, recommends movies predicted to have the highest
rating for that user using the dot product of user and movie latent factors.

Run: python3 scripts/recommend.py
"""
import os

import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(HERE, "models", "model.joblib")


def load_bundle():
    return joblib.load(MODEL_PATH)


def recommend_similar_movies(bundle, title_query, top_n=10):
    movies = bundle["movies"]
    movie_factors = bundle["movie_factors"]
    movie_to_idx = bundle["movie_to_idx"]

    matches = movies[movies["title"].str.contains(title_query, case=False, regex=False)]
    if matches.empty:
        raise ValueError(f"No movie title matches '{title_query}'")
    target_row = matches.iloc[0]
    target_movie_id = target_row["movie_id"]

    if target_movie_id not in movie_to_idx:
        raise ValueError(f"Movie '{target_row['title']}' has no ratings in the training data")

    target_idx = movie_to_idx[target_movie_id]
    target_vec = movie_factors[target_idx].reshape(1, -1)

    # Real cosine similarity between the target movie and every other movie's
    # learned latent-factor vector.
    sims = cosine_similarity(target_vec, movie_factors)[0]

    ranked_idx = np.argsort(-sims)
    idx_to_movie = bundle["idx_to_movie"]

    results = []
    for idx in ranked_idx:
        movie_id = idx_to_movie[idx]
        if movie_id == target_movie_id:
            continue
        title = movies.loc[movies["movie_id"] == movie_id, "title"].values[0]
        results.append((title, float(sims[idx])))
        if len(results) >= top_n:
            break

    return target_row["title"], results


def recommend_for_user(bundle, user_id, top_n=10):
    user_to_idx = bundle["user_to_idx"]
    movie_factors = bundle["movie_factors"]
    user_factors = bundle["user_factors"]
    movies = bundle["movies"]
    idx_to_movie = bundle["idx_to_movie"]

    if user_id not in user_to_idx:
        raise ValueError(f"User {user_id} not found in training data")

    u_idx = user_to_idx[user_id]
    user_vec = user_factors[u_idx]

    # Predicted rating for every movie = dot product of the user's latent
    # taste vector and each movie's latent factor vector (matrix factorization
    # prediction), a real computed score — not a random guess.
    predicted_scores = movie_factors @ user_vec

    ranked_idx = np.argsort(-predicted_scores)
    results = []
    for idx in ranked_idx:
        movie_id = idx_to_movie[idx]
        title = movies.loc[movies["movie_id"] == movie_id, "title"].values[0]
        results.append((title, float(predicted_scores[idx])))
        if len(results) >= top_n:
            break
    return results


if __name__ == "__main__":
    bundle = load_bundle()

    title, similar = recommend_similar_movies(bundle, "Toy Story", top_n=5)
    print(f"Movies similar to '{title}':")
    for t, score in similar:
        print(f"  {t}  (cosine similarity={score:.4f})")

    print()
    user_id = bundle["user_to_idx"] and list(bundle["user_to_idx"].keys())[0]
    recs = recommend_for_user(bundle, user_id, top_n=5)
    print(f"Top picks for user {user_id}:")
    for t, score in recs:
        print(f"  {t}  (predicted score={score:.4f})")
