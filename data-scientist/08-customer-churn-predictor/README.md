# Project 08 — Customer Churn Predictor (Classification)

## Purpose
A complete, real ML classification project: predict whether a telecom
customer will cancel ("churn") using the industry-famous IBM Telco Customer
Churn dataset. Students practice classification metrics, categorical
encoding, class imbalance, and model comparison end-to-end.

## What Students Learn
- Cleaning a real, messy string column (`TotalCharges`)
- One-hot encoding many categorical columns
- Training and comparing Logistic Regression, Random Forest, and XGBoost
- Evaluating classification with accuracy, precision, recall, F1, and a
  confusion matrix
- Why accuracy alone is misleading on imbalanced data
- Tuning with `GridSearchCV`
- Saving a classifier with `joblib` and using it for real predictions

## Tech
Python, pandas, scikit-learn, xgboost, joblib.

## Dataset
**IBM Telco Customer Churn**
- Source URL used: `https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv`
- License: IBM sample dataset, freely distributed for education/demo use.
- Rows: 7,043. Columns: 21 (customer demographics, account info, services
  subscribed, `MonthlyCharges`, `TotalCharges`, and target `Churn`).
- Data quality findings (measured directly on the downloaded file):
  - **0** missing values as loaded, but `TotalCharges` is stored as **text**
    and contains **11** rows that are blank strings (`" "`) — these are all
    customers with `tenure == 0` (brand new, never billed). We coerce to
    numeric with `pd.to_numeric(errors="coerce")` and fill those 11 with
    `0.0`.
  - **0** duplicate rows.
  - Class balance: **5,174** "No" churn vs **1,869** "Yes" churn (about
    26.5% churn rate) — a real, moderately imbalanced target, which is why we
    look at precision/recall/F1, not just accuracy.

## Structure
```
08-customer-churn-predictor/
  data/Telco-Customer-Churn.csv
  scripts/train.py       # cleans, engineers features, trains 3 models, tunes, saves
  scripts/predict.py     # loads model.joblib, predicts on new sample customers
  models/model.joblib    # saved trained pipeline (created by train.py)
  models/metrics.json    # saved real metrics (created by train.py)
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
Cleans `TotalCharges`, drops `customerID`, engineers `avg_monthly_spend` and
`tenure_years`, splits 80/20 (stratified on `Churn`), trains Logistic
Regression, Random Forest, and XGBoost, tunes XGBoost with a small
`GridSearchCV`, and saves the best model (by test F1) to `models/model.joblib`.

### Actual measured results (this run)
| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.8077 | 0.6614 | 0.5642 | **0.6089** |
| Random Forest | 0.7814 | 0.6100 | 0.4893 | 0.5430 |
| XGBoost (untuned) | 0.7963 | 0.6465 | 0.5134 | 0.5723 |
| XGBoost (tuned) | 0.8070 | 0.6759 | 0.5241 | 0.5904 |

Best model selected: **logistic_regression** (highest F1 of 0.6089 on the
real held-out test set of 1,409 customers). Confusion matrix (rows = actual
No/Yes, cols = predicted No/Yes): `[[927, 108], [163, 211]]`.

XGBoost tuned best params:
`learning_rate=0.03, max_depth=3, n_estimators=300`.

## Run — Prediction script
```bash
python3 scripts/predict.py
```
Expected output (real predictions from the saved model):
```
Customer 1: WILL CHURN  (churn probability = 64.21%)
Customer 2: will stay  (churn probability = 1.47%)
```

## Troubleshooting
- `KeyError: 'customerID'` on predict — the prediction script's sample
  customers intentionally omit `customerID`; the trained pipeline never sees
  it either (dropped during training).
- If `TotalCharges` errors during training, confirm you're using the CSV in
  `data/` unmodified — the blank-string quirk is handled in `load_and_clean()`.
- Low recall is expected here (real churn data is genuinely hard and
  imbalanced) — this is a realistic outcome to discuss with students, not a
  bug.

## Extension Ideas
- Try `class_weight="balanced"` or SMOTE to address the imbalance.
- Add a feature for "number of add-on services subscribed".
- Plot a precision-recall curve instead of a single threshold.

## Portfolio Tips
Explain in your write-up *why* F1 (not accuracy) was the right metric to
optimize given the ~26% churn rate, and show the confusion matrix — that
kind of metric literacy is what separates a beginner project from a
job-ready one.
