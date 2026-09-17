# Number Prediction Model

A beginner-friendly, fully working machine learning project built for the Lumexa Python & AI Foundations course. This project trains a linear regression model in scikit-learn to predict a student's test score from the number of hours they studied, then evaluates and visualizes the results.

## Overview

This project demonstrates a complete, real, end-to-end supervised machine learning (regression) workflow:

1. Generate a realistic synthetic dataset (hours studied vs. test score).
2. Split the data into training and test sets.
3. Train a linear regression model.
4. Evaluate the model honestly using MSE and R².
5. Visualize the results with Matplotlib.
6. Use the trained model to make predictions on brand-new input.

It is designed to be run entirely on a laptop with no GPU and no internet access after the initial package install, and it corresponds directly to Lessons 5-8 of the Python & AI Foundations course.

## Learning Objectives

- Understand the difference between features (X) and labels (y) in a real dataset.
- Practice the full train/test split and model evaluation workflow.
- Interpret MSE and R² as measures of model quality.
- Recognize overfitting vs. underfitting by comparing training and test metrics.
- Use a trained model for inference on new, unseen data.
- Communicate model results with clear, labeled visualizations.

## Features

- Synthetic but realistic dataset generator with configurable noise.
- Clean separation of concerns: data generation, training, evaluation, visualization, and inference each live in their own script.
- Proper train/test split with a reproducible random seed.
- Reports both MSE and R² on training and test sets, flagging possible overfitting/underfitting.
- Saves a trained model to disk (`models/model.joblib`) so `predict.py` can be run independently of training.
- Generates a labeled scatter plot with a prediction line, saved as a PNG.
- Includes a complete, runnable Jupyter notebook walking through the entire workflow interactively.

## Project Structure

```
01-number-prediction-model/
├── README.md
├── requirements.txt
├── data/
│   └── generate_data.py       # Creates data/study_scores.csv
├── notebooks/
│   └── number_prediction_walkthrough.ipynb
├── models/                     # Created automatically; stores model.joblib after training
├── src/
│   ├── data_prep.py            # Loads CSV, splits into train/test, returns NumPy arrays
│   ├── train.py                # Trains the model and saves it to models/model.joblib
│   ├── evaluate.py              # Loads the saved model, reports MSE/R² on train & test sets
│   ├── visualize.py             # Produces results_chart.png
│   └── predict.py               # Loads the saved model and predicts on new input
└── outputs/                     # Created automatically; stores charts and text summaries
```

## Requirements

- Python 3.9 or newer
- pip (Python's package manager)
- See `requirements.txt` for exact pinned package versions

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

All configuration lives as plain constants at the top of each script (no config files or environment variables are needed, since this project has no secrets or external services):

- `data/generate_data.py`: `NUM_SAMPLES`, `NOISE_LEVEL`, `RANDOM_SEED` control the synthetic dataset.
- `src/train.py`: `TEST_SIZE`, `RANDOM_SEED` control the train/test split.

Adjust these values directly in the files if you want to experiment with more data, more noise, or a different split ratio.

## Running

Run each step from the project's root folder (`01-number-prediction-model/`), in order:

```bash
# 1. Generate the dataset (creates data/study_scores.csv)
python3 data/generate_data.py

# 2. Train the model (creates models/model.joblib)
python3 src/train.py

# 3. Evaluate the trained model (prints MSE and R² to the terminal)
python3 src/evaluate.py

# 4. Visualize results (creates outputs/results_chart.png)
python3 src/visualize.py

# 5. Predict on new input
python3 src/predict.py --hours 6.5
```

Alternatively, open `notebooks/number_prediction_walkthrough.ipynb` in Jupyter to run the entire workflow interactively, cell by cell:

```bash
jupyter notebook notebooks/number_prediction_walkthrough.ipynb
```

## How It Works

1. **Data generation** (`data/generate_data.py`): creates a synthetic dataset where test scores follow a roughly linear relationship with hours studied, plus realistic random noise, then saves it as `data/study_scores.csv`.
2. **Data prep** (`src/data_prep.py`): loads the CSV using NumPy, reshapes the feature column into the 2D shape scikit-learn requires, and splits it into training and test sets using `train_test_split`.
3. **Training** (`src/train.py`): fits a `LinearRegression` model on the training set only, then saves the trained model to `models/model.joblib` using `joblib` so it can be reused without retraining.
4. **Evaluation** (`src/evaluate.py`): loads the saved model, computes predictions on both the training and test sets, and reports MSE and R² for each, along with a plain-language verdict (good fit / possible overfitting / possible underfitting).
5. **Visualization** (`src/visualize.py`): plots the test set's actual values against the model's predicted values and saves a labeled chart to `outputs/results_chart.png`.
6. **Prediction** (`src/predict.py`): loads the saved model and produces a prediction for a new "hours studied" value passed via a command-line argument.

## Common Problems

- **`ModuleNotFoundError: No module named 'sklearn'`**: run `pip install -r requirements.txt` inside your active virtual environment.
- **`FileNotFoundError: data/study_scores.csv`**: run `python3 data/generate_data.py` first — the dataset is not committed to the repo, it is generated on demand.
- **`FileNotFoundError: models/model.joblib`**: run `python3 src/train.py` before running `evaluate.py` or `predict.py`.
- **Charts don't display when running scripts remotely/headlessly**: the scripts save charts to disk with `plt.savefig()` regardless of whether a display is available; open the resulting PNG file directly if `plt.show()` has no effect in your environment.
- **Different numbers than shown in this README**: the dataset uses a fixed random seed, but results can vary slightly between scikit-learn/NumPy versions — this is expected and not a bug.

## Extensions

- Add a second feature (e.g., "hours slept") to `data/generate_data.py` and `src/data_prep.py` and confirm the model still trains correctly with `X.shape` becoming `(n, 2)`.
- Try `PolynomialFeatures` combined with `LinearRegression` to fit curved relationships instead of a straight line.
- Swap `LinearRegression` for `Ridge` or `Lasso` regression and compare evaluation metrics.
- Add a `--csv` argument to `predict.py` to batch-predict scores for many students from a CSV file at once.
- Build a small command-line menu that lets a user choose to regenerate data, retrain, evaluate, or predict without remembering individual script names.
