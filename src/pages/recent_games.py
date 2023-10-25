from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from src.data_cols.injury_tracker import injury_tracker_columns
from src.data_cols.recent_games_players import recent_games_players_columns
from src.data_cols.recent_games_teams import recent_games_teams_columns
from src.data_cols.standings import standings_columns
from src.data import (
    injury_tracker_df,
    recent_games_players_df,
    recent_games_teams_df,
    pbp_df,
    standings_df,
)
from src.utils import pbp_transformer

pbp_plot_kpis, pbp_plot_df = pbp_transformer(pbp_df)
yesterdays_games = pbp_df["game_description"].drop_duplicates()

recent_games_layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
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
                html.Div(
                    [
                        dcc.Dropdown(
                            id="game-selector",
                            options=[
                                {"label": game, "value": game}
                                for game in yesterdays_games
                            ],
                            clearable=False,
                            value=yesterdays_games[0],
                        ),
                    ],
                    style={"width": "15%", "float": "left"},
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="pbp-analysis-plot",
                            config={"displayModeBar": False},
                        ),
                    ],
                    style={"width": "85%", "float": "left"},
                ),
            ]
        ),
    ],
    className="custom-padding",
)


@callback(
    Output("player-recent-games-table", "data"),
    Input("player-recent-games-table", "data"),
)
def render_images(data):
    for row in data:
        row["player_logo"] = f'![Player Logo]({row["player_logo"]})'
    return data


@callback(
    Output("injury-tracker-table", "data"),
    Input("injury-tracker-table", "data"),
)
def render_images_injuries(data):
    for row in data:
        row["player_logo"] = f'![Player Logo]({row["player_logo"]})'
    return data


@callback(Output("pbp-analysis-plot", "figure"), [Input("game-selector", "value")])
def update_data_table(selected_value):
    filtered_pbp = pbp_plot_df.query(f"game_description == '{selected_value}'")

    figure = px.scatter(
        filtered_pbp,
        x="time_remaining_final",
        y="margin_score",
        labels={
            "time_remaining_final": "Quarter",
            "margin_score": "Score Differential",
        },
        title="Score Differential by Quarter",
    ).update_traces(
        marker=dict(
            color=filtered_pbp[
                "scoring_team_color"
            ],  # Color based on 'scoring_team_color'
            size=8,  # Adjust the size of the markers as needed
        ),
        mode="markers+lines",  # Combine markers and lines
    )

    return figure
