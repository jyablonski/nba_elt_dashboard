from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from src.config import DARK_LAYOUT_TEMPLATE, BASE_TABLE_STYLE, SINGLE_BAR_COLOR
from src.data_cols.future_schedule import future_schedule_columns
from src.data_cols.tonights_schedule import tonights_schedule_columns
from src.database import (
    game_types_df,
    past_schedule_analysis_df,
    preseason_odds_df,
    schedule_season_remaining_df,
    schedule_tonights_games_df,
    team_blown_leads_df,
    team_odds_outcomes_df,
)

# Constants
SCHEDULE_TABLE_OPTIONS = [
    {"label": "Tonight's Games", "value": "tonights-games"},
    {"label": "Full Schedule", "value": "full-schedule"},
]

SCHEDULE_PLOT_OPTIONS = [
    {"label": "Strength of Schedule (as of Today)", "value": "strength-of-schedule"},
    {"label": "Team Comebacks Analysis (Regular Season)", "value": "team-comebacks"},
    {"label": "Preseason Over / Under Trajectory", "value": "vegas-preseason-odds"},
    {"label": "Covering the Spread Metrics", "value": "team-spread-metrics"},
    {"label": "Game Types by Margin of Victory", "value": "game-types"},
]

COMMON_HOVER_STYLE = dict(
    bgcolor="#222222",
    font_size=12,
    font_family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    font_color="rgb(230, 224, 224)",
)

# Data preprocessing
past_schedule_analysis_df = past_schedule_analysis_df.sort_values(
    by="pct_vs_below_500", ascending=True
)
preseason_odds_df = preseason_odds_df.sort_values(by="wins_differential", ascending=True)
team_blown_leads_df = team_blown_leads_df.query("season_type == 'Regular Season'").sort_values(
    by="net_comebacks", ascending=True
)
team_odds_outcomes_df = team_odds_outcomes_df.query("season_type == 'Regular Season'").sort_values(
    by="pct_covered_spread", ascending=True
)
game_types_df = game_types_df.query("season_type == 'Regular Season'")


def create_tonight_games_table():
    """Create tonight's games table with conditional formatting"""
    # Enhanced table style with better column widths
    enhanced_cell_style = {
        **BASE_TABLE_STYLE,
        "minWidth": "100px",
        "maxWidth": "180px",
        "whiteSpace": "normal",
        "height": "auto",
    }

    return dash_table.DataTable(
        columns=tonights_schedule_columns,
        data=schedule_tonights_games_df.to_dict("records"),
        # Table behavior
        css=[{"selector": ".show-hide", "rule": "display: none"}],
        cell_selectable=False,
        sort_action="native",
        page_size=15,
        merge_duplicate_headers=True,
        # Styling
        style_cell=enhanced_cell_style,
        style_header={
            "backgroundColor": "#1e1e1e",
            "fontWeight": "bold",
            "textAlign": "center",
            "padding": "12px",
            "borderBottom": "2px solid #007bff",
        },
        style_data_conditional=[
            {
                "if": {
                    "filter_query": "{home_is_great_value} = 1",
                    "column_id": "home_team_odds",
                },
                "backgroundColor": "#4CAF50",
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {
                    "filter_query": "{away_is_great_value} = 1",
                    "column_id": "away_team_odds",
                },
                "backgroundColor": "#4CAF50",
                "color": "white",
                "fontWeight": "bold",
            },
            # Alternating row colors for better readability
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#2a2a2a",
            },
        ],
    )


def create_full_schedule_table():
    """Create full schedule table"""
    enhanced_cell_style = {
        **BASE_TABLE_STYLE,
        "minWidth": "100px",
        "maxWidth": "180px",
        "whiteSpace": "normal",
        "height": "auto",
    }

    return dash_table.DataTable(
        columns=future_schedule_columns,
        data=schedule_season_remaining_df.to_dict("records"),
        # Table behavior
        css=[{"selector": ".show-hide", "rule": "display: none"}],
        cell_selectable=False,
        sort_action="native",
        page_size=15,
        # Styling
        style_cell=enhanced_cell_style,
        style_header={
            "backgroundColor": "#1e1e1e",
            "fontWeight": "bold",
            "textAlign": "center",
            "padding": "12px",
            "borderBottom": "2px solid #007bff",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#2a2a2a",
            },
        ],
    )


