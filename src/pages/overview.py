from dash import callback, dash_table, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

from src.data_cols.standings import standings_columns
from src.data import (
    bans_df,
    contract_value_analysis_df,
    player_stats_df,
    standings_df,
    team_contracts_analysis_df,
    team_ratings_df,
)
from src.utils import generate_team_ratings_figure

team_contracts_analysis_df = team_contracts_analysis_df.sort_values(
    by="team_pct_salary_earned", ascending=True
)

# it's not baaaaaaad idk
overview_layout = (
    html.Div(
        [
            # Single div to contain all four KPIs
            html.Div(
                [
                    # KPI 1
                    html.Div(
                        [
                            html.Div(
                                f"{bans_df['tot_wins'][0]} - {bans_df['tot_wins'][1]}",
                                style={"fontSize": 24},
                            ),
                            html.Div("League Wide Home - Road Win Record"),
                            html.Div(
                                f"{bans_df['win_pct'][0] * 100:.0f}% - {bans_df['win_pct'][1] * 100:.0f}% Win Percentage Splits"  # noqa
                            ),
                        ],
                        className="kpi-card",
                    ),
                    # KPI 2
                    html.Div(
                        [
                            html.Div(bans_df["avg_pts"][0], style={"fontSize": 24}),
                            html.Div("League Average Points Scored / Game"),
                            html.Div(
                                f"{((bans_df['avg_pts'][0] - bans_df['last_yr_ppg'][0]) / bans_df['avg_pts'][0]) * 100:.2f}% difference from Last Season"  # noqa
                            ),
                        ],
                        className="kpi-card",
                    ),
                    # KPI 3
                    html.Div(
                        [
                            html.Div(
                                bans_df["sum_active_protocols"][0],
                                style={"fontSize": 24},
                            ),
                            html.Div("Active Players in COVID Protocols"),
                            html.Div(bans_df["protocols_text"][0]),
                        ],
                        className="kpi-card",
                    ),
                    # KPI 4
                    html.Div(
                        [
                            html.Div(
                                bans_df["upcoming_game_date"][0].strftime("%A, %B %d"),
                                style={"fontSize": 24},
                            ),
                            html.Div(f"{bans_df['upcoming_games'][0]} Upcoming Games"),
                            html.Div(""),
                        ],
                        className="kpi-card",
                    ),
                ],
                className="kpi-container",
                style={"display": "flex", "justify-content": "space-between"},
            ),
            html.Div(
                [
                    html.Br(),
                    html.Div(
                        f"Last Updated {(bans_df['scrape_time'][0]).strftime('%A, %B %d %-I:%M %p UTC')}"  # noqa
                    ),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1("Western Conference"),
                            dash_table.DataTable(
                                id="western-standings-table",
                                columns=standings_columns,
                                data=standings_df.query(
                                    'conference == "Western"'
                                ).to_dict("records"),
                                style_cell={"background-color": "#383b3d"},
                                hidden_columns=[
                                    "active_protocols",
                                    "conference",
                                    "team",
                                ],
                                css=[
                                    {
                                        "selector": ".show-hide",
                                        "rule": "display: none",
                                    }
                                ],
                                sort_action="native",
                                page_size=15,
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.H1("Eastern Conference"),
                            dash_table.DataTable(
                                id="eastern-standings-table",
                                columns=standings_columns,
                                data=standings_df.query(
                                    'conference == "Eastern"'
                                ).to_dict("records"),
                                style_cell={"background-color": "#383b3d"},
                                hidden_columns=[
                                    "active_protocols",
                                    "conference",
                                    "team",
                                ],
                                css=[
                                    {
                                        "selector": ".show-hide",
                                        "rule": "display: none",
                                    }
                                ],
                                sort_action="native",
                                page_size=15,
                            ),
                        ],
                        width=6,
                    ),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            id="season-selector",
                            options=[
                                {
                                    "label": "Regular Season",
                                    "value": "Regular Season",
                                },
                                {"label": "Playoffs", "value": "Playoffs"},
                            ],
                            clearable=False,
                            value="Regular Season",
                        ),
                        width={"size": 2},
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Player Scoring Efficiency"),
                            dcc.Graph(id="player-scoring-efficiency-plot"),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.H3("Team Ratings"),
                            dcc.Graph(
                                id="team-ratings-plot",
                                figure=generate_team_ratings_figure(df=team_ratings_df),
                            ),
                        ],
                        width=6,
                    ),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Player Value Analysis"),
                            dcc.Graph(
                                id="player-value-analysis-plot",
                                figure=px.scatter(
                                    contract_value_analysis_df,
                                    x="salary",
                                    y="avg_mvp_score",
                                    labels={
                                        "salary": "Salary",
                                        "avg_mvp_score": "Average MVP Score",
                                    },
                                    custom_data=[
                                        "player",
                                        "team",
                                        "avg_mvp_score",
                                        "salary",
                                        "color_var",
                                    ],
                                    color="color_var",
                                    color_discrete_map={
                                        "Superstars": "purple",
                                        "Great Value": "green",
                                        "Normal": "gray",
                                        "Bad Value": "red",
                                    },
                                )
                                .update_traces(
                                    hoverlabel=dict(
                                        bgcolor="white",
                                        font_size=12,
                                        font_family="Rockwell",
                                    ),
                                    hovertemplate="<b>%{customdata[0]}</b><br>"
                                    "%{customdata[1]}<br>"
                                    "<b>Average MVP Score:</b> %{customdata[2]}<br>"
                                    "<b>Salary:</b> $%{customdata[3]:,}<br>"
                                    "<b>Type:</b> %{customdata[4]}<br>",
                                )
                                .update_layout(legend_title_text=""),
                            ),
                        ],
                        width={"size": 6},
                    ),
                    dbc.Col(
                        [
                            html.H3("Team Contract Value Analysis"),
                            dcc.Graph(
                                id="contract-bar-plot",
                                figure=px.bar(
                                    team_contracts_analysis_df,
                                    x="team_pct_salary_earned",
                                    y="team",
                                    color="win_percentage",
                                    color_continuous_scale=[
                                        (0, "red"),
                                        (1, "green"),
                                    ],
                                    labels={
                                        "team_pct_salary_earned": "Team % Salary Earned",
                                        "team": "Team",
                                    },
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
                                .update_traces(
                                    hoverlabel=dict(
                                        bgcolor="white",
                                        font_size=12,
                                        font_family="Rockwell",
                                    ),
                                    hovertemplate="<b>%{customdata[0]}</b><br>"
                                    "<b>Win %:</b> %{customdata[1]:.1%}<br>"
                                    "<b>% Salary Value Earned:</b> %{customdata[4]:.1%}<br>"
                                    "<b>% Salary Value Lost from Injury:</b> %{customdata[6]:.1%}<br>"  # noqa
                                    "<b>Total Salary Value Earned:</b> %{customdata[2]:$,}<br>"
                                    "<b>Total Salary Value Lost from Injury:</b> %{customdata[5]:$,}",  # noqa
                                )
                                .update_layout(legend_title_text=""),
                            ),
                        ],
                        width={"size": 6},
                    ),
                ],
            ),
        ],
        className="custom-padding",
    ),
)


