# Project 04: Climate Change Dashboard

**Course:** Lumexa Data Scientist Path — Course 14, Data Visualisation
**Tech:** Python, Pandas, Plotly, Dash

## Purpose
Build a real, interactive web dashboard exploring how CO2 emissions have changed over time across major countries, using Our World in Data's public climate dataset. This project is the capstone application of Lessons 6-8 (Interactive charts with Plotly, Building a Dash dashboard, Final dashboard).

## What Students Learn
- Loading, cleaning, and filtering a real-world CSV dataset with pandas.
- Building a multi-page-feeling, single-page Dash app with dropdown-driven callbacks.
- Designing linked interactivity: one dropdown updates multiple charts and KPI cards at once.
- Choosing chart types (line for trends, stacked area for composition, multi-line for comparison) appropriate to each question, per Lesson 4's decision framework.
- Applying honest, accessible color choices per Lesson 5.

## Tech Stack
- Python 3.10+
- pandas
- Plotly (Plotly Express + Graph Objects)
- Dash

## Dataset
**Source:** Our World in Data, CO2 and Greenhouse Gas Emissions dataset
**URL:** https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv
**License:** Our World in Data publishes this dataset under a Creative Commons BY license; it aggregates data from the Global Carbon Project and other sources.

**Trimming note (real data only, no fabrication):** The full upstream file contains 50,411 rows across 254 countries/regions and years 1750-2024 (79 columns). To keep the dataset small and classroom-friendly, we filtered it down to 8 real countries/regions (**World, United States, China, India, Germany, Brazil, Australia, United Kingdom**) and years **1950-2024**, keeping 18 relevant columns (population, gdp, co2, co2_per_capita, cumulative_co2, coal/oil/gas_co2, methane, nitrous_oxide, temperature_change_from_co2, share_global_co2, energy metrics). This produced **600 rows** — every value is a real, unmodified measurement from the original OWID file; no numbers were invented, only rows/columns were removed.

**Inspected findings:**
- Shape after trim: 600 rows x 18 columns (75 years x 8 countries/regions).
- `iso_code` is null for "World" (expected — it's an aggregate, not a country).
- `gdp` has 74 missing values (some countries/years lack GDP estimates in the source data).
- `energy_per_capita` and `primary_energy_consumption` have 120 missing values combined (early-year gaps in OWID's energy data).
- `co2` and `co2_per_capita` have zero missing values across the kept rows and are used as the dashboard's primary metrics.

## Structure
```
04-climate-change-dashboard/
├── app.py              # The Dash application (run this)
├── data/
│   └── owid-co2-data.csv   # Real, trimmed OWID dataset (600 rows)
├── requirements.txt
└── README.md
```

## Install
```bash
cd projects/04-climate-change-dashboard
pip install -r requirements.txt
```

## How to Run
```bash
python app.py
```
Then open **http://127.0.0.1:8050** in a browser.

## What the Dashboard Does
- A **country/region dropdown** at the top drives 4 KPI cards (latest total CO2, CO2 per capita, % change since 1950, share of global CO2) plus two charts: a CO2 emissions trend line and a stacked-area chart breaking emissions down by fossil fuel source (coal/oil/gas).
- A second, independent **multi-select dropdown** lets you pick 2+ countries to compare on two more charts: total CO2 over time, and CO2 per capita over time — both as multi-line comparisons.
- All charts and KPI values update instantly and are computed live from the real CSV — nothing is hardcoded.

## Expected Output
Visiting the app shows a title, the country dropdown (default "World"), four KPI cards, a green CO2 trend line, and a colored stacked-area chart. Below that, a comparison section defaults to United States/China/India/Germany, showing two multi-colored line charts. Switching either dropdown updates the relevant charts with no page reload.

## Troubleshooting
- **Port already in use**: run `app.run(debug=True, port=8060)` (edit the last line of `app.py`) or stop whatever else is using port 8050.
- **`ModuleNotFoundError: dash`**: run `pip install -r requirements.txt` in the same Python environment you're using to launch the app.
- **Blank charts**: confirm `data/owid-co2-data.csv` exists and has not been accidentally modified — re-download from the URL above if needed.
- **Charts show "N/A" for share of global CO2**: this happens for years/countries where `share_global_co2` is null in the source data; this is expected and reflects real data gaps, not a bug.

## Extension Ideas
- Add a `dcc.RangeSlider` to filter the year range shown in each chart.
- Add a per-capita vs. total CO2 scatter chart, colored by country, to explore the relationship between population size and emissions.
- Deploy the app publicly using a service like Render or PythonAnywhere so it's shareable via a public URL.

## Portfolio Tips
Screenshot the dashboard in 2-3 different dropdown states (e.g., "World" and "China") to show the interactivity in a static portfolio (like a PDF resume or GitHub README), but always link to the live/runnable code so reviewers can try it themselves. Mention the specific real dataset and its size in your portfolio description — "built on Our World in Data's public CO2 dataset" is a concrete, credible detail employers look for.
