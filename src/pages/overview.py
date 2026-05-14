from dash import callback, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

from src.ui.cards import kpi_card as create_kpi_card
from src.data_cols.player_stats import player_scoring_efficiency_columns
from src.data_cols.standings import standings_columns
from src.database import (
    bans_df,
    contract_value_analysis_df,
    injuries_df,
    player_stats_df,
    standings_df,
    team_contracts_analysis_df,
    team_ratings_df,
)
from src.theme.plotly import TRACE_HOVERLABEL, apply_dark_layout
from src.ui.sections import page_hero, section_header
from src.ui.tables import dark_datatable
from src.utils import generate_team_ratings_figure, scoring_efficiency_season_config

# Scoring-efficiency season filter (aligned initial table + dropdown at import time)
_SCORING_SEASON_DEFAULT, _SCORING_SEASON_OPTIONS = scoring_efficiency_season_config()

# Constants
VALUE_ANALYSIS_COLORS = {
    "Superstars": "#9362DA",
    "Great Value": "#3fb7d9",
    "Normal": "#383b3d",
    "Bad Value": "#e04848",
}

# Data preprocessing
team_contracts_analysis_df = team_contracts_analysis_df.sort_values(
    by="team_pct_salary_earned", ascending=True
)


def _regular_season_league_avg_ts_percent() -> float:
    return float(player_stats_df.query("season_type == 'Regular Season'")["avg_ts_percent"].mean())


def _scoring_efficiency_records(selected_season: str | None) -> list[dict]:
    """Players with 20+ PPG for the selected season; TS% benchmark vs reg.-season league avg."""
    season = selected_season or "Regular Season"
    rs_avg = _regular_season_league_avg_ts_percent()
    filtered = player_stats_df.query(
        "season_type == @season and avg_ppg >= 20", local_dict={"season": season}
    )
    if filtered.empty:
        return []
    rows: list[dict] = []
    for _, row in filtered.iterrows():
        ts = float(row["avg_ts_percent"])
        rows.append(
            {
                "player": str(row["player"]),
                "team": str(row["team"]),
                "avg_ppg": round(float(row["avg_ppg"]), 1),
                "avg_ts_percent": ts,
                "games_played": int(row["games_played"]),
                "is_mvp_candidate": str(row["is_mvp_candidate"]),
                "ts_vs_reg_pp": round((ts - rs_avg) * 100, 1),
            }
        )
    rows.sort(key=lambda r: r["avg_ppg"], reverse=True)
    return rows


def create_player_scoring_efficiency_table():
    return dark_datatable(
        columns=player_scoring_efficiency_columns,
        data=_scoring_efficiency_records(_SCORING_SEASON_DEFAULT),
        table_id="player-scoring-efficiency-table",
        sort_action="native",
        sort_mode="single",
        sort_by=[{"column_id": "avg_ppg", "direction": "desc"}],
        page_size=15,
        style_cell={"padding": "8px", "minWidth": "72px"},
        style_data_conditional=[
            {
                "if": {
                    "filter_query": '{is_mvp_candidate} contains "Top 5"',
                    "column_id": "is_mvp_candidate",
                },
                "color": "#9362DA",
                "fontWeight": "600",
            },
            {
                "if": {"filter_query": "{ts_vs_reg_pp} >= 0", "column_id": "avg_ts_percent"},
                "color": "#7ee8d4",
            },
            {
                "if": {"filter_query": "{ts_vs_reg_pp} < 0", "column_id": "avg_ts_percent"},
                "color": "#e8e6e3",
            },
        ],
    )


def create_standings_table(conference_name, data):
    return dark_datatable(
        columns=standings_columns,
        data=data,
        table_id=f"{conference_name.lower()}-standings-table",
        style_cell={"padding": "8px"},
        hidden_columns=["active_protocols", "conference", "team"],
        cell_selectable=False,
        css=[{"selector": ".show-hide", "rule": "display: none"}],
        sort_action="native",
        page_size=15,
    )


def create_player_value_analysis_chart():
    fig = px.scatter(
        contract_value_analysis_df,
        x="salary",
        y="avg_mvp_score",
        labels={
            "salary": "Annual Salary",
            "avg_mvp_score": "Average MVP Score",
        },
        title="Player Contract Value vs Performance",
        custom_data=[
            "player",
            "team",
            "avg_mvp_score",
            "salary",
            "color_var",
            "games_played",
            "games_missed",
        ],
        color="color_var",
        color_discrete_map=VALUE_ANALYSIS_COLORS,
    )

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_xaxes(tickformat="$,.0f")
    fig.update_layout(
        legend_title_text="Player Category",
        title={"x": 0.5, "xanchor": "center"},
    )

    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Team:</b> %{customdata[1]}<br>"
            "<b>Category:</b> %{customdata[4]}<br>"
            "<b>MVP Score:</b> %{customdata[2]:.2f}<br>"
            "<b>Salary:</b> $%{customdata[3]:,}<br>"
            "<b>Games Played:</b> %{customdata[5]}<br>"
            "<b>Games Missed:</b> %{customdata[6]}<br>"
            "<extra></extra>"
        ),
    )

    return fig