def create_strength_of_schedule_plot():
    """Create strength of schedule analysis plot"""
    fig = px.bar(
        past_schedule_analysis_df,
        x="pct_vs_below_500",
        y="team",
        labels={"team": "Team", "pct_vs_below_500": "% Games vs Below .500 Teams"},
        title="Strength of Schedule Analysis",
        color_discrete_sequence=[SINGLE_BAR_COLOR],
        custom_data=[
            "team",
            "win_pct",
            "avg_win_pct_opp",
            "home_record",
            "road_record",
            "above_record",
            "below_record",
            "pct_vs_above_500",
            "pct_vs_below_500",
            "record",
        ],
    )

    fig.update_layout(
        **DARK_LAYOUT_TEMPLATE,
        legend_title_text="",
        xaxis_tickformat=".0%",
        title={"x": 0.5, "xanchor": "center"},
    )

    fig.update_traces(
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Record:</b> %{customdata[9]}<br>"
            "<b>Win %:</b> %{customdata[1]:.1%}<br>"
            "<b>AVG Win % Opp.:</b> %{customdata[2]:.1%}<br>"
            "<b>Home Record:</b> %{customdata[3]}<br>"
            "<b>Road Record:</b> %{customdata[4]}<br>"
            "<b>Record vs Above .500:</b> %{customdata[5]}<br>"
            "<b>Record vs Below .500:</b> %{customdata[6]}<br>"
            "<b>% Games vs Above .500:</b> %{customdata[7]:.1%}<br>"
            "<b>% Games vs Below .500:</b> %{customdata[8]:.1%}<br>"
            "<extra></extra>"
        ),
    )
    return fig


def create_preseason_odds_plot():
    """Create preseason over/under trajectory plot"""
    fig = px.bar(
        preseason_odds_df,
        x="wins_differential",
        y="team",
        color="wins_differential",
        color_continuous_scale=[[0, "#e04848"], [0.5, "#383b3d"], [1, "#3fb7d9"]],
        labels={"team": "Team", "wins_differential": "Wins vs Preseason Projection"},
        title="Preseason Over/Under Performance",
        custom_data=[
            "team",
            "wins_differential",
            "predicted_stats",
            "projected_stats",
            "over_under",
            "championship_odds",
        ],
    )

    fig.update_layout(**DARK_LAYOUT_TEMPLATE, title={"x": 0.5, "xanchor": "center"})

    fig.update_traces(
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Wins Differential:</b> %{customdata[1]}<br>"
            "<b>Preseason O/U:</b> %{customdata[2]}<br>"
            "<b>Projected Stats:</b> %{customdata[3]}<br>"
            "<b>Status:</b> %{customdata[4]}<br>"
            "<b>Championship Odds:</b> %{customdata[5]}<br>"
            "<extra></extra>"
        ),
    )
    return fig


def create_spread_metrics_plot():
    """Create spread covering metrics plot"""
    fig = px.bar(
        team_odds_outcomes_df,
        x="pct_covered_spread",
        y="team",
        color="pct_covered_spread",
        color_continuous_scale=[[0, "#e04848"], [0.5, "#383b3d"], [1, "#3fb7d9"]],
        labels={"team": "Team", "pct_covered_spread": "% Games Covered Spread"},
        title="Spread Coverage Performance",
        custom_data=[
            "team",
            "games_played",
            "games_covered_spread",
            "games_favorite",
            "games_underdog",
            "games_favorite_covered",
            "games_underdog_covered",
            "pct_covered_spread",
            "pct_favorite_covered",
            "pct_underdog_covered",
        ],
    )

    fig.update_layout(
        **DARK_LAYOUT_TEMPLATE,
        legend_title_text="",
        xaxis_tickformat=".0%",
        title={"x": 0.5, "xanchor": "center"},
    )

    fig.update_traces(
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Games Played:</b> %{customdata[1]}<br>"
            "<b>Games Covered Spread:</b> %{customdata[2]}<br>"
            "<b>Games as Favorite:</b> %{customdata[3]}<br>"
            "<b>Games as Underdog:</b> %{customdata[4]}<br>"
            "<b>Favorite Games Covered:</b> %{customdata[5]}<br>"
            "<b>Underdog Games Covered:</b> %{customdata[6]}<br>"
            "<b>% Covered Spread:</b> %{customdata[7]:.1%}<br>"
            "<b>% Favorite Covered:</b> %{customdata[8]:.1%}<br>"
            "<b>% Underdog Covered:</b> %{customdata[9]:.1%}<br>"
            "<extra></extra>"
        ),
    )
    return fig


