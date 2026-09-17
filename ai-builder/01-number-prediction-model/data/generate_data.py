"""
generate_data.py
Lumexa Number Prediction Model - Synthetic Dataset Generator

Creates a realistic synthetic dataset relating "hours studied" (feature)
to "test score" (label) and saves it as data/study_scores.csv.

Run with:
    python3 data/generate_data.py
"""

import csv
import os

import numpy as np

# --- Configuration ---
NUM_SAMPLES = 200
NOISE_LEVEL = 6.0        # standard deviation of random noise added to scores
RANDOM_SEED = 42
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "study_scores.csv")

# The "true" underlying relationship we simulate:
# score = BASE_SCORE + (HOURS_COEFFICIENT * hours_studied) + noise
BASE_SCORE = 42.0
HOURS_COEFFICIENT = 5.1


def generate_dataset(num_samples=NUM_SAMPLES, noise_level=NOISE_LEVEL, seed=RANDOM_SEED):
    """Generates a synthetic (hours_studied, test_score) dataset.

    Returns:
        hours_studied (np.ndarray): 1D array of study hours, shape (num_samples,)
        test_scores (np.ndarray): 1D array of test scores, shape (num_samples,)
    """
    rng = np.random.default_rng(seed)

    # Hours studied: uniformly distributed between 0 and 12 hours.
    hours_studied = rng.uniform(low=0.0, high=12.0, size=num_samples)
    hours_studied = np.round(hours_studied, 2)

    # Test scores: linear relationship plus Gaussian noise, clipped to 0-100.
    noise = rng.normal(loc=0.0, scale=noise_level, size=num_samples)
    test_scores = BASE_SCORE + (HOURS_COEFFICIENT * hours_studied) + noise
    test_scores = np.clip(test_scores, 0, 100)
    test_scores = np.round(test_scores, 1)

    return hours_studied, test_scores


def save_to_csv(hours_studied, test_scores, output_path=OUTPUT_PATH):
    """Saves the dataset to a CSV file with columns: hours_studied, test_score."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["hours_studied", "test_score"])
        for hours, score in zip(hours_studied, test_scores):
            writer.writerow([hours, score])


def main():
    hours_studied, test_scores = generate_dataset()
    save_to_csv(hours_studied, test_scores)
    print(f"Generated {len(hours_studied)} samples.")
    print(f"Saved dataset to: {OUTPUT_PATH}")
    print(f"Sample rows:")
    for i in range(5):
        print(f"  hours_studied={hours_studied[i]:.2f}, test_score={test_scores[i]:.1f}")


if __name__ == "__main__":
    main()
