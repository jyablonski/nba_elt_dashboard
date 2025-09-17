from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from src.data_cols.recent_games_players import recent_games_players_columns
from src.data_cols.recent_games_teams import recent_games_teams_columns
from src.database import (
    recent_games_players_df,
    recent_games_teams_df,
    pbp_df,
)
from src.utils import pbp_transformer

PERFORMANCE_COLORS = {
    1: "#9362DA",  # Season high (purple) - matches .legend .season-high
    2: "#3fb7d9",  # 10+ above (blue) - matches .legend .ten-above
    3: "#e04848",  # 10+ below (red) - matches .legend .ten-below
}

COMMON_HOVER_STYLE = dict(
    bgcolor="rgba(255, 255, 255, 0.95)",
    font_size=12,
    font_family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    font_color="#000000",
)

# Data preprocessing
pbp_plot_kpis, pbp_plot_df = pbp_transformer(pbp_df)
yesterdays_games = pbp_df["game_description"].drop_duplicates()

GAME_OPTIONS = [{"label": game, "value": game} for game in yesterdays_games]


def create_performance_legend():
    """Create the performance color legend"""
    return html.Div(
        [
            html.H5(
                "Table Cell Coloring",
                style={"margin-bottom": "10px", "color": "rgb(230, 224, 224)", "font-size": "16px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                style={
                                    "backgroundColor": "#9362DA",
                                    "border": "1px solid #ccc",
                                    "width": "30px",
                                    "height": "15px",
                                    "display": "inline-block",
                                    "marginRight": "5px",
                                    "marginTop": "3px",
                                }
                            ),
                            " Season High",
                        ],
                        style={"display": "flex", "alignItems": "center", "marginRight": "15px"},
                    ),
                    html.Div(
                        [
                            html.Span(
                                style={
                                    "backgroundColor": "#3fb7d9",
                                    "border": "1px solid #ccc",
                                    "width": "30px",
                                    "height": "15px",
                                    "display": "inline-block",
                                    "marginRight": "5px",
                                    "marginTop": "3px",
                                }
                            ),
                            " 10+ pts Above",
                        ],
                        style={"display": "flex", "alignItems": "center", "marginRight": "15px"},
                    ),
                    html.Div(
                        [
                            html.Span(
                                style={
                                    "backgroundColor": "#e04848",
                                    "border": "1px solid #ccc",
                                    "width": "30px",
                                    "height": "15px",
                                    "display": "inline-block",
                                    "marginRight": "5px",
                                    "marginTop": "3px",
                                }
                            ),
                            " 10+ pts Below",
                        ],
                        style={"display": "flex", "alignItems": "center", "marginRight": "15px"},
                    ),
                ],
                style={"display": "flex", "flex-wrap": "wrap", "alignItems": "center"},
            ),
        ],
        style={"width": "100%", "overflow": "hidden"},
    )


def create_players_table():
    """Create the players performance table"""
    return dash_table.DataTable(
        id="player-recent-games-table",
        columns=recent_games_players_columns,
        data=recent_games_players_df.to_dict("records"),
        # Table behavior
        css=[
            {"selector": ".show-hide", "rule": "display: none"},
            {
                "selector": ".dash-cell img",
                "rule": "max-height: 80px; max-width: 80px; height: auto; width: auto; display: block; margin: 0 auto;",
            },
        ],
        cell_selectable=False,
        sort_action="native",
        page_size=15,
        # Styling
        style_cell={
            "background-color": "#383b3d",
            "textAlign": "center",
            "fontSize": 15,
            "color": "rgb(230, 224, 224)",
            "padding": "8px",
            "height": "auto",
            "minHeight": "50px",
            "whiteSpace": "normal",
        },
        # Column widths
        style_cell_conditional=[
            {"if": {"column_id": "player_logo"}, "width": "12%", "padding": "4px"},
            {"if": {"column_id": "player"}, "width": "18%", "textAlign": "left"},
            {"if": {"column_id": "outcome"}, "width": "8%"},
            {"if": {"column_id": "salary"}, "width": "10%"},
            {"if": {"column_id": "pts"}, "width": "8%"},
            {"if": {"column_id": "game_ts_percent"}, "width": "12%"},
            {"if": {"column_id": "plus_minus"}, "width": "10%"},
        ],
        # Performance-based conditional formatting
        style_data_conditional=[
            # Points coloring
            {
                "if": {"filter_query": "{pts_color} = 1", "column_id": "pts"},
                "backgroundColor": PERFORMANCE_COLORS[1],
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {"filter_query": "{pts_color} = 2", "column_id": "pts"},
                "backgroundColor": PERFORMANCE_COLORS[2],
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {"filter_query": "{pts_color} = 3", "column_id": "pts"},
                "backgroundColor": PERFORMANCE_COLORS[3],
                "color": "white",
                "fontWeight": "bold",
            },
            # True shooting coloring
            {
                "if": {"filter_query": "{ts_color} = 1", "column_id": "game_ts_percent"},
                "backgroundColor": PERFORMANCE_COLORS[1],
                "color": "white",
                "fontWeight": "bold",
            },
        ],
    )


