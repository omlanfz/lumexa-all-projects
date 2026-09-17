"""
Project 06: Sports Comparison Visualiser
Course 14 - Data Visualisation | Lumexa Data Scientist Path

Uses two REAL FiveThirtyEight NBA datasets:
  - modern_RAPTOR_by_team.csv : player-season RAPTOR/WAR advanced stats, 2014-2022 (kept in full)
  - nbaallelo.csv              : team game-by-game Elo ratings, 1947-2015 (trimmed to 8 real
                                  franchises: Lakers, Celtics, Warriors, Bulls, Spurs, Rockets,
                                  Heat, Cavaliers - all rows kept for those franchises are real,
                                  unmodified FiveThirtyEight rows)

Produces:
  - output/team_raptor_comparison.html   (interactive Plotly bar comparison of team RAPTOR/WAR)
  - output/team_elo_trend_comparison.html (interactive Plotly line chart of Elo over time)
  - output/team_radar_comparison.html    (interactive Plotly radar chart, multi-stat comparison)

Run with: python build_comparisons.py
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

HERE = os.path.dirname(__file__)
RAPTOR_PATH = os.path.join(HERE, "data", "modern_RAPTOR_by_team.csv")
ELO_PATH = os.path.join(HERE, "data", "nbaallelo.csv")
OUT_DIR = os.path.join(HERE, "output")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Load REAL datasets
# ---------------------------------------------------------------------------
raptor = pd.read_csv(RAPTOR_PATH)
elo = pd.read_csv(ELO_PATH)

print(f"RAPTOR: {raptor.shape[0]} real player-season rows, seasons {raptor['season'].min()}-{raptor['season'].max()}")
print(f"ELO:    {elo.shape[0]} real team-game rows, years {elo['year_id'].min()}-{elo['year_id'].max()}")
print(f"ELO franchises kept: {sorted(elo['fran_id'].unique())}")

# ---------------------------------------------------------------------------
# 1. TEAM RAPTOR COMPARISON: aggregate real player RAPTOR to team-season level
# ---------------------------------------------------------------------------
team_season = (
    raptor.groupby(["team", "season"], as_index=False)
    .agg(team_raptor_total=("raptor_total", "mean"), team_war_total=("war_total", "sum"))
)

teams_to_compare = ["GSW", "BOS", "LAL", "MIA"]
latest_season = int(raptor["season"].max())

latest_team_stats = team_season[
    (team_season["team"].isin(teams_to_compare)) & (team_season["season"] == latest_season)
].sort_values("team_war_total", ascending=False)

fig_bar = px.bar(
    latest_team_stats, x="team", y="team_war_total",
    color="team", color_discrete_sequence=px.colors.qualitative.Set2,
    title=f"Total Team WAR (Wins Above Replacement) in {latest_season}: Real RAPTOR Data",
    labels={"team": "Team", "team_war_total": "Total WAR (summed across roster)"},
    template="plotly_white",
    hover_data={"team_raptor_total": ":.2f"},
)
fig_bar.write_html(os.path.join(OUT_DIR, "team_raptor_comparison.html"))
print("Saved: team_raptor_comparison.html")

# ---------------------------------------------------------------------------
# 2. FRANCHISE ELO TREND COMPARISON: real season-end Elo over time
# ---------------------------------------------------------------------------
season_end_elo = (
    elo.groupby(["fran_id", "year_id"], as_index=False)["elo_n"].mean()
    .rename(columns={"elo_n": "avg_elo"})
)

franchises_to_compare = ["Lakers", "Celtics", "Warriors", "Bulls"]
elo_sub = season_end_elo[season_end_elo["fran_id"].isin(franchises_to_compare)]

fig_line = px.line(
    elo_sub, x="year_id", y="avg_elo", color="fran_id",
    title="NBA Franchise Elo Rating Over Time (Real FiveThirtyEight Data)",
    labels={"year_id": "Season year", "avg_elo": "Average Elo rating", "fran_id": "Franchise"},
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Set1,
)
fig_line.update_layout(hovermode="x unified")
fig_line.write_html(os.path.join(OUT_DIR, "team_elo_trend_comparison.html"))
print("Saved: team_elo_trend_comparison.html")

# ---------------------------------------------------------------------------
# 3. RADAR CHART: multi-stat comparison of two teams in the latest RAPTOR season
# ---------------------------------------------------------------------------
radar_stats = ["raptor_offense", "raptor_defense", "war_total", "predator_offense", "predator_defense"]
team_a, team_b = "GSW", "BOS"

radar_df = (
    raptor[(raptor["season"] == latest_season) & (raptor["team"].isin([team_a, team_b]))]
    .groupby("team")[radar_stats].mean()
)

# Normalize each stat to 0-1 across the two teams so the radar shape is comparable
radar_norm = (radar_df - radar_df.min()) / (radar_df.max() - radar_df.min() + 1e-9)

fig_radar = go.Figure()
for team in [team_a, team_b]:
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_norm.loc[team].values.tolist() + [radar_norm.loc[team].values[0]],
        theta=radar_stats + [radar_stats[0]],
        fill="toself",
        name=team,
    ))
fig_radar.update_layout(
    title=f"{team_a} vs {team_b}: Advanced Stat Profile ({latest_season} season, normalized)",
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    template="plotly_white",
)
fig_radar.write_html(os.path.join(OUT_DIR, "team_radar_comparison.html"))
print("Saved: team_radar_comparison.html")

print("\nAll comparison visualisations built successfully from real NBA data.")