def create_comebacks_plot():
    """Create team comebacks analysis plot"""
    fig = px.bar(
        team_blown_leads_df,
        x="net_comebacks",
        y="team",
        color="net_comebacks",
        color_continuous_scale=[[0, "#e04848"], [0.5, "#383b3d"], [1, "#3fb7d9"]],
        labels={"team": "Team", "net_comebacks": "Net Comebacks (Comebacks - Blown Leads)"},
        title="Team Comeback Performance",
        custom_data=[
            "team",
            "blown_leads_10pt",
            "blown_lead_rank",
            "team_comebacks_10pt",
            "comeback_rank",
            "net_comebacks",
            "net_rank",
        ],
    )

    fig.update_layout(**DARK_LAYOUT_TEMPLATE, title={"x": 0.5, "xanchor": "center"})

    fig.update_traces(
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Comebacks:</b> %{customdata[1]}<br>"
            "<b>Blown Leads:</b> %{customdata[2]}<br>"
            "<b>Net Comebacks:</b> %{customdata[3]}<br>"
            "<b>Comeback Win %:</b> %{customdata[4]:.1%}<br>"
            "<extra></extra>"
        ),
    )
    return fig


def create_game_types_plot():
    """Create game types distribution plot"""
    fig = px.bar(
        game_types_df,
        x="n",
        y="game_type",
        labels={"n": "Number of Games", "game_type": "Game Type"},
        title="Distribution of Games by Margin",
        color_discrete_sequence=[SINGLE_BAR_COLOR],
        custom_data=["game_type", "n", "explanation"],
    )

    fig.update_layout(**DARK_LAYOUT_TEMPLATE, title={"x": 0.5, "xanchor": "center"})

    fig.update_traces(
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>Game Type:</b> %{customdata[0]}<br>"
            "<b># Games:</b> %{customdata[1]}<br>"
            "<b>Definition:</b> %{customdata[0]}s are games where<br>"
            "the Margin of Victory is %{customdata[2]}<br>"
            "<extra></extra>"
        ),
        textfont={"color": "rgb(230, 224, 224)"},
    )
    return fig


