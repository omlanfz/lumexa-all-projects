# Project 2: School Grade Analysis

Part of **Lumexa Data Scientist Path — Course 13: Python for Data**.

## Purpose
Analyze real student exam performance data across math, reading, and writing scores, applying
the full data science workflow to explore how demographic and preparation factors relate to
academic performance — while carefully distinguishing correlation from causation.

## Honest Note on the Dataset
This project's brief asked us to genuinely search for a real, accessible mirror of the popular
"Students Performance in Exams" dataset (originally published on Kaggle by user `spscientist`,
https://www.kaggle.com/datasets/spscientist/students-performance-in-exams) on
`raw.githubusercontent.com`. We tested over 20 candidate URLs across many GitHub users/orgs.
**One genuine, working mirror was found and verified with `curl` before use**:

```
https://raw.githubusercontent.com/rashida048/Datasets/master/StudentsPerformance.csv
```
(HTTP 200, verified reachable; downloaded directly — 1,000 rows, matching the well-known
"Students Performance in Exams" schema exactly.)

The real file is shipped in this project at `data/StudentsPerformance.csv` — **no fabricated
data was used or is shipped**. If this mirror ever becomes unavailable in the future, the
original dataset can always be downloaded directly from Kaggle:
1. Go to https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
2. Download `StudentsPerformance.csv`
3. Place it at `projects/02-school-grade-analysis/data/StudentsPerformance.csv`
   (the notebook expects exactly this filename and path, and will run immediately once the
   file is present).

## What Students Learn
- Loading and inspecting a real, clean student-record dataset.
- Confirming data quality (no missing values, no duplicates) rather than assuming it.
- Filtering students by test preparation status and by an "at-risk" score threshold.
- Aggregating average scores by gender, test preparation status, and parental education level.
- Computing correlation between math, reading, and writing scores, and interpreting the
  results without overstating cause and effect.

## Tech
Python 3, pandas, numpy, Jupyter Notebook.

## Dataset
- **File:** `data/StudentsPerformance.csv`
- **Source (as shipped):** verified real mirror at
  https://raw.githubusercontent.com/rashida048/Datasets/master/StudentsPerformance.csv
- **Original dataset:** "Students Performance in Exams" by Kaggle user `spscientist`
  (free/open license) — https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
- **Columns:** `gender`, `race/ethnicity`, `parental level of education`, `lunch`,
  `test preparation course`, `math score`, `reading score`, `writing score`.
- **Real, inspected findings:**
  - Shape: **1,000 rows × 8 columns**.
  - Missing values: **0**. Duplicate rows: **0**.

## Structure
```
02-school-grade-analysis/
├── analysis.ipynb              # Executed notebook with real outputs
├── data/
│   └── StudentsPerformance.csv  # Real dataset (verified GitHub mirror)
├── requirements.txt
└── README.md
```

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
jupyter notebook analysis.ipynb
# or, to re-execute headlessly and verify it still runs end-to-end:
jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
```

## Expected Output
Running the notebook prints: dataset shape, null/duplicate checks, a derived "average score"
column, filtered views (top scorers who completed test prep; at-risk students below 60 average),
group averages by gender (~69.6 female vs. ~65.8 male in this dataset), by test preparation
status (~72.7 completed vs. ~65.0 none), and by parental education level (rising from ~63.1 to
~73.6 as education level increases), a pivot table of average math score by gender and test
prep status, `.describe()` statistics, and a correlation matrix showing reading/writing scores
very strongly correlated (~0.95) and math moderately-to-strongly correlated with both (~0.80–0.82).

## Troubleshooting
- **`FileNotFoundError` for `data/StudentsPerformance.csv`**: run the notebook from inside the
  `02-school-grade-analysis/` folder, or download the file per the Kaggle instructions above and
  place it at the exact path shown.
- **Missing packages**: `pip install -r requirements.txt`.

## Extension Challenges
- Investigate whether `lunch` type (a rough proxy for socioeconomic status in this dataset)
  correlates with average score.
- Build a pivot table of average score by `race/ethnicity` group and test prep status combined.
- Explore whether the score gap between test-prep-completed and non-completed students differs
  by parental education level.

## Portfolio Tips
When presenting this project, always phrase demographic findings as *observed patterns in this
specific dataset*, never as general claims about ability — this is both scientifically correct
and the kind of careful, responsible framing real employers look for in a junior data analyst.
