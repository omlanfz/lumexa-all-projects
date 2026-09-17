# Project 05: Market Trends Chart

**Course:** Lumexa Data Scientist Path — Course 14, Data Visualisation
**Tech:** Python, Pandas, Matplotlib, Seaborn, Plotly

## Purpose
Analyze and visualize a real historical stock price series (Apple, 2014), producing both a static (Matplotlib/Seaborn) chart and a fully interactive (Plotly) chart showing price trends, moving averages, and volatility — applying Lessons 2 (Matplotlib), 3 (Seaborn), 5 (storytelling/color), and 6 (Plotly).

## What Students Learn
- Loading and cleaning a real time-series CSV with pandas (parsing dates, sorting, renaming columns).
- Computing real derived metrics from real data: rolling (moving) averages and day-over-day percent change — never hardcoded numbers.
- Building a polished static Matplotlib/Seaborn chart with a headline title, multiple series, and a legend.
- Building the same insight as an interactive Plotly chart with unified hover tooltips.
- Using a histogram/KDE (Seaborn) to explore the distribution of daily returns.

## Tech Stack
- Python 3.10+
- pandas
- Matplotlib
- Seaborn
- Plotly

## Dataset
**Source:** Plotly's public sample datasets repository (historical Apple stock data)
**URL:** https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv
**License:** Published by Plotly as an open sample dataset for demos/education.

**Inspected findings:**
- Shape: 240 rows x 2 columns.
- Original column names are `AAPL_x` (date) and `AAPL_y` (closing price) — renamed to `date` and `close` in the script for clarity.
- Date range: **2014-01-02 to 2014-12-12** (240 real U.S. trading days — the dataset does not extend through the full calendar year).
- Closing price range across the year: **$69.00 to $118.80**.
- No missing values in either column.
- This is closing-price data only (no explicit volume column); the "volume proxy" idea mentioned in some course materials is represented here instead via the daily % change distribution chart, since no real volume column exists in this specific file — we do not fabricate a volume series.

## Structure
```
05-market-trends-chart/
├── build_charts.py     # Main script - run this
├── data/
│   └── apple_stock_2014.csv
├── output/              # Generated after running the script
│   ├── apple_stock_matplotlib.png
│   ├── apple_stock_plotly.html
│   └── apple_daily_change_distribution.png
├── requirements.txt
└── README.md
```

## Install
```bash
cd projects/05-market-trends-chart
pip install -r requirements.txt
```

## How to Run
```bash
python build_charts.py
```
This prints dataset inspection details to the console and generates three files in `output/`.

## Expected Output
- **`apple_stock_matplotlib.png`**: a static chart with the raw daily close price in light gray, a blue 10-day moving average, and a red 30-day moving average, with a headline title describing the year's overall upward trend and pullbacks.
- **`apple_stock_plotly.html`**: an interactive version of the same three series — open in any browser to hover over any date and see exact values for all three lines at once (`hovermode="x unified"`), and to zoom/pan into specific weeks or months.
- **`apple_daily_change_distribution.png`**: a histogram with a KDE overlay showing the distribution of Apple's daily percent price changes in 2014, mostly clustered near zero with a roughly bell-shaped spread.

## Troubleshooting
- **`FileNotFoundError` for the CSV**: confirm you're running the script from inside `projects/05-market-trends-chart/` (or that `data/apple_stock_2014.csv` exists relative to `build_charts.py`).
- **Empty/blank PNG**: ensure `plt.tight_layout()` runs before `plt.savefig()` (already handled in the script) and check the `output/` folder was created.
- **HTML file won't open interactively**: some corporate browsers block local file JavaScript; try a different browser or serve the file locally with `python -m http.server` from inside `output/`.

## Extension Ideas
- Extend the moving-average strategy into a simple "golden cross / death cross" signal marker (where the 10-day MA crosses the 30-day MA) plotted as annotated points.
- Find and load a second, longer real stock CSV (e.g., a multi-year series from another confirmed `raw.githubusercontent.com` source) to compare short-term (2014) vs. long-term trends.
- Add a candlestick chart using Plotly's `go.Candlestick` if you locate a real dataset that includes Open/High/Low/Close columns (this dataset only has Close).

## Portfolio Tips
Include both the static PNG (works anywhere, even in a PDF) and a link to the interactive HTML (great for a personal website or GitHub Pages) in your portfolio. Explicitly state in your portfolio caption that the moving averages are computed live from real data with pandas `.rolling()` — this signals real data-manipulation skill, not just chart styling.
