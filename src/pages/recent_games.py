from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from src.data_cols.injury_tracker import injury_tracker_columns
from src.data_cols.recent_games_players import recent_games_players_columns
from src.data_cols.recent_games_teams import recent_games_teams_columns
from src.data import (
    injury_tracker_df,
    recent_games_players_df,
    recent_games_teams_df,
    pbp_df,
)
from src.utils import pbp_transformer

pbp_plot_kpis, pbp_plot_df = pbp_transformer(pbp_df)
yesterdays_games = pbp_df["game_description"].drop_duplicates()

recent_games_layout = html.Div(
    [
        html.Div(
            [
                html.Br(),
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
                    style={"width": "25%", "float": "left"},
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="pbp-analysis-plot",
                            config={"displayModeBar": False},
                        ),
                    ],
                    style={"width": "99%", "float": "left"},
                ),
            ]
        ),
        html.Div(
            [
                html.Br(),
                html.Div(
                    [
                        dash_table.DataTable(
                            id="player-recent-games-table",
                            columns=recent_games_players_columns,
                            data=recent_games_players_df.to_dict("records"),
                            css=[{"selector": ".show-hide", "rule": "display: none"}],
                            sort_action="native",
                            # style_table={"maxWidth": "100px"},
                            page_size=15,
                            style_cell_conditional=[
                                {"if": {"column_id": "player_logo"}, "width": "50%"},
                                {"if": {"column_id": "player"}, "width": "16%"},
                                {"if": {"column_id": "outcome"}, "width": "2%"},
                                {"if": {"column_id": "salary"}, "width": "4%"},
                                {"if": {"column_id": "pts"}, "width": "4%"},
                                {"if": {"column_id": "game_ts_percent"}, "width": "4%"},
                            ],
                            style_data_conditional=[
                                {
                                    "if": {"column_id": "player_logo"},
                                    "width": "50px",
                                    "white-space": "normal",  # Allow the image to resize within the cell
                                },
                            ],
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
                        html.H1("Injury Report"),
                        dash_table.DataTable(
                            id="injury-tracker-table",
                            columns=injury_tracker_columns,
                            data=injury_tracker_df.to_dict("records"),
                            css=[{"selector": ".show-hide", "rule": "display: none"}],
                        ),
                    ],
                    style={"width": "32%", "display": "inline-block"},
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
        row["player_logo"] = f'![Missing Image]({row["player_logo"]})'

    return data


@callback(
    Output("injury-tracker-table", "data"),
    Input("injury-tracker-table", "data"),
)
def render_images_injuries(data):
    for row in data:
        row["player_logo"] = f'![Missing Image]({row["player_logo"]})'

    return data


@callback(Output("pbp-analysis-plot", "figure"), [Input("game-selector", "value")])
def update_data_table(selected_value):
    filtered_pbp = pbp_plot_df.query(f"game_description == '{selected_value}'")

    figure = px.scatter(
        filtered_pbp,
        x="time_remaining_final",
        y="margin_score",
        labels={
            "margin_score": "Score Differential",
            "time_remaining_final": "",
        },
        title="Game Plot",
        hover_name="scoring_team",
    ).update_traces(
        marker=dict(
            color=filtered_pbp["scoring_team_color"],
            size=8,
        ),
        mode="markers+lines",  # Combine markers and lines
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        customdata=filtered_pbp[
            [
                "play",
                "time_quarter",
                "quarter",
                "leading_team_text",
                "score",
            ]
        ],
        hovertemplate="<b>Timestamp:</b> %{customdata[1]} in the %{customdata[2]}<br>"
        "<b>Scoring Team:</b> %{hovertext} (%{customdata[3]} %{customdata[4]})<br>"
        "<b>Play:</b> %{customdata[0]}<br>",
    )

    # yeeeahhh mfer
    figure.update_xaxes(
        autorange="reversed",
        ticktext=[
            "1st Quarter",
            "2nd Quarter",
            "3rd Quarter",
            "4th Quarter",
            "End of 4th Quarter",
            "1st OT",
            "2nd OT",
            "3rd OT",
            "4th OT",
        ],
        tickvals=[48.00, 36.00, 24.00, 12.00, 0.00, -5.00, -10.00, -15.00, -20.00],
    )

    figure.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)", paper_bgcolor="rgba(0, 0, 0, 0)"
    )
    return figure
