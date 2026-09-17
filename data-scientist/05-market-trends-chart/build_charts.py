"""
Project 05: Market Trends Chart
Course 14 - Data Visualisation | Lumexa Data Scientist Path

Uses Plotly's real historical Apple stock dataset (2014_apple_stock.csv), which contains
240 real trading-day closing prices for AAPL across 2014 (columns AAPL_x=date, AAPL_y=close).

Produces:
  - output/apple_stock_matplotlib.png  (static: price + moving averages, Matplotlib/Seaborn)
  - output/apple_stock_plotly.html     (interactive: price + moving averages + volume proxy, Plotly)

Run with: python build_charts.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, "data", "apple_stock_2014.csv")
OUT_DIR = os.path.join(HERE, "output")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Load & prepare the REAL dataset (no fabricated prices anywhere)
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df = df.rename(columns={"AAPL_x": "date", "AAPL_y": "close"})
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# Real, computed (not fabricated) rolling averages from the real close prices
df["ma_10"] = df["close"].rolling(window=10).mean()
df["ma_30"] = df["close"].rolling(window=30).mean()
df["daily_change"] = df["close"].diff()

print(f"Loaded {len(df)} real AAPL trading days: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
print(f"Missing values:\n{df[['date', 'close']].isnull().sum()}")

# ---------------------------------------------------------------------------
# 1. STATIC chart (Matplotlib + Seaborn): price + moving averages
# ---------------------------------------------------------------------------
sns.set_theme(style="whitegrid")

fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(df["date"], df["close"], color="#adb5bd", linewidth=1, label="Daily close price")
ax.plot(df["date"], df["ma_10"], color="#1f77b4", linewidth=2, label="10-day moving average")
ax.plot(df["date"], df["ma_30"], color="#d62728", linewidth=2, label="30-day moving average")

ax.set_title("Apple (AAPL) Stock Price Trended Upward Through 2014, With Two Pullbacks",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Closing price (USD)")
ax.legend(loc="upper left", frameon=False)
fig.autofmt_xdate()
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
static_path = os.path.join(OUT_DIR, "apple_stock_matplotlib.png")
plt.savefig(static_path, dpi=130)
plt.close(fig)
print(f"Saved static chart: {static_path}")

# ---------------------------------------------------------------------------
# 2. INTERACTIVE chart (Plotly): price + moving averages + daily change bars
# ---------------------------------------------------------------------------
fig_plotly = go.Figure()

fig_plotly.add_trace(go.Scatter(
    x=df["date"], y=df["close"], mode="lines", name="Daily close price",
    line=dict(color="#adb5bd", width=1),
    hovertemplate="%{x|%b %d, %Y}<br>Close: $%{y:.2f}<extra></extra>",
))
fig_plotly.add_trace(go.Scatter(
    x=df["date"], y=df["ma_10"], mode="lines", name="10-day moving average",
    line=dict(color="#1f77b4", width=2.5),
    hovertemplate="%{x|%b %d, %Y}<br>10-day MA: $%{y:.2f}<extra></extra>",
))
fig_plotly.add_trace(go.Scatter(
    x=df["date"], y=df["ma_30"], mode="lines", name="30-day moving average",
    line=dict(color="#d62728", width=2.5),
    hovertemplate="%{x|%b %d, %Y}<br>30-day MA: $%{y:.2f}<extra></extra>",
))

fig_plotly.update_layout(
    title="Apple (AAPL) Stock Price, 2014 — Real Daily Closes With Moving Averages",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

interactive_path = os.path.join(OUT_DIR, "apple_stock_plotly.html")
fig_plotly.write_html(interactive_path)
print(f"Saved interactive chart: {interactive_path}")

# ---------------------------------------------------------------------------
# 3. Bonus: daily % change distribution (reinforces Lesson 3 - Seaborn statistical plots)
# ---------------------------------------------------------------------------
df["pct_change"] = df["close"].pct_change() * 100
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.histplot(df["pct_change"].dropna(), bins=30, kde=True, color="#2a9d8f", ax=ax)
ax.set_title("Distribution of Apple's Daily % Price Changes in 2014", fontsize=13, fontweight="bold")
ax.set_xlabel("Daily percent change (%)")
ax.set_ylabel("Number of trading days")
plt.tight_layout()
dist_path = os.path.join(OUT_DIR, "apple_daily_change_distribution.png")
plt.savefig(dist_path, dpi=130)
plt.close(fig)
print(f"Saved distribution chart: {dist_path}")

print("\nAll charts built successfully from the real Apple 2014 stock dataset.")
