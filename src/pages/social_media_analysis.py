from dash import dash_table, dcc, html

from src.data_cols.standings import standings_columns
from src.data import standings_df

social_media_analysis_layout = html.Div(
    [
        # Single div to contain all four KPIs
        html.Div(
            [
                # KPI 1
                html.Div(
                    [
                        html.Div("KPI 1 Value", style={"fontSize": 24}),
                        html.Div("KPI 1 Description"),
                    ],
                    className="kpi-box",
                ),
                # KPI 2
                html.Div(
                    [
                        html.Div("KPI 2 Value", style={"fontSize": 24}),
                        html.Div("KPI 2 Description"),
                    ],
                    className="kpi-box",
                ),
                # KPI 3
                html.Div(
                    [
                        html.Div("KPI 3 Value", style={"fontSize": 24}),
                        html.Div("KPI 3 Description"),
                    ],
                    className="kpi-box",
                ),
                # KPI 4
                html.Div(
                    [
                        html.Div("KPI 4 Value", style={"fontSize": 24}),
                        html.Div("KPI 4 Description"),
                    ],
                    className="kpi-box",
                ),
            ],
            className="kpi-container",
            style={"display": "flex", "justify-content": "space-between"},
        ),
    ],
    className="custom-padding",
)
