from dash import dcc, html
import dash_bootstrap_components as dbc

player_analysis_layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Select a Player", style={"text-align": "left"}),
                        dcc.Dropdown(
                            id="player-selector",
                            options=[
                                {"label": "Tonight's Games", "value": "tonights-games"},
                                {
                                    "label": "Full Schedule",
                                    "value": "full-schedule",
                                },
                            ],
                            value="tonights-games",
                            clearable=False,
                        ),
                    ],
                    width=3,
                ),
            ]
        ),
        dbc.Row(
            [
                html.Br(),
                dbc.Col(
                    id="player-table-1",
                    width=6,
                ),
                dbc.Col(
                    id="player-table-2",
                    width=6,
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("League Average Margins of Victory"),
                                dcc.Graph(
                                    id="player-plot-1",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                html.H3("Team Schedule Analysis"),
                                dcc.Graph(
                                    id="player-plot-2",
                                ),
                            ],
                            width=6,
                        ),
                    ]
                ),
            ]
        ),
    ],
    className="custom-padding",
)
