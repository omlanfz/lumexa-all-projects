# Project 09 — Movie Recommendation Engine

## Purpose
Build a genuinely functional movie recommender using real MovieLens ratings —
matrix factorization plus real cosine similarity, not a random pick dressed
up as "AI."

## What Students Learn
- Building a real user-item ratings matrix from raw rating rows
- Why that matrix is extremely sparse (95.5% empty here) and what that means
- Matrix factorization with `TruncatedSVD` to learn latent "taste" factors
- Computing real cosine similarity between learned movie vectors
- Item-based collaborative filtering ("if you liked X, you'll like...")
- User-based prediction (dot product of user and movie latent vectors)
- Limitations of collaborative filtering: cold start, sparsity, popularity
  bias

## Tech
Python, pandas, scikit-learn (`TruncatedSVD`, `cosine_similarity`), scipy
(sparse matrices), joblib.

## Dataset
**MovieLens 1M** (GroupLens Research), mirrored at:
- `https://raw.githubusercontent.com/khanhnamle1994/movielens/master/movies.csv`
- `https://raw.githubusercontent.com/khanhnamle1994/movielens/master/ratings.csv`
- License: MovieLens data is provided by GroupLens for research/education use
  (see the original grouplens.org MovieLens license terms).
- Files are **tab-separated** and use **latin-1** encoding (some movie titles
  contain non-UTF-8 characters) — both handled explicitly in the loading
  code.
- `movies.csv`: 3,883 rows, columns `movie_id, title, genres`. 0 nulls.
- `ratings.csv`: 1,000,209 real ratings, columns
  `user_id, movie_id, rating, timestamp, user_emb_id, movie_emb_id`. 0 nulls,
  0 duplicate rows.
  - 6,040 unique users rated 3,706 unique movies.
  - Ratings are integers 1–5, mean 3.58, std 1.12.
  - Resulting user-item matrix is **95.53% sparse** — the central challenge
    collaborative filtering has to work around.

> **Note on this copy:** `ratings.csv` is 37MB, too large to include directly inside the
> delivered ZIP alongside everything else — `movies.csv` (small) is still included as-is.
> Run `data/download_dataset.sh` once (or manually
> `curl -L -o data/ratings.csv https://raw.githubusercontent.com/khanhnamle1994/movielens/master/ratings.csv`)
> before running `scripts/train.py` — it expects the file at exactly `data/ratings.csv`. This is
> the same real, complete 1,000,209-row file described above; the shipped `models/model.joblib`
> was trained on this exact file, so predictions reproduce exactly once it's downloaded.

## Structure
```
09-movie-recommendation-engine/
  data/movies.csv
  data/ratings.csv
  scripts/train.py       # builds ratings matrix, fits TruncatedSVD, saves factors
  scripts/recommend.py   # real cosine-similarity + latent-factor recommendations
  models/model.joblib    # saved SVD model + latent factors + id maps
  requirements.txt
```

## Install
```bash
pip install -r requirements.txt
```

## Run — "Training" (fitting the factorization model)
```bash
python3 scripts/train.py
```
Builds a sparse 6,040 × 3,706 user-item matrix from the real ratings, fits
`TruncatedSVD(n_components=50)` to factor it into user and movie latent
vectors, and saves everything needed for recommendations to
`models/model.joblib`.

Actual measured output:
```
Loaded 3883 movies and 1000209 real ratings from 6040 users.
User-item matrix shape: (6040, 3706), sparsity: 95.5316%
Explained variance ratio (top 50 components): 0.4122
```

## Run — Recommendations
```bash
python3 scripts/recommend.py
```
This finds movies similar to "Toy Story" via **real cosine similarity** on
learned latent vectors, and separately predicts top picks for a real user ID
via the dot product of that user's and every movie's latent factors.

Actual measured output:
```
Movies similar to 'Toy Story (1995)':
  Toy Story 2 (1999)  (cosine similarity=0.8180)
  Bug's Life, A (1998)  (cosine similarity=0.6460)
  Babe (1995)  (cosine similarity=0.5705)
  Pleasantville (1998)  (cosine similarity=0.5015)
  Tarzan (1999)  (cosine similarity=0.4824)

Top picks for user 1:
  Toy Story (1995)  (predicted score=4.2721)
  Toy Story 2 (1999)  (predicted score=4.2234)
  Schindler's List (1993)  (predicted score=3.6576)
  Back to the Future (1985)  (predicted score=3.0594)
  Shawshank Redemption, The (1994)  (predicted score=2.9593)
```
Note the top hit for "Toy Story" is genuinely "Toy Story 2" — real evidence
the similarity math is working, not randomly shuffled.

## Methodology & Limitations
- **Matrix factorization (SVD)**: compresses the sparse ratings matrix into
  50 dense "taste dimensions" per user/movie. This handles sparsity far
  better than raw item-item cosine similarity on the full sparse matrix
  would.
- **Cold start**: a brand-new movie or user with zero ratings has no learned
  latent vector, so it cannot be recommended or used as a similarity anchor
  until it accumulates some ratings.
- **Sparsity**: with 95.5% of the matrix empty, factorization only
  approximates true taste — the top-50 components explain about 41% of the
  variance in ratings, so predictions are directional, not exact.
- **Popularity bias**: heavily-rated movies tend to have more stable, and
  often higher, latent scores, so blockbuster titles can be over-recommended
  relative to niche films with few ratings.

## Troubleshooting
- `UnicodeDecodeError` while loading — make sure `encoding="latin-1"` is
  passed; several movie titles include accented characters.
- `ValueError: No movie title matches` — the search is a case-insensitive
  substring match on `title`; check spelling/spacing (titles include the
  release year, e.g. "Toy Story (1995)").
- Recommendations look generic — try increasing `N_COMPONENTS` in
  `train.py` for finer-grained taste vectors (at the cost of more noise).

## Extension Ideas
- Add a simple Flask endpoint that accepts a movie title and returns the
  top-N similar titles as JSON (mirrors Project 07/08's API pattern).
- Blend genre metadata with the learned latent vectors for a hybrid
  recommender.
- Evaluate with a real train/test split on ratings (mask some ratings, then
  measure how well the model predicts them) to get a quantitative RMSE.

## Portfolio Tips
Show the similarity table for a movie your reviewer will recognize (like
"Toy Story"), and be ready to explain *why* SVD works on sparse data —
that's the single most common recommender-systems interview question.