@callback(
    Output("player-scoring-efficiency-plot", "figure"),
    Input("season-selector", "value"),
)
def update_graph(selected_season):
    regular_season_ts_percent_avg = player_stats_df.query(
        "season_type == 'Regular Season'"
    )["avg_ts_percent"].mean()

    filtered_df = player_stats_df.copy().query(
        f"season_type == '{selected_season}' & avg_ppg >= 20"
    )

    fig = px.scatter(
        filtered_df,
        x="avg_ppg",
        y="avg_ts_percent",
        labels={
            "avg_ppg": "Average PPG",
            "avg_ts_percent": "Average TS%",
        },
        color="is_mvp_candidate",
        color_discrete_map={
            "Top 5 MVP Candidate": "orange",
            "Other": "grey",
        },
        custom_data=[
            "player",
            "team",
            "avg_ppg",
            "avg_ts_percent",
            "is_mvp_candidate",
        ],
    )

    fig.add_hline(
        y=regular_season_ts_percent_avg,
        line_width=3,
        line_dash="dash",
        line_color="black",
        opacity=0.5,
    )

    fig.update_layout(legend_title_text="", yaxis_tickformat=".0%")

    fig.update_traces(
        marker=dict(
            size=8,
        ),
        mode="markers",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        hovertemplate="<b>%{customdata[0]}</b><br>"
        "%{customdata[1]}<br>"
        "<b>Average PPG:</b> %{customdata[2]}<br>"
        "<b>Average TS%:</b> %{customdata[3]:.1%}<br>"
        "<b>Type:</b> %{customdata[4]}",
    )

    fig.add_annotation(
        x=player_stats_df["avg_ppg"].max(),
        y=regular_season_ts_percent_avg - 0.01,
        text="League Average TS%",
        yanchor="top",
        showarrow=False,
    )

    return fig
