from dash import dash_table, dcc, html

from src.data_cols.injury_tracker import injury_tracker_columns
from src.data_cols.recent_games_players import recent_games_players_columns
from src.data_cols.recent_games_teams import recent_games_teams_columns
from src.data_cols.standings import standings_columns
from src.data import (
    injury_tracker_df,
    recent_games_players_df,
    recent_games_teams_df,
    standings_df,
)

recent_games_layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        # html.H1("Western Conference"),
                        dash_table.DataTable(
                            id="player-recent-games-table",
                            columns=recent_games_players_columns,
                            data=recent_games_players_df.to_dict("records"),
                            # hidden_columns=[
                            #     "active_protocols",
                            #     "conference",
                            #     "team",
                            # ],
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
                        # html.H1("Eastern Conference"),
                        dash_table.DataTable(
                            id="team-recent-games-table",
                            columns=recent_games_teams_columns,
                            data=recent_games_teams_df.to_dict("records"),
                            # hidden_columns=[
                            #     "active_protocols",
                            #     "conference",
                            #     "team",
                            # ],
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
                            columns=injury_tracker_columns,
                            data=injury_tracker_df.to_dict("records"),
                            # hidden_columns=[
                            #     "active_protocols",
                            #     "conference",
                            #     "team",
                            # ],
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
