from dash import callback, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from src.data_cols.injuries import injuries_columns
from src.data_cols.transactions import transactions_columns
from src.database import (
    injuries_df,
    mov_df,
    player_stats_df,
    team_adv_stats_df,
    transactions_df,
)
from src.data import team_names
from src.ui.cards import kpi_card as create_kpi_card
from src.theme.plotly import TRACE_HOVERLABEL, apply_dark_layout
from src.ui.sections import page_hero, section_header
from src.ui.tables import dark_datatable

TEAM_OPTIONS = [{"label": team, "value": team} for team in team_names]

GAME_OUTCOME_COLORS = {
    "W": "#3fb7d9",  # Blue for wins
    "L": "#e04848",  # Red for losses
}

MVP_CANDIDATE_COLORS = {
    "Top 5 MVP Candidate": "#9362DA",  # Purple from your theme
    "Other": "#383b3d",  # Gray from your theme
}

TOOLTIP_CSS = [
    {
        "selector": ".dash-table-tooltip",
        "rule": (
            "background-color: #222222; font-family: Inter, system-ui, sans-serif; "
            "color: rgb(230, 224, 224)"
        ),
    }
]


def create_data_table(columns, data, *, table_id: str, conditional_columns=None):
    return dark_datatable(
        table_id=table_id,
        columns=columns,
        data=data,
        css=TOOLTIP_CSS,
        cell_selectable=False,
        sort_action="native",
        page_size=10,
        style_cell={
            "whiteSpace": "normal",
            "height": "auto",
            "minHeight": "2.5rem",
            "lineHeight": "1.35",
            "textAlign": "center",
            "fontSize": 12,
        },
        style_cell_conditional=conditional_columns or [],
        tooltip_data=[
            {column: {"value": str(value), "type": "markdown"} for column, value in row.items()}
            for row in data
        ],
        tooltip_duration=None,
    )


# Layout
team_analysis_layout = html.Div(
    [
        page_hero(
            title="Per-team trends, health, and roster moves.",
        ),
        # KPI Section
        html.Div(
            [
                # Team Selector
                create_kpi_card(
                    [
                        html.H4("Select Team", className="mb-2"),
                        dcc.Dropdown(
                            id="team-selector",
                            options=TEAM_OPTIONS,
                            value=team_names[0],
                            clearable=False,
                            className="dash-dropdown",
                        ),
                    ]
                ),
                # Dynamic KPI Boxes
                html.Div(id="kpi-boxes-1", className="kpi-card"),
                html.Div(id="kpi-boxes-2", className="kpi-card"),
                html.Div(id="kpi-boxes-3", className="kpi-card"),
            ],
            className="kpi-container",
            style={"display": "flex", "justify-content": "space-between", "margin-bottom": "20px"},
        ),
        # Charts Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        section_header("Game Margin of Victory"),
                        dcc.Graph(
                            id="mov-plot",
                            config={"displayModeBar": False},
                            style={"height": "500px"},
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        section_header("Player Scoring Efficiency"),
                        dcc.Graph(
                            id="team-player-efficiency-plot",
                            config={"displayModeBar": False},
                            style={"height": "500px"},
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
        html.Br(),
        # Tables Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        section_header("Team Injuries"),
                        html.Div(id="injuries-table"),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        section_header("Team Transactions"),
                        html.Div(id="transactions-table"),
                    ],
                    width=6,
                ),
            ]
        ),
    ],
    className="custom-padding",
)


# Callbacks
@callback(Output("mov-plot", "figure"), Input("team-selector", "value"))
def update_mov(selected_team):
    """Update margin of victory plot"""
    if not selected_team:
        return {}

    filtered_df = mov_df.query(f"full_team == '{selected_team}'")

    if filtered_df.empty:
        return {}

    fig = px.bar(
        filtered_df,
        x="game_date",
        y="mov",
        labels={
            "game_date": "Date",
            "mov": "Margin of Victory",
        },
        color="outcome",
        color_discrete_map=GAME_OUTCOME_COLORS,
        custom_data=["game_date", "opponent", "mov", "outcome", "pts_scored", "pts_scored_opp"],
    )

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(title={"x": 0.5, "xanchor": "center"})

    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
        hovertemplate=(
            "<b>%{customdata[0]} %{customdata[3]}</b> vs <b>%{customdata[1]}</b><br>"
            "<b>Score:</b> %{customdata[4]} - %{customdata[5]}<br>"
            "<b>Margin of Victory:</b> %{customdata[2]}<br>"
            "<extra></extra>"
        ),
    )

    return fig


@callback(Output("team-player-efficiency-plot", "figure"), Input("team-selector", "value"))
def update_team_player_efficiency(selected_team):
    """Update player efficiency scatter plot"""
    if not selected_team:
        return {}

    team_player_efficiency = player_stats_df.query(f"full_team == '{selected_team}'")

    if team_player_efficiency.empty:
        return {}

    fig = px.scatter(
        team_player_efficiency,
        x="avg_ppg",
        y="avg_ts_percent",
        color="is_mvp_candidate",
        color_discrete_map=MVP_CANDIDATE_COLORS,
        text="player",
        labels={"avg_ppg": "Average Points Per Game", "avg_ts_percent": "True Shooting %"},
        custom_data=["player", "avg_ppg", "avg_ts_percent", "is_mvp_candidate", "games_played"],
    )

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(
        legend_title_text="Player Type",
        yaxis_tickformat=".0%",
        title={"x": 0.5, "xanchor": "center"},
    )

    fig.update_traces(
        textposition="top center",
        textfont={"color": "rgb(230, 224, 224)", "size": 10},
        hoverlabel=TRACE_HOVERLABEL,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Type:</b> %{customdata[3]}<br>"
            "<b>Average PPG:</b> %{customdata[1]}<br>"
            "<b>True Shooting %:</b> %{customdata[2]:.1%}<br>"
            "<b>Games Played:</b> %{customdata[4]}<br>"
            "<extra></extra>"
        ),
    )

    return fig


