from dash import dcc, html
import dash_bootstrap_components as dbc

from src.ui.sections import page_hero, section_header

player_analysis_layout = html.Div(
    [
        page_hero(
            title="Player-level views (work in progress).",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        section_header("Select a player"),
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
                            className="dash-dropdown",
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
                                section_header("League average margins of victory"),
                                dcc.Graph(
                                    id="player-plot-1",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                section_header("Team schedule analysis"),
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
