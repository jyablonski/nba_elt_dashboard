from dash import dash_table, dcc, html

from src.data_cols.standings import standings_columns
from src.data import bans_df, standings_df

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
                            html.Div(
                                f"{bans_df['tot_wins'][0]} - {bans_df['tot_wins'][1]}",
                                style={"fontSize": 24},
                            ),
                            html.Div("League Wide Home - Road Win Record"),
                            html.Div(
                                f"{bans_df['win_pct'][0] * 100:.0f}% - {bans_df['win_pct'][1] * 100:.0f}% Win Percentage Splits"
                            ),
                        ],
                        className="kpi-box",
                    ),
                    # KPI 2
                    html.Div(
                        [
                            html.Div(bans_df["avg_pts"][0], style={"fontSize": 24}),
                            html.Div("League Average Points Scored / Game"),
                            html.Div(
                                f"{bans_df['avg_pts'][0] - bans_df['last_yr_ppg'][0]} difference from Last Season"
                            ),
                        ],
                        className="kpi-box",
                    ),
                    # KPI 3
                    html.Div(
                        [
                            html.Div("KPI 3 Value", style={"fontSize": 24}),
                            html.Div("Active Players in COVID Protocols"),
                            html.Div(f"xyz difference from 7 days ago"),
                        ],
                        className="kpi-box",
                    ),
                    # KPI 4
                    html.Div(
                        [
                            html.Div(
                                bans_df["upcoming_game_date"][0].strftime("%A, %B %d"),
                                style={"fontSize": 24},
                            ),
                            html.Div(f"{bans_df['upcoming_games'][0]} Upcoming Games"),
                            html.Div(""),
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