@callback(Output("injuries-table", "children"), Input("team-selector", "value"))
def update_injuries(selected_team):
    """Update injuries table"""
    if not selected_team:
        return html.Div("No team selected")

    # Sort by scrape_date in descending order (most recent first)
    filtered_injuries = injuries_df.query(f"team == '{selected_team}'").sort_values(
        by="scrape_date", ascending=False
    )

    if filtered_injuries.empty:
        return html.Div(
            "No injuries reported", style={"text-align": "center", "color": "rgb(230, 224, 224)"}
        )

    return create_data_table(
        columns=injuries_columns,
        data=filtered_injuries.to_dict("records"),
        table_id="team-injuries-table",
        conditional_columns=[
            {"if": {"column_id": "player"}, "width": "15%"},
            {"if": {"column_id": "team"}, "width": "15%"},
            {"if": {"column_id": "date"}, "width": "15%"},
            {"if": {"column_id": "status"}, "width": "10%"},
            {"if": {"column_id": "injury"}, "width": "10%"},
            {"if": {"column_id": "description"}, "width": "50%", "textAlign": "left"},
        ],
    )


@callback(Output("transactions-table", "children"), Input("team-selector", "value"))
def update_transactions(selected_team):
    """Update transactions table"""
    if not selected_team:
        return html.Div("No team selected")

    # Sort by date in descending order (most recent first)
    filtered_transactions = transactions_df.query(
        f'transaction.str.contains("{selected_team}")', engine="python"
    ).sort_values(by="date", ascending=False)

    if filtered_transactions.empty:
        return html.Div(
            "No recent transactions", style={"text-align": "center", "color": "rgb(230, 224, 224)"}
        )

    return create_data_table(
        columns=transactions_columns,
        data=filtered_transactions.to_dict("records"),
        table_id="team-transactions-table",
        conditional_columns=[
            {"if": {"column_id": "date"}, "width": "20%"},
            {"if": {"column_id": "transaction"}, "width": "80%", "textAlign": "left"},
        ],
    )


@callback(Output("kpi-boxes-1", "children"), [Input("team-selector", "value")])
def update_kpi_boxes_1(selected_team):
    """Update team ratings KPI box"""
    if not selected_team:
        return []

    kpi_values = team_adv_stats_df.query(f"team == '{selected_team}'")

    if kpi_values.empty:
        return [html.Div("No data available")]

    return [
        html.Div(
            "Team Ratings", style={"fontSize": 20, "fontWeight": "bold", "margin-bottom": "10px"}
        ),
        html.Div(f"Net Rating: {kpi_values['nrtg'].iloc[0]}", style={"margin-bottom": "5px"}),
        html.Div(f"Offensive Rating: {kpi_values['ortg'].iloc[0]}", style={"margin-bottom": "5px"}),
        html.Div(f"Defensive Rating: {kpi_values['drtg'].iloc[0]}", style={"margin-bottom": "5px"}),
    ]


@callback(Output("kpi-boxes-2", "children"), [Input("team-selector", "value")])
def update_kpi_boxes_2(selected_team):
    """Update advanced stats KPI box"""
    if not selected_team:
        return []

    kpi_values = team_adv_stats_df.query(f"team == '{selected_team}'")

    if kpi_values.empty:
        return [html.Div("No data available")]

    return [
        html.Div(
            "Advanced Stats", style={"fontSize": 20, "fontWeight": "bold", "margin-bottom": "10px"}
        ),
        html.Div(f"SRS: {kpi_values['srs'].iloc[0]}", style={"margin-bottom": "5px"}),
        html.Div(f"Pace: {kpi_values['pace'].iloc[0]}", style={"margin-bottom": "5px"}),
        html.Div(f"TS %: {kpi_values['ts_percent'].iloc[0]:.1%}", style={"margin-bottom": "5px"}),
    ]


@callback(Output("kpi-boxes-3", "children"), [Input("team-selector", "value")])
def update_kpi_boxes_3(selected_team):
    """Update opponent stats KPI box"""
    if not selected_team:
        return []

    kpi_values = team_adv_stats_df.query(f"team == '{selected_team}'")

    if kpi_values.empty:
        return [html.Div("No data available")]

    return [
        html.Div(
            "Opponent Stats", style={"fontSize": 20, "fontWeight": "bold", "margin-bottom": "10px"}
        ),
        html.Div(
            f"TOV %: {kpi_values['tov_percent_opp'].iloc[0]}%", style={"margin-bottom": "5px"}
        ),
        html.Div(
            f"eFG %: {kpi_values['efg_percent_opp'].iloc[0]:.1%}", style={"margin-bottom": "5px"}
        ),
    ]