def create_teams_table():
    """Create the teams performance table"""
    return dash_table.DataTable(
        id="team-recent-games-table",
        columns=recent_games_teams_columns,
        data=recent_games_teams_df.to_dict("records"),
        # Table behavior
        css=[
            {"selector": ".show-hide", "rule": "display: none"},
            {
                "selector": ".dash-cell img",
                "rule": "max-height: 40px; max-width: 40px; height: auto; width: auto; display: block; margin: 0 auto;",
            },
        ],
        cell_selectable=False,
        merge_duplicate_headers=True,
        # Styling
        style_cell={
            "background-color": "#383b3d",
            "textAlign": "center",
            "fontSize": 15,
            "color": "rgb(230, 224, 224)",
            "padding": "8px",
            "height": "auto",
            "minHeight": "45px",
            "whiteSpace": "normal",
        },
        # Column widths
        style_cell_conditional=[
            {"if": {"column_id": "team_logo"}, "width": "12%", "padding": "4px"},
            {"if": {"column_id": "opp_logo"}, "width": "12%", "padding": "4px"},
            {"if": {"column_id": "pts_scored"}, "width": "10%"},
            {"if": {"column_id": "max_team_lead"}, "width": "12%"},
            {"if": {"column_id": "pts_scored_opp"}, "width": "10%"},
            {"if": {"column_id": "max_opponent_lead"}, "width": "12%"},
            {"if": {"column_id": "mov"}, "width": "8%"},
            {"if": {"column_id": "vs"}, "width": "6%"},
        ],
        # Performance-based conditional formatting
        style_data_conditional=[
            # Team points coloring
            {
                "if": {"filter_query": "{pts_color} = 1", "column_id": "pts_scored"},
                "backgroundColor": PERFORMANCE_COLORS[1],
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {"filter_query": "{pts_color} = 2", "column_id": "pts_scored"},
                "backgroundColor": PERFORMANCE_COLORS[2],
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {"filter_query": "{pts_color} = 3", "column_id": "pts_scored"},
                "backgroundColor": PERFORMANCE_COLORS[3],
                "color": "white",
                "fontWeight": "bold",
            },
            # Opponent points coloring
            {
                "if": {"filter_query": "{opp_pts_color} = 1", "column_id": "pts_scored_opp"},
                "backgroundColor": PERFORMANCE_COLORS[1],
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {"filter_query": "{opp_pts_color} = 2", "column_id": "pts_scored_opp"},
                "backgroundColor": PERFORMANCE_COLORS[2],
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {"filter_query": "{opp_pts_color} = 3", "column_id": "pts_scored_opp"},
                "backgroundColor": PERFORMANCE_COLORS[3],
                "color": "white",
                "fontWeight": "bold",
            },
        ],
    )


