import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback

df = pd.read_csv("data/cleaned_all.csv")
df = df.dropna(subset=["latitude", "longitude", "arithmetic_mean"])

POLLUTANT_CONFIG = {
    "PM2.5": {"unit": "µg/m³", "label": "Annual Mean (µg/m³)"},
    "Ozone": {"unit": "ppm",   "label": "Annual Mean (ppm)"},
    "NO2":   {"unit": "ppb",   "label": "Annual Mean (ppb)"},
}

DESCRIPTIONS = {
    "PM2.5": "Fine particulate matter ≤2.5 µm. Penetrates deep into lungs.",
    "Ozone": "Ground-level ozone formed by pollutants reacting in sunlight.",
    "NO2":   "Nitrogen dioxide from vehicles and power plants.",
}

def build_figure(pollutant):
    subset = df[df["pollutant_name"] == pollutant]
    cfg = POLLUTANT_CONFIG[pollutant]

    fig = px.scatter_map(
        subset,
        lat="latitude",
        lon="longitude",
        color="arithmetic_mean",
        size="arithmetic_mean",
        size_max=18,
        color_continuous_scale=[
            [0.0,  "#4caf50"],
            [0.5,  "#ffeb3b"],
            [1.0,  "#f44336"],
        ],
        range_color=[subset["arithmetic_mean"].min(), subset["arithmetic_mean"].max()],
        hover_name="local_site_name",
        hover_data={
            "city": True,
            "county": True,
            "arithmetic_mean": ":.4f",
            "aqi_category": True,
            "observation_percent": ":.0f",
            "latitude": False,
            "longitude": False,
        },
        labels={
            "arithmetic_mean": cfg["label"],
            "aqi_category": "AQI Category",
            "observation_percent": "Coverage (%)",
        },
        map_style="carto-positron",
        center={"lat": 44.3, "lon": -85.0},
        zoom=5.8,
        height=600,
    )

    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font_family="'Inter', sans-serif",
        font_color="#111111",
        coloraxis_colorbar=dict(
            title=dict(text=cfg["unit"], font=dict(size=11, color="#666")),
            tickfont=dict(size=10, color="#666"),
            thickness=8,
            len=0.5,
            bgcolor="rgba(0,0,0,0)",
            outlinewidth=0,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={
        "backgroundColor": "#ffffff",
        "minHeight": "100vh",
        "fontFamily": "'Inter', sans-serif",
        "color": "#111111",
        "maxWidth": "1100px",
        "margin": "0 auto",
        "padding": "48px 32px",
    },
    children=[
        html.Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap"
        ),

        # Header
        html.Div(
            style={"marginBottom": "32px", "borderBottom": "1px solid #eee", "paddingBottom": "24px"},
            children=[
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-end"},
                    children=[
                        html.Div([
                            html.H1(
                                "Michigan Air Quality",
                                style={"fontSize": "28px", "fontWeight": "600",
                                       "margin": "0 0 4px 0", "letterSpacing": "-0.02em"}
                            ),
                            html.P(
                                id="subtitle",
                                style={"fontSize": "14px", "color": "#888", "margin": "0"}
                            ),
                            html.P(
                                "All sites within EPA 'Good' thresholds. Colors show relative variation across Michigan.",
                                style={"fontSize": "12px", "color": "#bbb", "margin": "4px 0 0 0"}
                            ),

                        ]),
                        html.Div([
                            dcc.Dropdown(
                                id="pollutant-dropdown",
                                options=[{"label": p, "value": p} for p in POLLUTANT_CONFIG],
                                value="PM2.5",
                                clearable=False,
                                style={
                                    "width": "160px",
                                    "fontSize": "13px",
                                    "border": "1px solid #e0e0e0",
                                    "borderRadius": "4px",
                                }
                            ),
                        ]),
                    ]
                ),
            ]
        ),

        # Stats
        html.Div(
            id="stats-row",
            style={"display": "flex", "gap": "40px", "marginBottom": "28px"},
        ),

        # Map
        html.Div(
            style={
                "borderRadius": "6px",
                "overflow": "hidden",
                "border": "1px solid #e8e8e8",
            },
            children=[dcc.Graph(id="map", config={"displayModeBar": False})]
        ),

        # Footer
        html.Div(
            "EPA Air Quality System (AQS) · Michigan · 2024 annual summary",
            style={"fontSize": "11px", "color": "#bbb", "marginTop": "16px", "textAlign": "right"}
        ),
    ]
)

def stat(value, label):
    return html.Div([
        html.Div(value, style={"fontSize": "20px", "fontWeight": "600", "letterSpacing": "-0.01em"}),
        html.Div(label, style={"fontSize": "11px", "color": "#999", "marginTop": "2px", "textTransform": "uppercase", "letterSpacing": "0.05em"}),
    ])

@callback(
    Output("map", "figure"),
    Output("subtitle", "children"),
    Output("stats-row", "children"),
    Input("pollutant-dropdown", "value"),
)
def update(pollutant):
    subset = df[df["pollutant_name"] == pollutant]
    cfg = POLLUTANT_CONFIG[pollutant]
    u = cfg["unit"]

    stats = [
        stat(str(len(subset)), "sites"),
        stat(f"{subset['arithmetic_mean'].mean():.3f} {u}", "statewide mean"),
        stat(f"{subset['first_max_value'].max():.2f} {u}", "highest peak"),
        stat(subset.loc[subset['first_max_value'].idxmax(), 'city'] or "N/A", "worst city"),
    ]

    return build_figure(pollutant), DESCRIPTIONS[pollutant], stats

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)