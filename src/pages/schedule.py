from __future__ import annotations

from typing import Any

import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from src.config import SINGLE_BAR_COLOR
from src.data_cols.future_schedule import future_schedule_columns
from src.database import (
    game_types_df,
    past_schedule_analysis_df,
    preseason_odds_df,
    schedule_season_remaining_df,
    schedule_tonights_games_df,
    team_blown_leads_df,
    team_odds_outcomes_df,
)
from src.theme.plotly import TRACE_HOVERLABEL, apply_dark_layout
from src.ui.sections import page_hero, section_header
from src.ui.tables import dark_datatable

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


def _truthy_great_value(raw: object) -> bool:
    try:
        return int(raw) == 1
    except TypeError, ValueError:
        return False


def _fmt_game_date(val: Any) -> str:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return "-"
    try:
        return pd.Timestamp(val).strftime("%a %b %d").replace(" 0", " ")
    except ValueError, TypeError, OSError:
        return str(val)


def _fmt_pct(val: Any) -> str:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return "-"
    try:
        return f"{float(val):.1%}"
    except TypeError, ValueError:
        return "-"


def _fmt_rank(val: Any) -> str:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return "-"
    try:
        x = float(val)
        if x == int(x):
            return str(int(x))
        return f"{x:.1f}"
    except TypeError, ValueError:
        return "-"


def create_tonight_games_cards() -> html.Div:
    """Tonight slate as responsive matchup cards (same fields as former DataTable)."""
    df = schedule_tonights_games_df
    if df is None or df.empty:
        return html.Div(
            "No games on the slate for this view.",
            className="schedule-empty text-muted small",
        )

    slate_date_label: str | None = None
    if "game_date" in df.columns:
        parsed = pd.to_datetime(df["game_date"], errors="coerce").dropna()
        if not parsed.empty:
            unique_days = pd.Series(parsed.dt.normalize().unique())
            if len(unique_days) == 1:
                slate_date_label = _fmt_game_date(unique_days.iloc[0])

    cards: list[html.Div] = []
    for _, row in df.iterrows():
        home_gv = _truthy_great_value(row.get("home_is_great_value"))
        away_gv = _truthy_great_value(row.get("away_is_great_value"))
        away_line = str(row.get("away_team_odds") or row.get("away_team") or "-")
        home_line = str(row.get("home_team_odds") or row.get("home_team") or "-")

        meta_children: list = []
        if slate_date_label is None:
            meta_children.append(
                html.Span(_fmt_game_date(row.get("game_date")), className="schedule-card-date"),
            )
        meta_children.append(
            html.Span(str(row.get("start_time") or "-"), className="schedule-card-time"),
        )
        meta_cls = "schedule-card-meta"
        if slate_date_label is not None:
            meta_cls += " schedule-card-meta--solo-time"

        cards.append(
            html.Div(
                [
                    html.Div(
                        meta_children,
                        className=meta_cls,
                    ),
                    html.Div(
                        [
                            html.Div(
                                away_line,
                                className=(
                                    "schedule-card-team schedule-card-team--away"
                                    + (" schedule-card-team--value" if away_gv else "")
                                ),
                            ),
                            html.Span("@", className="schedule-card-at"),
                            html.Div(
                                home_line,
                                className=(
                                    "schedule-card-team schedule-card-team--home"
                                    + (" schedule-card-team--value" if home_gv else "")
                                ),
                            ),
                        ],
                        className="schedule-card-matchup",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span("Avg team rank", className="schedule-card-stat-lbl"),
                                    html.Span(
                                        _fmt_rank(row.get("avg_team_rank")),
                                        className="schedule-card-stat-val",
                                    ),
                                ],
                                className="schedule-card-stat",
                            ),
                            html.Div(
                                [
                                    html.Span("Home win %", className="schedule-card-stat-lbl"),
                                    html.Span(
                                        _fmt_pct(row.get("home_team_predicted_win_pct")),
                                        className="schedule-card-stat-val",
                                    ),
                                ],
                                className="schedule-card-stat",
                            ),
                            html.Div(
                                [
                                    html.Span("Road win %", className="schedule-card-stat-lbl"),
                                    html.Span(
                                        _fmt_pct(row.get("away_team_predicted_win_pct")),
                                        className="schedule-card-stat-val",
                                    ),
                                ],
                                className="schedule-card-stat",
                            ),
                        ],
                        className="schedule-card-stats",
                    ),
                ],
                className="schedule-tonight-card",
            )
        )

    wrap_children: list = []
    if slate_date_label:
        wrap_children.append(
            html.Div(slate_date_label, className="schedule-tonight-slate-date"),
        )
    wrap_children.append(html.Div(cards, className="schedule-tonight-grid"))
    return html.Div(wrap_children, className="schedule-tonight-slate")


def create_full_schedule_table():
    enhanced_cell_style = {
        "minWidth": "100px",
        "maxWidth": "180px",
        "whiteSpace": "normal",
        "height": "auto",
    }

    return dark_datatable(
        table_id="schedule-full-table",
        columns=future_schedule_columns,
        data=schedule_season_remaining_df.to_dict("records"),
        cell_selectable=False,
        sort_action="native",
        page_size=15,
        style_cell=enhanced_cell_style,
        style_header={
            "backgroundColor": "var(--surface-header)",
            "fontWeight": "600",
            "textAlign": "center",
            "padding": "12px",
            "borderBottom": "2px solid var(--accent)",
            "fontFamily": "var(--font-sans)",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "var(--surface-cell)",
            },
        ],
    )


