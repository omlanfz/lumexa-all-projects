# Project 06: Sports Comparison Visualiser

**Course:** Lumexa Data Scientist Path — Course 14, Data Visualisation
**Tech:** Python, Pandas, Plotly

## Purpose
Build an interactive tool for comparing NBA teams using two real FiveThirtyEight datasets: player-level RAPTOR/WAR advanced statistics, and historical team Elo ratings. Applies Lessons 3 (statistical thinking), 4 (choosing the right chart — bar, line, and radar for different comparison questions), 5 (color/storytelling), and 6 (interactive Plotly).

## What Students Learn
- Aggregating real player-level data up to team-season statistics with `pandas.groupby()`.
- Building three distinct comparison chart types suited to three distinct questions: a bar chart (single-season team comparison), a multi-line chart (long-term franchise trend), and a radar/spider chart (multi-stat profile comparison).
- Normalizing multiple stats onto a comparable 0-1 scale for a fair radar chart.
- Working with two real datasets of very different shapes (player-season rows vs. team-game rows) and reconciling them into a coherent analysis.

## Tech Stack
- Python 3.10+
- pandas
- Plotly (Plotly Express + Graph Objects)

## Datasets
**1. Modern RAPTOR by Team** (player-season advanced stats)
- **Source:** FiveThirtyEight
- **URL:** https://raw.githubusercontent.com/fivethirtyeight/data/master/nba-raptor/modern_RAPTOR_by_team.csv
- **License:** FiveThirtyEight's data is published under Creative Commons Attribution 4.0 for educational/non-commercial reuse.
- **Kept in full** (no trimming needed): 7,289 rows x 23 columns, covering seasons 2014-2022, including both regular season and playoff rows for each player. Key columns used: `player_name`, `season`, `team`, `raptor_offense`, `raptor_defense`, `raptor_total`, `war_total`, `predator_offense`, `predator_defense`.

**2. NBA All Elo** (team game-by-game Elo ratings)
- **Source:** FiveThirtyEight
- **URL:** https://raw.githubusercontent.com/fivethirtyeight/data/master/nba-elo/nbaallelo.csv
- **License:** Same as above (FiveThirtyEight, CC BY 4.0).
- **Trimming note (real data only):** The full file contains 126,314 real team-game rows spanning 1947-2015 across every NBA/ABA franchise in history. To keep the file manageable for a classroom project, we filtered it down to 8 real, well-known franchises (**Lakers, Celtics, Warriors, Bulls, Spurs, Rockets, Heat, Cavaliers**), keeping **36,629 rows** — every value is a real, unmodified FiveThirtyEight measurement; only rows for other franchises were removed, nothing was invented.

**Inspected findings:**
- RAPTOR: 30 real NBA team abbreviations present (e.g., GSW, BOS, LAL, MIA); seasons run 2014-2022; no missing values in the core RAPTOR/WAR columns.
- ELO (trimmed): franchise-year Elo ratings run from 1947 to 2015 for the 8 kept franchises; the Lakers have the most rows (6,024) reflecting their long, mostly stable franchise history in Los Angeles/Minneapolis.

## Structure
```
06-sports-comparison-visualiser/
├── build_comparisons.py    # Main script - run this
├── data/
│   ├── modern_RAPTOR_by_team.csv
│   └── nbaallelo.csv        # Trimmed to 8 franchises (see above)
├── output/                  # Generated after running the script
│   ├── team_raptor_comparison.html
│   ├── team_elo_trend_comparison.html
│   └── team_radar_comparison.html
├── requirements.txt
└── README.md
```

## Install
```bash
cd projects/06-sports-comparison-visualiser
pip install -r requirements.txt
```

## How to Run
```bash
python build_comparisons.py
```
This prints dataset inspection details to the console and generates three interactive HTML files in `output/`.

## Expected Output
- **`team_raptor_comparison.html`**: an interactive bar chart comparing total team WAR (Wins Above Replacement, summed across each team's real roster) for GSW, BOS, LAL, and MIA in the most recent RAPTOR season (2022), with hover tooltips showing each team's average RAPTOR rating too.
- **`team_elo_trend_comparison.html`**: an interactive multi-line chart showing the Lakers, Celtics, Warriors, and Bulls' average season Elo rating from 1947 to 2015, letting you hover and zoom into any era (e.g., the Bulls' 1990s dynasty, or the Warriors' 2010s peak).
- **`team_radar_comparison.html`**: an interactive radar (spider) chart comparing the Warriors (GSW) and Celtics (BOS) across 5 normalized advanced stats (offensive/defensive RAPTOR, WAR, offensive/defensive predator) for the most recent season.

## Troubleshooting
- **`FileNotFoundError`**: confirm you're running from inside `projects/06-sports-comparison-visualiser/` so the relative `data/` paths resolve.
- **Radar chart looks flat/empty**: this happens if both compared teams have identical stats after normalization (unlikely with real data) — try changing `team_a`/`team_b` in the script to two different teams.
- **Team abbreviation not found**: RAPTOR uses standard 2-3 letter NBA abbreviations (e.g., `GSW`, `BOS`) while Elo uses franchise names (e.g., `"Warriors"`, `"Celtics"`) — these are two different naming schemes in the two source files and are handled separately in the script; don't mix them up if you customize the code.

## Extension Ideas
- Add a player-vs-player radar comparing two individual players' RAPTOR profiles instead of team averages.
- Merge both datasets by mapping team abbreviations to franchise names, to build one combined "team power ranking" that blends recent RAPTOR performance with historical Elo trend.
- Convert this into a small Dash app (following Lesson 7/8 patterns) with dropdowns for selecting which teams/players to compare, instead of hardcoded team lists in the script.

## Portfolio Tips
Link to all three interactive HTML files (or host them together on a simple static site) so viewers can explore different teams themselves. In your portfolio write-up, name both real datasets and their real row counts — concrete, verifiable data provenance is a strong signal in a data science portfolio.