# Layout
recent_games_layout = html.Div(
    [
        # Play by Play Section
        html.Div(
            [
                html.H3(
                    "Play by Play Analysis", style={"margin-bottom": "20px", "text-align": "center"}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(
                                    "Select Game:",
                                    style={"margin-bottom": "10px", "fontWeight": "bold"},
                                ),
                                dcc.Dropdown(
                                    id="game-selector",
                                    options=GAME_OPTIONS,
                                    clearable=False,
                                    value=yesterdays_games[0]
                                    if len(yesterdays_games) > 0
                                    else None,
                                    style={"margin-bottom": "20px"},
                                ),
                            ],
                            width=4,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="pbp-analysis-plot",
                                    config={"displayModeBar": False},
                                    style={"height": "600px"},
                                ),
                            ],
                            width=12,
                        ),
                    ]
                ),
            ],
            style={"margin-bottom": "40px"},
        ),
        # Legend Section
        dbc.Row(
            [
                dbc.Col([create_performance_legend()], width=6),
            ],
            style={"margin-bottom": "20px"},
        ),
        # Tables Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Top Player Performances", style={"margin-bottom": "15px"}),
                        create_players_table(),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H3("Team Game Results", style={"margin-bottom": "15px"}),
                        html.Div([create_teams_table()], className="team-data-table"),
                    ],
                    width=6,
                ),
            ]
        ),
    ],
    className="custom-padding",
)


# Callbacks
@callback(
    Output("player-recent-games-table", "data"),
    Input("player-recent-games-table", "data"),
)
def render_player_images(data):
    """Render player images in the table"""
    for row in data:
        row["player_logo"] = f"![Player Image]({row['player_logo']})"
    return data


@callback(
    Output("team-recent-games-table", "data"),
    Input("team-recent-games-table", "data"),
)
def render_team_images(data):
    """Render team logos in the table"""
    for row in data:
        row["team_logo"] = f"![Team Logo](assets/{row['team_logo']})"
        row["opp_logo"] = f"![Opponent Logo](assets/{row['opp_logo']})"
    return data


@callback(Output("pbp-analysis-plot", "figure"), [Input("game-selector", "value")])
def update_pbp_plot(selected_game):
    """Update play-by-play analysis plot"""
    if not selected_game:
        return {}

    filtered_pbp = pbp_plot_df.query(f"game_description == '{selected_game}'")

    if filtered_pbp.empty:
        return {}

    fig = px.scatter(
        filtered_pbp,
        x="time_remaining_final",
        y="margin_score",
        labels={
            "margin_score": "Score Differential",
            "time_remaining_final": "Game Time",
        },
        title=f"Play-by-Play Score Flow: {selected_game}",
        custom_data=[
            "play",
            "time_quarter",
            "quarter",
            "leading_team_text",
            "score",
            "game_plot_team_text",
        ],
    )

    # Apply dark theme layout with transparent backgrounds
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent paper background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        font={
            "color": "rgb(230, 224, 224)",
            "family": "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
        },
        xaxis={
            "gridcolor": "#383b3d",
            "linecolor": "#383b3d",
            "tickcolor": "#383b3d",
            "zerolinecolor": "#383b3d",
        },
        yaxis={
            "gridcolor": "#383b3d",
            "linecolor": "#383b3d",
            "tickcolor": "#383b3d",
            "zerolinecolor": "#383b3d",
        },
        margin={"l": 80, "r": 40, "t": 80, "b": 60},
        title={"x": 0.5, "xanchor": "center"},
    )

    # Update traces with team colors and styling
    fig.update_traces(
        marker=dict(
            color=filtered_pbp["scoring_team_color"],
            size=8,
            line=dict(width=1, color="rgb(230, 224, 224)"),
        ),
        mode="markers+lines",
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>Time:</b> %{customdata[1]} in %{customdata[2]}<br>"
            "<b>Scoring Team:</b> %{customdata[5]}<br>"
            "<b>Score:</b> %{customdata[4]} (%{customdata[3]})<br>"
            "<b>Play:</b> %{customdata[0]}<br>"
            "<extra></extra>"
        ),
    )

    # Custom x-axis for game quarters
    fig.update_xaxes(
        autorange="reversed",
        ticktext=[
            "1st Quarter",
            "2nd Quarter",
            "3rd Quarter",
            "4th Quarter",
            "End of 4th",
            "1st OT",
            "2nd OT",
            "3rd OT",
            "4th OT",
        ],
        tickvals=[48.00, 36.00, 24.00, 12.00, 0.00, -5.00, -10.00, -15.00, -20.00],
        showline=True,
        linecolor="rgb(230, 224, 224)",
        linewidth=1,
        mirror=True,
        title="Game Progress",
    )

    # Style y-axis
    fig.update_yaxes(
        showline=True,
        linecolor="rgb(230, 224, 224)",
        linewidth=1,
        mirror=True,
        title="Score Differential",
    )

    return fig