def create_strength_of_schedule_plot():
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

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(
        legend_title_text="",
        xaxis_tickformat=".0%",
        title={"x": 0.5, "xanchor": "center"},
    )

    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
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

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(title={"x": 0.5, "xanchor": "center"})

    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
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

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(
        legend_title_text="",
        xaxis_tickformat=".0%",
        title={"x": 0.5, "xanchor": "center"},
    )

    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
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

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(title={"x": 0.5, "xanchor": "center"})

    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Comebacks:</b> %{customdata[3]}<br>"
            "<b>Blown Leads:</b> %{customdata[1]}<br>"
            "<b>Net Comebacks:</b> %{customdata[5]}<br>"
            "<b>Comeback Rank:</b> %{customdata[4]}<br>"
            "<b>Blown Lead Rank:</b> %{customdata[2]}<br>"
            "<extra></extra>"
        ),
    )
    return fig


def create_game_types_plot():
    fig = px.bar(
        game_types_df,
        x="n",
        y="game_type",
        labels={"n": "Number of Games", "game_type": "Game Type"},
        title="Distribution of Games by Margin",
        color_discrete_sequence=[SINGLE_BAR_COLOR],
        custom_data=["game_type", "n", "explanation"],
    )

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(title={"x": 0.5, "xanchor": "center"})

    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
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


def _schedule_intel_bar() -> html.Div:
    return html.Div(
        html.Div(
            [
                html.Div(
                    [
                        html.Span("Moneyline odds from ", className="schedule-intel-muted"),
                        html.A(
                            html.Img(
                                src="../assets/draftkings.png",
                                height="28",
                                alt="DraftKings",
                                className="schedule-intel-logo",
                            ),
                            href="https://www.draftkings.com",
                            target="_blank",
                            rel="noopener noreferrer",
                            className="schedule-intel-dk",
                        ),
                    ],
                    className="schedule-intel-group",
                ),
                html.Span("", className="schedule-intel-dot"),
                html.Span("Highlight = strong ML value", className="schedule-intel-legend"),
            ],
            className="schedule-intel-bar-inner",
        ),
        className="schedule-intel-bar",
    )


schedule_layout = html.Div(
    [
        page_hero(
            title="Schedule",
            subtitle="Tonight's games and season-long schedule intel.",
        ),
        _schedule_intel_bar(),
        html.Div(
            [
                html.Div(
                    [
                        html.Span("Games & odds", className="schedule-panel-kicker"),
                        html.P(
                            [
                                "Odds shown here are generated from a logistic regression model. ",
                                "See the ",
                                html.Span("About", className="fw-semibold"),
                                " tab for methodology, data sources, and more.",
                            ],
                            className="schedule-panel-lede text-muted small mb-0",
                        ),
                    ],
                    className="schedule-panel-head-text",
                ),
                html.Div(
                    [
                        html.Label("Schedule view", className="schedule-field-label"),
                        dcc.Dropdown(
                            id="schedule-table-selector",
                            options=SCHEDULE_TABLE_OPTIONS,
                            value="tonights-games",
                            clearable=False,
                            className="dash-dropdown schedule-dropdown",
                        ),
                    ],
                    className="schedule-toolbar",
                ),
                html.Div(id="schedule-table", className="schedule-panel-body"),
            ],
            className="schedule-panel schedule-panel--games",
        ),
        html.Div(
            [
                section_header("NBA Schedule Analysis"),
                html.P(
                    "League-wide views: strength of schedule, spreads, preseason lines, and more.",
                    className="schedule-panel-lede schedule-panel-lede--center text-muted small",
                ),
                html.Div(
                    [
                        html.Label("Analysis plot", className="schedule-field-label"),
                        dcc.Dropdown(
                            id="schedule-plot-selector",
                            options=SCHEDULE_PLOT_OPTIONS,
                            value="strength-of-schedule",
                            clearable=False,
                            className="dash-dropdown schedule-dropdown",
                        ),
                    ],
                    className="schedule-toolbar schedule-toolbar--analysis",
                ),
                html.Div(
                    dcc.Graph(
                        id="schedule-plot",
                        style={"height": "min(70vh, 640px)", "minHeight": "420px"},
                        config={"displayModeBar": False, "displaylogo": False},
                    ),
                    className="schedule-plot-frame",
                ),
            ],
            className="schedule-panel schedule-panel--analysis",
        ),
    ],
    className="schedule-page custom-padding",
)


# Callbacks
@callback(Output("schedule-table", "children"), [Input("schedule-table-selector", "value")])
def update_schedule_table(selected_value):
    """Tonight's slate as cards; full season as sortable table."""
    if selected_value == "tonights-games":
        return create_tonight_games_cards()
    if selected_value == "full-schedule":
        return html.Div(create_full_schedule_table(), className="schedule-datatable-wrap")
    return html.Div("No data available", className="schedule-empty text-muted small")


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

    return create_strength_of_schedule_plot()
