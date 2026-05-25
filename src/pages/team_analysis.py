from dash import callback, dcc, html
from dash.dash_table import FormatTemplate
from dash.dash_table.Format import Format, Scheme
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data_access.cache import get_table
from src.data_access.tables import team_names
from src.team_analysis_panels import (
    build_injuries_panel,
    build_transactions_panel,
    filter_transactions_last_days,
)
from src.ui.cards import kpi_card as create_kpi_card
from src.theme.plotly import TRACE_HOVERLABEL, apply_dark_layout
from src.ui.sections import page_hero, section_header
from src.ui.tables import dark_datatable

TEAM_OPTIONS = [{"label": team, "value": team} for team in team_names]

GAME_OUTCOME_COLORS = {
    "W": "#3fb7d9",  # Blue for wins
    "L": "#e04848",  # Red for losses
}

TEAM_PLAYER_TABLE_COLUMNS: list = [
    dict(id="player", name="Player"),
    dict(id="games_played", name="GP", type="numeric"),
    dict(
        id="avg_ppg",
        name="PPG",
        type="numeric",
        format=Format(precision=1, scheme=Scheme.fixed),
    ),
    dict(id="avg_ts_percent", name="TS %", type="numeric", format=FormatTemplate.percentage(1)),
    dict(
        id="avg_plus_minus",
        name="+/-",
        type="numeric",
        format=Format(precision=1, scheme=Scheme.fixed),
    ),
    dict(id="is_mvp_candidate", name="Player type"),
    dict(id="ppg_rank", name="PPG rk", type="numeric"),
    dict(id="scoring_category", name="Scoring tier"),
]


def _rows_for_team(df: pd.DataFrame | None, column: str, team: str) -> pd.DataFrame:
    if df is None or df.empty or column not in df.columns:
        return pd.DataFrame()
    return df.loc[df[column] == team].copy()


