# Project 1: Sports Performance Analysis

Part of **Lumexa Data Scientist Path — Course 13: Python for Data**.

## Purpose
Analyze real NBA/BAA team performance across nearly 80 seasons using the FiveThirtyEight
NBA Elo dataset, applying the full data science workflow: load, inspect, clean, filter, sort,
aggregate, and statistically summarize real sports data to reach genuine, evidence-based
conclusions.

## What Students Learn
- Loading and inspecting a large real-world CSV dataset (126,000+ rows).
- Cleaning real missing data (a mostly-empty `notes` column) and confirming there are no duplicates.
- Filtering and sorting to isolate specific teams, seasons, and game types (e.g., high-scoring playoff games).
- Aggregating with `.groupby()` and `pd.pivot_table()` to compare franchises and seasons.
- Computing statistical summaries and correlation (e.g., Elo rating vs. points scored) and
  interpreting the results carefully, without overstating causation.

## Tech
Python 3, pandas, numpy, Jupyter Notebook.

## Dataset
- **File:** `data/nbaallelo.csv`
- **Source:** FiveThirtyEight's public NBA Elo dataset —
  https://raw.githubusercontent.com/fivethirtyeight/data/master/nba-elo/nbaallelo.csv
- **License:** FiveThirtyEight's open data, published for public analysis (see FiveThirtyEight's data GitHub repository for full terms).
- **Columns:** `gameorder`, `game_id`, `lg_id`, `_iscopy`, `year_id`, `date_game`, `seasongame`,
  `is_playoffs`, `team_id`, `fran_id`, `pts`, `elo_i`, `elo_n`, `win_equiv`, `opp_id`, `opp_fran`,
  `opp_pts`, `opp_elo_i`, `opp_elo_n`, `game_location`, `game_result`, `forecast`, `notes`.
- **Real, inspected findings:**
  - Shape: **126,314 rows × 23 columns**.
  - Missing values: only `notes` has any (**120,890 missing, ~95.7%**) — expected, since it's
    only populated for unusual games. Filled with `"none"` rather than dropped.
  - Duplicate rows: **0**.
  - Covers every NBA/BAA season from **1946-47 through 2015 (as recorded in this dataset version)**.

> **Note on this copy:** at 18MB, this raw CSV was too large to include directly inside the
> delivered ZIP alongside everything else. Run `data/download_dataset.sh` once (or manually
> `curl -L -o data/nbaallelo.csv https://raw.githubusercontent.com/fivethirtyeight/data/master/nba-elo/nbaallelo.csv`)
> before opening `analysis.ipynb` — the notebook expects the file at exactly `data/nbaallelo.csv`.
> This is the same real, complete dataset described above; nothing about it has been altered or trimmed.

## Structure
```
01-sports-performance-analysis/
├── analysis.ipynb        # Executed notebook with real outputs
├── data/
│   └── nbaallelo.csv      # Real dataset (downloaded from FiveThirtyEight)
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
Running the notebook end-to-end prints: dataset shape and column list, missing-value and
duplicate counts, cleaned data confirmation, filtered high-scoring playoff games, Celtics
season-by-season scoring, top-10 franchises by all-time wins, a team scoring summary table,
a pivot table of average points by franchise/season, `.describe()` statistics for points
scored, a correlation matrix between Elo ratings and points, the single highest post-game Elo
rating ever recorded (the 1995-96 Chicago Bulls), and a final written conclusions section.

## Troubleshooting
- **`FileNotFoundError` for `data/nbaallelo.csv`**: make sure you run the notebook from inside
  the `01-sports-performance-analysis/` folder so the relative path `data/nbaallelo.csv` resolves.
- **Missing packages**: run `pip install -r requirements.txt` again; if Jupyter itself is missing, `pip install notebook`.
- **Notebook won't execute headlessly**: confirm `nbconvert` is installed (`pip show nbconvert`).

## Extension Challenges
- Analyze whether playoff-game scoring differs systematically from regular-season scoring.
- Build a pivot table of team win rate (not just win count) by season.
- Investigate whether `forecast` (FiveThirtyEight's predicted win probability) correlates with actual game outcomes.

## Portfolio Tips
Present this project by leading with the headline finding (e.g., "the Lakers and Celtics have
the most wins in NBA history in this dataset") and the pivot table visualization, then walk
through your cleaning decisions — being explicit about *why* you filled rather than dropped
missing `notes` values shows real data science judgment, not just code fluency.
