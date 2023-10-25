from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from src.data_cols.standings import standings_columns
from src.data import (
    bans_df,
    contract_value_analysis_df,
    scorers_df,
    standings_df,
    team_contracts_analysis_df,
    team_ratings_df,
)

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
                                f"{bans_df['win_pct'][0] * 100:.0f}% - {bans_df['win_pct'][1] * 100:.0f}% Win Percentage Splits"
                            ),
                        ],
                        className="kpi-box",
                    ),
                    # KPI 2
                    html.Div(
                        [
                            html.Div(bans_df["avg_pts"][0], style={"fontSize": 24}),
                            html.Div("League Average Points Scored / Game"),
                            html.Div(
                                f"{((bans_df['avg_pts'][0] - bans_df['last_yr_ppg'][0]) / bans_df['avg_pts'][0]) * 100:.2f}% difference from Last Season"
                            ),
                        ],
                        className="kpi-box",
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
                        className="kpi-box",
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
                        className="kpi-box",
                    ),
                ],
                className="kpi-container",
                style={"display": "flex", "justify-content": "space-between"},
            ),
            html.Div(
                [
                    # Left side (Western Conference)
                    html.Div(
                        [
                            html.H1("Western Conference"),
                            dash_table.DataTable(
                                id="western-standings-table",
                                columns=standings_columns,
                                data=standings_df.query(
                                    'conference == "Western"'
                                ).to_dict("records"),
                                hidden_columns=[
                                    "active_protocols",
                                    "conference",
                                    "team",
                                ],
                                css=[
                                    {"selector": ".show-hide", "rule": "display: none"}
                                ],
                            ),
                        ],
                        style={
                            "width": "49%",
                            "display": "inline-block",
                            "margin-right": "30px",
                        },
                    ),
                    # Right side (Eastern Conference)
                    html.Div(
                        [
                            html.H1("Eastern Conference"),
                            dash_table.DataTable(
                                id="eastern-standings-table",
                                columns=standings_columns,
                                data=standings_df.query(
                                    'conference == "Eastern"'
                                ).to_dict("records"),
                                hidden_columns=[
                                    "active_protocols",
                                    "conference",
                                    "team",
                                ],
                                css=[
                                    {"selector": ".show-hide", "rule": "display: none"}
                                ],
                            ),
                        ],
                        style={"width": "49%", "display": "inline-block"},
                    ),
                ]
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(
                            id="season-selector",
                            options=[
                                {"label": "Regular Season", "value": "Regular Season"},
                                {"label": "Playoffs", "value": "Playoffs"},
                            ],
                            clearable=False,
                            value="Regular Season",
                        )
                    ),
                    dcc.Graph(
                        id="player-scoring-efficiency-plot",
                        style={"width": "50%", "display": "inline-block"},
                    ),
                    dcc.Graph(
                        id="team-ratings-plot",
                        style={"width": "50%", "display": "inline-block"},
                        figure=px.scatter(
                            team_ratings_df,
                            x="ortg",
                            y="drtg",
                            text="team",
                            labels={
                                "ortg": "Offensive Rating (ORTG)",
                                "drtg": "Defensive Rating (DRTG)",
                            },
                        ),
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="player-value-analysis-plot",
                        style={"width": "50%", "display": "inline-block"},
                        figure=px.scatter(
                            contract_value_analysis_df,
                            x="salary",
                            y="player_mvp_calc_avg",
                            color="color_var",
                            color_discrete_map={
                                "Superstars": "purple",
                                "Great Value": "green",
                                "Normal": "gray",
                                "Bad Value": "red",
                            },  # Apply the custom color scale
                            labels={
                                "player": "Player",
                                "team": "Team",
                                "salary": "Salary",
                                "player_mvp_calc_avg": "Player MVP Category",
                            },
                        ),
                    ),
                    dcc.Graph(
                        id="contract-bar-plot",
                        style={"width": "50%", "display": "inline-block"},
                        figure=px.bar(
                            team_contracts_analysis_df,
                            x="team_pct_salary_earned",
                            y="team",
                            color="win_percentage",
                            color_continuous_scale=[(0, "red"), (1, "green")],
                            labels={
                                "team_pct_salary_earned": "Team % Salary Earned",
                                "team": "Team",
                            },
                        ),
                    ),
                ]
            ),
        ],
        className="custom-padding",
    ),
)

avg_ortg = team_ratings_df["ortg"].mean()
avg_drtg = team_ratings_df["drtg"].mean()

average_ortg_line = go.Scatter(
    x=[avg_ortg, avg_ortg],
    y=[team_ratings_df["drtg"].min(), team_ratings_df["drtg"].max()],
    mode="lines",
    name="Average ORTG",
    line=dict(color="red", dash="dash"),
)

average_drtg_line = go.Scatter(
    x=[team_ratings_df["ortg"].min(), team_ratings_df["ortg"].max()],
    y=[avg_drtg, avg_drtg],
    mode="lines",
    name="Average DRTG",
    line=dict(color="blue", dash="dash"),
)

# Add team logos using image annotations
team_logos = []
for i, row in team_ratings_df.iterrows():
    team_logo = row["team_logo"]
    team_logos.append(
        go.layout.Image(
            source=f"assets/logos/{team_logo}",  # Assuming logos are in an 'assets' directory
            x=row["ortg"],  # X coordinate
            y=row["drtg"],  # Y coordinate
            xref="x",
            yref="y",
            xanchor="center",
            yanchor="bottom",
            sizex=0.2,
            sizey=0.2,
        )
    )


@callback(
    Output("player-scoring-efficiency-plot", "figure"),
    Input("season-selector", "value"),
)
def update_graph(selected_season):
    if selected_season == "Regular Season":
        filtered_df = scorers_df.query("season_avg_ppg >= 20")

        fig = px.scatter(
            filtered_df,
            x="season_avg_ppg",
            y="season_ts_percent",
            color="top5_candidates",
            color_discrete_map={
                "Top 5 MVP Candidate": "orange",
                "Other": "grey",
            },
            hover_name="player",
            hover_data=["team"],
        )

        fig.update_layout(legend_title_text="")

        return fig
    else:
        filtered_playoffs_df = scorers_df.query("playoffs_avg_ppg >= 20")

        fig = px.scatter(
            filtered_playoffs_df,
            x="playoffs_avg_ppg",
            y="playoffs_ts_percent",
            color="top5_candidates",
            color_discrete_map={
                "Top 5 MVP Candidate": "orange",
                "Other": "grey",
            },
            hover_name="player",
            hover_data=["team"],
        )

        fig.update_layout(legend_title_text="")

        return fig

    # # Create a bar chart with Plotly Express
    # fig = px.bar(
    #     game_types_df,
    #     x="game_type",
    #     y="n",
    #     text="explanation",  # Set text to display on hover (custom tooltip)
    #     labels={"n": "Count", "game_type": "Type"},  # Rename the y-axis label
    # )

    # # Customize the tooltip display
    # fig.update_traces(texttemplate="%{text}", textposition="outside")

    # return fig
