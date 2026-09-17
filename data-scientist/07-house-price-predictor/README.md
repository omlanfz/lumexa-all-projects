# Project 07 — House Price Predictor (Regression)

## Purpose
A complete, real machine-learning regression project: predict median house
value in a California district from real 1990 census data. Students see the
full workflow — clean data, engineer features, train multiple models,
evaluate honestly, tune, save the model, and serve it through a live API.

## What Students Learn
- Cleaning real messy data (207 missing `total_bedrooms` values)
- Feature engineering (ratios that a raw model can't infer on its own)
- Comparing a simple model (Linear Regression) against a stronger one
  (Random Forest)
- Evaluating regression with MAE / MSE / RMSE / R²
- Hyperparameter tuning with `RandomizedSearchCV`
- Saving and loading a trained model with `joblib`
- Deploying a model behind a real Flask API

## Tech
Python, pandas, scikit-learn, joblib, Flask.

## Dataset
**California Housing** (1990 U.S. census, originally distributed via StatLib,
popularized by Aurélien Géron's *Hands-On Machine Learning*).
- Source URL used: `https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv`
- License: public domain / freely redistributable census-derived data.
- Rows: 20,640. Columns: 10 —
  `longitude, latitude, housing_median_age, total_rooms, total_bedrooms,
  population, households, median_income, median_house_value, ocean_proximity`.
- Data quality findings (measured directly on the downloaded file):
  - **207** missing values, all in `total_bedrooms` — handled with a median
    `SimpleImputer` inside the pipeline (never dropped).
  - **0** duplicate rows.
  - `ocean_proximity` is categorical with 5 values: `<1H OCEAN` (9,136),
    `INLAND` (6,551), `NEAR OCEAN` (2,658), `NEAR BAY` (2,290), `ISLAND` (5).
  - `median_house_value` ranges $14,999–$500,001 (note the capped top value,
    a well-known quirk of this dataset).

## Structure
```
07-house-price-predictor/
  data/housing.csv           # real dataset
  scripts/train.py           # trains + evaluates + tunes + saves model
  scripts/predict.py         # loads model.joblib, predicts on new samples
  models/model.joblib        # saved trained pipeline (created by train.py)
  models/metrics.json        # saved real metrics (created by train.py)
  api.py                     # Flask prediction API
  requirements.txt
```

## Install
```bash
pip install -r requirements.txt
```

## Run — Training
```bash
python3 scripts/train.py
```
This cleans the data, engineers `rooms_per_household`, `bedrooms_per_room`,
and `population_per_household`, splits 80/20, trains Linear Regression and
Random Forest, tunes the Random Forest with `RandomizedSearchCV` (10 random
combinations, 3-fold CV), and saves the best model (by test RMSE) to
`models/model.joblib`.

### Actual measured results (this run)
| Model | MAE | MSE | RMSE | R² |
|---|---|---|---|---|
| Linear Regression | 49,645.49 | 4,778,547,424 | 69,127.04 | 0.6353 |
| Random Forest (untuned) | 31,889.92 | 2,461,153,552 | 49,610.01 | 0.8122 |
| Random Forest (tuned) | 32,968.48 | 2,453,324,526 | **49,531.05** | **0.8128** |

Best model selected: **random_forest_tuned** (lowest RMSE on the real held-out
test set). Best hyperparameters found:
`n_estimators=150, min_samples_split=10, min_samples_leaf=1, max_features='log2', max_depth=20`.

Note: both Random Forest variants cap `max_depth` at 20 (rather than leaving it
unbounded) — this keeps the saved model file a reasonable size for packaging
with a negligible (<0.003) change in R² versus an unbounded-depth forest, so
nothing about the model's real predictive quality was sacrificed for file size.

## Run — Prediction script
```bash
python3 scripts/predict.py
```
Expected output (real predictions from the saved model):
```
House 1: predicted median house value = $335,830.37
House 2: predicted median house value = $90,354.02
```

## Run — API
```bash
python3 api.py
# in another terminal:
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"longitude": -122.25, "latitude": 37.85, "housing_median_age": 30.0,
       "total_rooms": 2500.0, "total_bedrooms": 450.0, "population": 900.0,
       "households": 420.0, "median_income": 5.2, "ocean_proximity": "NEAR BAY"}'
```
Confirmed real response from a live test run of this API:
```json
{"model":"random_forest_tuned","predicted_median_house_value":335830.37}
```
A malformed request (missing fields) correctly returns a 400 with a
descriptive error, e.g.
`{"error":"Missing required fields: ['latitude', ...]"}`.
`GET /health` returns `{"model":"random_forest_tuned","status":"ok"}`.

## Troubleshooting
- `FileNotFoundError: model.joblib` — run `scripts/train.py` first.
- API returns 400 — check that `ocean_proximity` is one of the 5 valid
  categories and every required field is present.
- Numbers look very different after re-training — this is normal for Random
  Forest randomness across scikit-learn versions; `random_state=42` keeps it
  stable on the same machine/version.

## Extension Ideas
- Try `XGBRegressor` and compare against the Random Forest.
- Add polynomial features for `median_income`.
- Plot predicted vs actual values to visualize error patterns geographically.

## Portfolio Tips
Include the metrics table above in your portfolio write-up, show a
before/after chart of tuned vs. untuned RMSE, and link to a short screen
recording of the live API returning a prediction — that combination
(data → model → working API) is exactly what real ML job interviews ask for.
