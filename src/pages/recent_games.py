from dash import dash_table, dcc, html

from src.data_cols.standings import standings_columns
from src.data import standings_df

recent_games_layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Western Conference"),
                        dash_table.DataTable(
                            id="player-recent-games-table",
                            columns=standings_columns,
                            data=standings_df.query('conference == "Western"').to_dict(
                                "records"
                            ),
                            hidden_columns=[
                                "active_protocols",
                                "conference",
                                "team",
                            ],
                            css=[{"selector": ".show-hide", "rule": "display: none"}],
                        ),
                    ],
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "margin-right": "30px",
                    },
                ),
                html.Div(
                    [
                        html.H1("Eastern Conference"),
                        dash_table.DataTable(
                            id="team-recent-games-table",
                            columns=standings_columns,
                            data=standings_df.query('conference == "Eastern"').to_dict(
                                "records"
                            ),
                            hidden_columns=[
                                "active_protocols",
                                "conference",
                                "team",
                            ],
                            css=[{"selector": ".show-hide", "rule": "display: none"}],
                        ),
                    ],
                    style={"width": "32%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.H1("Eastern Conference"),
                        dash_table.DataTable(
                            id="injury-tracker-table",
                            columns=standings_columns,
                            data=standings_df.query('conference == "Eastern"').to_dict(
                                "records"
                            ),
                            hidden_columns=[
                                "active_protocols",
                                "conference",
                                "team",
                            ],
                            css=[{"selector": ".show-hide", "rule": "display: none"}],
                        ),
                    ],
                    style={"width": "32%", "display": "inline-block"},
                ),
            ]
        ),
        html.Div(
            [
                dcc.Graph(
                    id="pbp-analysis-plot",
                    config={"displayModeBar": False},
                ),
            ]
        ),
    ],
    className="custom-padding",
)