# Improved Layout with Cards and Better Spacing
schedule_layout = html.Div(
    [
        # Header Section with Card
        dbc.Card(
            dbc.CardBody(
                [
                    html.H1(
                        "Upcoming Games",
                        className="text-center mb-4",
                        style={
                            "font-size": "2.5rem",
                            "font-weight": "bold",
                            "color": "#ffffff",
                        },
                    ),
                    # Info and Button Row
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Span(
                                            "Moneyline odds provided by ",
                                            className="me-2",
                                            style={"font-size": "14px", "color": "#cccccc"},
                                        ),
                                        html.A(
                                            html.Img(
                                                src="../assets/draftkings.png",
                                                height="32px",
                                                style={"vertical-align": "middle"},
                                            ),
                                            href="https://www.draftkings.com",
                                            target="_blank",
                                            className="mx-2",
                                        ),
                                        html.Span(
                                            "•",
                                            className="mx-3",
                                            style={"color": "#666", "font-size": "16px"},
                                        ),
                                        html.Span(
                                            "●",
                                            className="me-2",
                                            style={"color": "#4CAF50", "font-size": "16px"},
                                        ),
                                        html.Span(
                                            "Green = Great Value",
                                            style={
                                                "font-weight": "600",
                                                "color": "#4CAF50",
                                                "font-size": "14px",
                                            },
                                        ),
                                    ],
                                    className="d-flex align-items-center justify-content-center flex-wrap",
                                ),
                                lg=8,
                                md=12,
                                className="mb-3 mb-lg-0",
                            ),
                            dbc.Col(
                                html.A(
                                    [
                                        html.I(className="fas fa-bullseye me-2"),
                                        "Make & Track Bet Predictions",
                                    ],
                                    href="https://api.jyablonski.dev/bets",
                                    className="btn btn-primary w-100",
                                    style={
                                        "font-weight": "600",
                                        "padding": "10px 20px",
                                        "border-radius": "8px",
                                        "font-size": "14px",
                                    },
                                ),
                                lg=4,
                                md=12,
                                className="d-flex align-items-center",
                            ),
                        ],
                        className="align-items-center",
                    ),
                ]
            ),
            className="mb-4 shadow-sm",
            style={"backgroundColor": "#1a1a1a", "border": "1px solid #333"},
        ),
        # Schedule Table Card
        dbc.Card(
            dbc.CardBody(
                [
                    # Controls
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        "Select Schedule View:",
                                        className="form-label fw-bold mb-2",
                                        style={"font-size": "14px", "color": "#e0e0e0"},
                                    ),
                                    dcc.Dropdown(
                                        id="schedule-table-selector",
                                        options=SCHEDULE_TABLE_OPTIONS,
                                        value="tonights-games",
                                        clearable=False,
                                        style={"width": "300px"},
                                        className="mb-3",
                                    ),
                                ],
                                width=12,
                            ),
                        ],
                    ),
                    # Table
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    id="schedule-table",
                                    style={
                                        "overflow-x": "auto",
                                        "border-radius": "8px",
                                    },
                                ),
                                width=12,
                            )
                        ]
                    ),
                ]
            ),
            className="mb-5 shadow-sm",
            style={"backgroundColor": "#1a1a1a", "border": "1px solid #333"},
        ),
        # Analysis Section Card
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(
                        "NBA Schedule Analysis",
                        className="mb-4",
                        style={
                            "font-weight": "bold",
                            "color": "#ffffff",
                            "font-size": "1.8rem",
                        },
                    ),
                    # Plot Selector
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        "Select Analysis Plot:",
                                        className="form-label fw-bold mb-2",
                                        style={"font-size": "14px", "color": "#e0e0e0"},
                                    ),
                                    dcc.Dropdown(
                                        id="schedule-plot-selector",
                                        options=SCHEDULE_PLOT_OPTIONS,
                                        value="strength-of-schedule",
                                        clearable=False,
                                        style={"width": "100%", "max-width": "500px"},
                                        className="mb-4",
                                    ),
                                ],
                                width=12,
                            ),
                        ]
                    ),
                    # Chart
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="schedule-plot",
                                    style={"height": "600px"},
                                    config={"displayModeBar": True, "displaylogo": False},
                                ),
                                width=12,
                            ),
                        ]
                    ),
                ]
            ),
            className="shadow-sm",
            style={"backgroundColor": "#1a1a1a", "border": "1px solid #333"},
        ),
    ],
    className="container-fluid px-4 py-4",
    style={"max-width": "1600px", "margin": "0 auto"},
)


# Callbacks
@callback(Output("schedule-table", "children"), [Input("schedule-table-selector", "value")])
def update_schedule_table(selected_value):
    """Update schedule table based on selection"""
    if selected_value == "tonights-games":
        return create_tonight_games_table()
    elif selected_value == "full-schedule":
        return create_full_schedule_table()
    return html.Div("No data available")


@callback(
    Output("schedule-plot", "figure"),
    Input("schedule-plot-selector", "value"),
)
def update_schedule_plot(selected_schedule_plot):
    """Update schedule analysis plot based on selection"""
    plot_functions = {
        "strength-of-schedule": create_strength_of_schedule_plot,
        "vegas-preseason-odds": create_preseason_odds_plot,
        "team-spread-metrics": create_spread_metrics_plot,
        "team-comebacks": create_comebacks_plot,
        "game-types": create_game_types_plot,
    }

    plot_function = plot_functions.get(selected_schedule_plot)
    if plot_function:
        return plot_function()

    # Fallback to strength of schedule
    return create_strength_of_schedule_plot()
