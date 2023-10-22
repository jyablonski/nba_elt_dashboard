from dash import dash_table, dcc, html

from src.data_cols.standings import standings_columns
from src.data import standings_df

# it's not baaaaaaad idk
overview_layout = (
    html.Div(
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
            html.Div(
                [
                    # Left side (Western Conference)
                    html.Div(
                        [
                            html.H1("Western Conference"),
                            dash_table.DataTable(
                                id="western-standings-table",
                                columns=standings_columns,
                                data=standings_df.query(
                                    'conference == "Western"'
                                ).to_dict("records"),
                                hidden_columns=[
                                    "active_protocols",
                                    "conference",
                                    "team",
                                ],
                                css=[
                                    {"selector": ".show-hide", "rule": "display: none"}
                                ],
                            ),
                        ],
                        style={
                            "width": "49%",
                            "display": "inline-block",
                            "margin-right": "30px",
                        },
                    ),
                    # Right side (Eastern Conference)
                    html.Div(
                        [
                            html.H1("Eastern Conference"),
                            dash_table.DataTable(
                                id="eastern-standings-table",
                                columns=standings_columns,
                                data=standings_df.query(
                                    'conference == "Eastern"'
                                ).to_dict("records"),
                                hidden_columns=[
                                    "active_protocols",
                                    "conference",
                                    "team",
                                ],
                                css=[
                                    {"selector": ".show-hide", "rule": "display: none"}
                                ],
                            ),
                        ],
                        style={"width": "49%", "display": "inline-block"},
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="player-scoring-efficiency-plot",
                        config={
                            "displayModeBar": False
                        },  # Optional: Hide the plotly toolbar
                        style={"width": "50%", "display": "inline-block"},
                    ),
                    dcc.Graph(
                        id="team-ratings-plot",
                        config={
                            "displayModeBar": False
                        },  # Optional: Hide the plotly toolbar
                        style={"width": "50%", "display": "inline-block"},
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="player-value-analysis-plot",
                        config={
                            "displayModeBar": False
                        },  # Optional: Hide the plotly toolbar
                        style={"width": "50%", "display": "inline-block"},
                    ),
                    dcc.Graph(
                        id="contract-bar-plot",
                        config={
                            "displayModeBar": False
                        },  # Optional: Hide the plotly toolbar
                        style={"width": "50%", "display": "inline-block"},
                    ),
                ]
            ),
        ],
        className="custom-padding",
    ),
)
