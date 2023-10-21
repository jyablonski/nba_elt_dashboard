from dash import html, dcc
import dash_table

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
                            html.H1("Western Conference Standings"),
                            dash_table.DataTable(
                                id="western-standings-table",
                                columns=[
                                    {"name": col, "id": col}
                                    for col in standings_df.columns
                                ],
                                data=standings_df.query(
                                    'conference == "Western"'
                                ).to_dict("records"),
                            ),
                        ],
                        style={"width": "49%", "display": "inline-block"},
                    ),
                    # Right side (Eastern Conference)
                    html.Div(
                        [
                            html.H1("Eastern Conference Standings"),
                            dash_table.DataTable(
                                id="eastern-standings-table",
                                columns=[
                                    {"name": col, "id": col}
                                    for col in standings_df.columns
                                ],
                                data=standings_df.query(
                                    'conference == "Eastern"'
                                ).to_dict("records"),
                            ),
                        ],
                        style={"width": "49%", "display": "inline-block"},
                    ),
                ]
            ),
        ]
    ),
)
