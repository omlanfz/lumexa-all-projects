"""
Project 04: Climate Change Dashboard
Course 14 - Data Visualisation | Lumexa Data Scientist Path

A real, runnable Dash app exploring CO2 emissions trends using Our World in Data's
public CO2 & climate dataset (trimmed to 8 countries + World, 1950-2024; see data/README
notes in this project's README.md for details on the trim).

Run with:  python app.py
Then open: http://127.0.0.1:8050
"""

import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "owid-co2-data.csv")

# ---------------------------------------------------------------------------
# Load & prepare the REAL dataset (no synthetic/fabricated numbers anywhere)
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df = df.dropna(subset=["co2", "co2_per_capita"])

countries = sorted(df["country"].unique().tolist())
default_country = "World" if "World" in countries else countries[0]

comparison_countries = [c for c in countries if c != "World"]
latest_year = int(df["year"].max())

app = Dash(__name__)
app.title = "Lumexa | Climate Change Dashboard"
server = app.server  # exposes the underlying Flask server for verification/testing

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1050px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1("Climate Change Dashboard", style={"textAlign": "center"}),
        html.P(
            "Explore real CO2 emissions data from Our World in Data (1950-2024) for the "
            "World and 7 major countries. Select a country below to update every chart.",
            style={"textAlign": "center", "color": "#555"},
        ),
        html.Div(
            style={"textAlign": "center", "margin": "16px 0"},
            children=[
                html.Label("Country / Region: ", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{"label": c, "value": c} for c in countries],
                    value=default_country,
                    clearable=False,
                    style={"width": "320px", "margin": "8px auto"},
                ),
            ],
        ),

        html.Div(id="kpi-row", style={"display": "flex", "justifyContent": "center",
                                       "gap": "24px", "flexWrap": "wrap", "margin": "20px 0"}),

        dcc.Graph(id="co2-trend-chart"),
        dcc.Graph(id="co2-source-chart"),

        html.H3("Country Comparison", style={"textAlign": "center", "marginTop": "36px"}),
        html.Div(
            style={"textAlign": "center", "margin": "10px 0 20px"},
            children=[
                html.Label("Compare countries: ", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id="compare-dropdown",
                    options=[{"label": c, "value": c} for c in comparison_countries],
                    value=["United States", "China", "India", "Germany"],
                    multi=True,
                    style={"width": "600px", "margin": "8px auto"},
                ),
            ],
        ),
        dcc.Graph(id="comparison-chart"),
        dcc.Graph(id="per-capita-chart"),

        html.P(
            f"Data source: Our World in Data CO2 & Greenhouse Gas Emissions dataset "
            f"(github.com/owid/co2-data), trimmed to 8 countries + World, 1950-{latest_year}. "
            f"Values are real, unmodified measurements for the rows kept.",
            style={"textAlign": "center", "color": "#999", "fontSize": "12px", "marginTop": "30px"},
        ),
    ],
)


def kpi_card(label, value):
    return html.Div(
        style={"border": "1px solid #ddd", "borderRadius": "8px", "padding": "14px 22px",
               "textAlign": "center", "minWidth": "150px"},
        children=[
            html.Div(label, style={"fontSize": "12px", "color": "#888"}),
            html.Div(value, style={"fontSize": "22px", "fontWeight": "bold"}),
        ],
    )


@app.callback(
    Output("kpi-row", "children"),
    Output("co2-trend-chart", "figure"),
    Output("co2-source-chart", "figure"),
    Input("country-dropdown", "value"),
)
def update_country_view(selected_country):
    sub = df[df["country"] == selected_country].sort_values("year")
    latest = sub.iloc[-1]
    earliest = sub.iloc[0]
    pct_change = (latest["co2"] - earliest["co2"]) / earliest["co2"] * 100 if earliest["co2"] else float("nan")

    kpis = [
        kpi_card("Latest Total CO2 (Mt)", f"{latest['co2']:.1f}"),
        kpi_card("CO2 per Capita (t)", f"{latest['co2_per_capita']:.2f}"),
        kpi_card(f"Change since {int(earliest['year'])}", f"{pct_change:+.0f}%"),
        kpi_card("Share of Global CO2", f"{latest.get('share_global_co2', float('nan')):.1f}%"
                 if pd.notna(latest.get('share_global_co2')) else "N/A"),
    ]

    trend_fig = px.line(
        sub, x="year", y="co2", markers=False,
        title=f"{selected_country}: Total CO2 Emissions, {int(earliest['year'])}-{int(latest['year'])}",
        labels={"year": "Year", "co2": "CO2 emissions (million tonnes)"},
        template="plotly_white",
    )
    trend_fig.update_traces(line_color="#2a9d8f", line_width=3)

    source_cols = ["coal_co2", "oil_co2", "gas_co2"]
    available_source_cols = [c for c in source_cols if c in sub.columns]
    source_df = sub[["year"] + available_source_cols].melt(id_vars="year", var_name="source", value_name="emissions")
    source_df["source"] = source_df["source"].str.replace("_co2", "", regex=False).str.title()
    source_fig = px.area(
        source_df, x="year", y="emissions", color="source",
        title=f"{selected_country}: CO2 Emissions by Fossil Fuel Source",
        labels={"year": "Year", "emissions": "CO2 emissions (million tonnes)", "source": "Source"},
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    return kpis, trend_fig, source_fig


@app.callback(
    Output("comparison-chart", "figure"),
    Output("per-capita-chart", "figure"),
    Input("compare-dropdown", "value"),
)
def update_comparison(selected_countries):
    if not selected_countries:
        selected_countries = ["World"]

    comp_df = df[df["country"].isin(selected_countries)].sort_values(["country", "year"])

    comparison_fig = px.line(
        comp_df, x="year", y="co2", color="country",
        title="Total CO2 Emissions Over Time: Country Comparison",
        labels={"year": "Year", "co2": "CO2 emissions (million tonnes)", "country": "Country"},
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set1,
    )

    per_capita_fig = px.line(
        comp_df, x="year", y="co2_per_capita", color="country",
        title="CO2 Emissions Per Capita: Country Comparison",
        labels={"year": "Year", "co2_per_capita": "CO2 per capita (tonnes)", "country": "Country"},
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set1,
    )

    return comparison_fig, per_capita_fig


if __name__ == "__main__":
    app.run(debug=True)
