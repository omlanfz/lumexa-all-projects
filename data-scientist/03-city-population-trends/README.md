# Project 3: City Population Trends

Part of **Lumexa Data Scientist Path — Course 13: Python for Data**.

## Purpose
Analyze real, long-run population data across countries and regions worldwide, applying the
full data science workflow to uncover growth trends, top/bottom populations, and correlations
between year and population size.

## Honest Note on "City" Scope
Per this project's brief, the real, freely-accessible dataset used here (`datasets/population`
on GitHub, sourced from the World Bank) is **country/region-level**, not city-level. No genuine
city-level population CSV was found accessible on `raw.githubusercontent.com`, and rather than
fabricate city data, this project uses the real country/region dataset and treats "city" loosely
as "place/region" population trends, as explicitly permitted by the project brief. This is
stated plainly here rather than disguised.

## What Students Learn
- Loading and inspecting a real World Bank dataset spanning 65 years (1960–2024).
- Recognizing and separating true countries from statistical aggregate regions (e.g. "World",
  "Middle income") that are mixed into the same column — a realistic, important real-world data
  cleaning challenge.
- Filtering and sorting to find the most and least populous countries in the latest year.
- Aggregating and pivoting population by country and decade to track long-run growth.
- Computing correlation between year and population, and distinguishing total population size
  from population *growth rate*.

## Tech
Python 3, pandas, numpy, Jupyter Notebook.

## Dataset
- **File:** `data/population.csv`
- **Source:** the "datasets" GitHub organization's population dataset (World Bank data) —
  https://raw.githubusercontent.com/datasets/population/master/data/population.csv
- **License:** Published under the Frictionless Data / datasets.io open data initiative, itself
  derived from World Bank Open Data (CC BY 4.0).
- **Columns:** `Country Name`, `Country Code`, `Year`, `Value` (population count).
- **Real, inspected findings:**
  - Shape: **17,195 rows × 4 columns**.
  - Missing values: **0**. Duplicate rows: **0**.
  - **265 unique named places** (a mix of true countries and World Bank aggregate regions),
    covering years **1960–2024**.

## Structure
```
03-city-population-trends/
├── analysis.ipynb        # Executed notebook with real outputs
├── data/
│   └── population.csv     # Real dataset (World Bank, via the datasets.io GitHub org)
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
Running the notebook prints: dataset shape and null/duplicate checks, a list separating true
countries from World Bank aggregate regions, the top 10 and bottom 10 most/least populous
countries in the latest year (2024), a pivot table tracking India/China/United States
population by decade since 1960, percentage growth for each of those three countries, overall
population summary statistics, the correlation between year and world population (very close
to 1.0), and year-over-year world population growth rate for the most recent decade — ending
with a written conclusions section.

## Troubleshooting
- **`FileNotFoundError` for `data/population.csv`**: run the notebook from inside the
  `03-city-population-trends/` folder.
- **Aggregate regions appearing in "top country" results**: confirm the `aggregate_names`
  exclusion list in the notebook is applied before ranking — this is a deliberate cleaning step,
  not a bug, and is explained in Section 3 of the notebook.
- **Missing packages**: `pip install -r requirements.txt`.

## Extension Challenges
- Add more countries to the growth-rate comparison and rank them by percentage growth since 1960.
- Investigate which decade had the fastest global population growth rate.
- Merge in a second real dataset (e.g., land area) to compute population density trends.

## Portfolio Tips
Be upfront in any presentation of this project about the country-vs-city scope decision — data
scientists are expected to clearly document dataset limitations rather than hide them, and doing
so here demonstrates real professional judgment.