def create_team_contract_analysis_chart():
    fig = px.bar(
        team_contracts_analysis_df,
        x="team_pct_salary_earned",
        y="team",
        color="win_percentage",
        color_continuous_scale=[[0, "#e04848"], [0.5, "#383b3d"], [1, "#3fb7d9"]],
        labels={
            "team_pct_salary_earned": "% Salary Value Earned",
            "team": "Team",
            "win_percentage": "Win %",
        },
        title="Team Contract Efficiency vs Win Percentage",
        custom_data=[
            "team",
            "win_percentage",
            "sum_salary_earned",
            "sum_salary_earned_max",
            "team_pct_salary_earned",
            "value_lost_from_injury",
            "team_pct_salary_lost",
        ],
    )

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_xaxes(tickformat=".0%")
    fig.update_layout(title={"x": 0.5, "xanchor": "center"})

    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Win Percentage:</b> %{customdata[1]:.1%}<br>"
            "<b>Salary Value Earned:</b> %{customdata[4]:.1%}<br>"
            "<b>Salary Lost to Injury:</b> %{customdata[6]:.1%}<br>"
            "<b>Total Value Earned:</b> $%{customdata[2]:,}<br>"
            "<b>Total Value Lost:</b> $%{customdata[5]:,}<br>"
            "<extra></extra>"
        ),
    )

    return fig


_overview_scrape = bans_df["scrape_time"][0]

# Layout
overview_layout = html.Div(
    [
        page_hero(
            title="The league at a glance.",
            meta=[
                html.Div(
                    f"League snapshot · {_overview_scrape.strftime('%A, %B %d')}",
                    className="text-muted small",
                ),
                html.Div(
                    _overview_scrape.strftime("Last updated: %A, %B %d at %H:%M UTC"),
                    className="text-muted small",
                ),
            ],
        ),
        # KPI Section
        html.Div(
            [
                # Home/Road Record KPI
                create_kpi_card(
                    [
                        html.Div(
                            f"{bans_df['tot_wins'][0]} - {bans_df['tot_wins'][1]}",
                            className="kpi-card__value",
                        ),
                        html.Div("League wide home vs road wins", className="kpi-card__title"),
                        html.Div(
                            f"{bans_df['win_pct'][0] * 100:.0f}% - {bans_df['win_pct'][1] * 100:.0f}% win percentage splits",
                            className="kpi-card__sub",
                        ),
                    ]
                ),
                # Points Per Game KPI
                create_kpi_card(
                    [
                        html.Div(
                            f"{bans_df['avg_pts'][0]:.1f}",
                            className="kpi-card__value",
                        ),
                        html.Div("League average points per game", className="kpi-card__title"),
                        html.Div(
                            f"{((bans_df['avg_pts'][0] - bans_df['last_yr_ppg'][0]) / bans_df['avg_pts'][0]) * 100:.2f}% difference vs last season",
                            className="kpi-card__sub",
                        ),
                    ]
                ),
                # Injury Report KPI
                create_kpi_card(
                    [
                        html.Div(
                            str(len(injuries_df)),
                            className="kpi-card__value",
                        ),
                        html.Div("Players on injury report", className="kpi-card__title"),
                        html.Div(
                            "All injury designations",
                            className="kpi-card__sub",
                        ),
                    ]
                ),
                # Upcoming Games KPI
                create_kpi_card(
                    [
                        html.Div(
                            bans_df["upcoming_game_date"][0].strftime("%B %d"),
                            className="kpi-card__value",
                        ),
                        html.Div(
                            f"{bans_df['upcoming_games'][0]} upcoming games",
                            className="kpi-card__title",
                        ),
                        html.Div(
                            bans_df["upcoming_game_date"][0].strftime("%A"),
                            className="kpi-card__sub",
                        ),
                    ]
                ),
            ],
            className="kpi-container",
        ),
        # Standings Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        section_header("Western Conference"),
                        create_standings_table(
                            "Western",
                            standings_df.query('conference == "Western"').to_dict("records"),
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        section_header("Eastern Conference"),
                        create_standings_table(
                            "Eastern",
                            standings_df.query('conference == "Eastern"').to_dict("records"),
                        ),
                    ],
                    width=6,
                ),
            ],
            style={"margin-bottom": "30px"},
        ),
        # Charts Section 1
        dbc.Row(
            [
                dbc.Col(
                    [
                        section_header("Player Scoring Efficiency"),
                        html.P(
                            "Players averaging 20+ PPG for the selected season. "
                            "True shooting % is tinted when at or above the regular-season league average.",
                            className="text-muted small mb-2",
                        ),
                        html.Div(
                            [
                                html.Span("Season type", className="text-muted small me-2"),
                                dcc.Dropdown(
                                    id="scoring-efficiency-season",
                                    options=_SCORING_SEASON_OPTIONS,
                                    value=_SCORING_SEASON_DEFAULT,
                                    clearable=False,
                                    className="dash-dropdown flex-grow-1",
                                    style={"minWidth": "200px", "maxWidth": "420px"},
                                ),
                            ],
                            className="d-flex flex-wrap align-items-center gap-2 mb-3",
                        ),
                        create_player_scoring_efficiency_table(),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        section_header("Team Ratings"),
                        dcc.Graph(
                            id="team-ratings-plot",
                            figure=generate_team_ratings_figure(df=team_ratings_df),
                            style={"height": "500px"},
                        ),
                    ],
                    width=6,
                ),
            ],
            style={"margin-bottom": "30px"},
        ),
        # Charts Section 2
        dbc.Row(
            [
                dbc.Col(
                    [
                        section_header("Player Value Analysis"),
                        dcc.Graph(
                            id="player-value-analysis-plot",
                            figure=create_player_value_analysis_chart(),
                            style={"height": "500px"},
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        section_header("Team Contract Efficiency"),
                        dcc.Graph(
                            id="contract-bar-plot",
                            figure=create_team_contract_analysis_chart(),
                            style={"height": "500px"},
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
    ],
    className="custom-padding",
)


@callback(
    Output("player-scoring-efficiency-table", "data"),
    Input("scoring-efficiency-season", "value"),
)
def update_scoring_efficiency_table(selected_season):
    return _scoring_efficiency_records(selected_season)