def _dark_message_figure(message: str) -> go.Figure:
    """Placeholder chart with dark theme (avoids empty `{}` white Plotly default)."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color="rgb(141, 150, 148)", family="Inter, system-ui, sans-serif"),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(margin=dict(l=32, r=32, t=32, b=32))
    return fig


def _team_kpi_section_title(text: str) -> html.Div:
    return html.Div(text, className="team-kpi-card__title")


def _fmt_num(x: object, *, decimals: int = 1) -> str:
    try:
        v = float(x)
        if decimals <= 0:
            return str(int(round(v)))
        return f"{v:.{decimals}f}"
    except TypeError, ValueError:
        return str(x)


def _team_kpi_row(label: str, value: str, *, highlight: bool = False) -> html.Div:
    val_cls = "team-kpi-stat-val" + (" team-kpi-stat-val--accent" if highlight else "")
    return html.Div(
        [
            html.Span(label, className="team-kpi-stat-lbl"),
            html.Span(value, className=val_cls),
        ],
        className="team-kpi-stat-row",
    )


def _team_kpi_stack(*rows: html.Div) -> html.Div:
    return html.Div(list(rows), className="team-kpi-stat-stack")


def team_analysis_layout() -> html.Div:
    return html.Div(
        [
            page_hero(
                title="Per-team trends, health, and roster moves",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            create_kpi_card(
                                [
                                    html.H4("Select Team", className="kpi-card__section"),
                                    dcc.Dropdown(
                                        id="team-selector",
                                        options=TEAM_OPTIONS,
                                        value=team_names[0],
                                        clearable=False,
                                        className="dash-dropdown",
                                    ),
                                ],
                                class_name="kpi-card kpi-card--tool",
                            ),
                            html.Div(
                                id="kpi-boxes-1", className="kpi-card kpi-card--stat team-kpi-card"
                            ),
                            html.Div(
                                id="kpi-boxes-2", className="kpi-card kpi-card--stat team-kpi-card"
                            ),
                            html.Div(
                                id="kpi-boxes-3", className="kpi-card kpi-card--stat team-kpi-card"
                            ),
                        ],
                        className="kpi-container",
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Health & roster",
                                className="team-analysis-section-kicker text-muted text-uppercase small mb-2",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(id="injuries-table"),
                                        width=12,
                                        md=6,
                                    ),
                                    dbc.Col(
                                        html.Div(id="transactions-table"),
                                        width=12,
                                        md=6,
                                    ),
                                ],
                                className="g-3 team-analysis-panels-row",
                            ),
                        ],
                        className="mb-4",
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Season trends",
                                className="team-analysis-section-kicker text-muted text-uppercase small mb-2",
                            ),
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
                                        width=12,
                                        lg=6,
                                    ),
                                    dbc.Col(
                                        [
                                            section_header("Player Scoring Efficiency"),
                                            html.Div(
                                                id="team-player-efficiency-table",
                                                className="team-analysis-players-table-wrap",
                                            ),
                                        ],
                                        width=12,
                                        lg=6,
                                    ),
                                ],
                                className="g-3",
                            ),
                        ],
                    ),
                ],
                className="team-analysis-inner",
            ),
        ],
        className="team-analysis-page custom-padding",
    )


# Callbacks
@callback(Output("mov-plot", "figure"), Input("team-selector", "value"))
def update_mov(selected_team):
    """Update margin of victory plot"""
    if not selected_team:
        return _dark_message_figure("Select a team to load margin of victory.")

    filtered_df = _rows_for_team(get_table("mov"), "full_team", selected_team)

    if filtered_df.empty:
        return _dark_message_figure(
            "No margin-of-victory rows for this team in the current dataset."
        )

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


@callback(Output("team-player-efficiency-table", "children"), Input("team-selector", "value"))
def update_team_player_efficiency(selected_team):
    """Sortable table: PPG, TS%, and role - no on-chart labels."""
    if not selected_team:
        return html.Div("Select a team to load player stats.", className="small text-muted")

    team_df = _rows_for_team(get_table("player_stats"), "full_team", selected_team)
    if "season_type" in team_df.columns:
        team_df = team_df.loc[team_df["season_type"].astype(str) == "Regular Season"]
    if team_df.empty:
        return html.Div(
            "No player efficiency rows for this team in the current dataset.",
            className="small text-muted",
        )

    team_df = team_df.sort_values("avg_ppg", ascending=False, na_position="last")
    col_defs = [c for c in TEAM_PLAYER_TABLE_COLUMNS if c["id"] in team_df.columns]
    if not col_defs:
        return html.Div("No displayable columns for player stats.", className="small text-muted")
    ids = [c["id"] for c in col_defs]
    data = team_df[ids].to_dict("records")

    return dark_datatable(
        table_id="team-player-efficiency-datatable",
        columns=col_defs,
        data=data,
        cell_selectable=False,
        sort_action="native",
        page_size=20,
        style_table={"overflowX": "auto", "minWidth": "100%"},
        style_cell={
            "textAlign": "center",
            "minWidth": "72px",
            "maxWidth": "220px",
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_cell_conditional=[
            {"if": {"column_id": "player"}, "textAlign": "left", "minWidth": "140px"},
        ],
        style_header={
            "backgroundColor": "var(--surface-header)",
            "fontWeight": "600",
            "fontFamily": "var(--font-sans)",
            "borderBottom": "2px solid var(--accent)",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "var(--surface-cell)"},
        ],
    )


@callback(Output("injuries-table", "children"), Input("team-selector", "value"))
def update_injuries(selected_team):
    """Update injuries panel (custom layout)."""
    if not selected_team:
        return html.Div("No team selected", className="small text-muted")

    injuries_df = get_table("injuries")
    filtered_injuries = injuries_df.loc[injuries_df["team"] == selected_team].sort_values(
        by="scrape_date", ascending=False
    )

    return build_injuries_panel(filtered_injuries)


@callback(Output("transactions-table", "children"), Input("team-selector", "value"))
def update_transactions(selected_team):
    """Update transactions panel (last 90 days, custom layout)."""
    if not selected_team:
        return html.Div("No team selected", className="small text-muted")

    filtered_transactions = filter_transactions_last_days(
        get_table("transactions"), selected_team, days=90
    )

    return build_transactions_panel(filtered_transactions)


@callback(Output("kpi-boxes-1", "children"), [Input("team-selector", "value")])
def update_kpi_boxes_1(selected_team):
    """Update team ratings KPI box"""
    if not selected_team:
        return []

    kpi_values = _rows_for_team(get_table("team_adv_stats"), "team", selected_team)

    if kpi_values.empty:
        return [html.Div("No data available", className="small text-muted")]

    r0 = kpi_values.iloc[0]
    return [
        _team_kpi_section_title("Team ratings"),
        _team_kpi_stack(
            _team_kpi_row("Net rating", _fmt_num(r0["nrtg"]), highlight=True),
            _team_kpi_row("Offensive rating", _fmt_num(r0["ortg"])),
            _team_kpi_row("Defensive rating", _fmt_num(r0["drtg"])),
        ),
    ]


@callback(Output("kpi-boxes-2", "children"), [Input("team-selector", "value")])
def update_kpi_boxes_2(selected_team):
    """Update advanced stats KPI box"""
    if not selected_team:
        return []

    kpi_values = _rows_for_team(get_table("team_adv_stats"), "team", selected_team)

    if kpi_values.empty:
        return [html.Div("No data available", className="small text-muted")]

    r0 = kpi_values.iloc[0]
    return [
        _team_kpi_section_title("Advanced stats"),
        _team_kpi_stack(
            _team_kpi_row("SRS", _fmt_num(r0["srs"])),
            _team_kpi_row("Pace", _fmt_num(r0["pace"])),
            _team_kpi_row("True shooting", f"{float(r0['ts_percent']):.1%}", highlight=True),
        ),
    ]


@callback(Output("kpi-boxes-3", "children"), [Input("team-selector", "value")])
def update_kpi_boxes_3(selected_team):
    """Update opponent stats KPI box"""
    if not selected_team:
        return []

    kpi_values = _rows_for_team(get_table("team_adv_stats"), "team", selected_team)

    if kpi_values.empty:
        return [html.Div("No data available", className="small text-muted")]

    r0 = kpi_values.iloc[0]
    try:
        tov_s = f"{float(r0['tov_percent_opp']):.1f}%"
    except TypeError, ValueError:
        tov_s = str(r0["tov_percent_opp"])
    try:
        efg_s = f"{float(r0['efg_percent_opp']):.1%}"
    except TypeError, ValueError:
        efg_s = str(r0["efg_percent_opp"])

    return [
        _team_kpi_section_title("Opponent stats"),
        _team_kpi_stack(
            _team_kpi_row("Opp. turnover rate", tov_s),
            _team_kpi_row("Opp. effective FG", efg_s, highlight=True),
        ),
    ]
