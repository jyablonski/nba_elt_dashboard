from dash import callback, dash_table, dcc, html
import dash_bootstrap_components as dbc
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

contract_value_analysis_df2 = contract_value_analysis_df.copy()
# contract_value_analysis_df = contract_value_analysis_df.sort_values(
#     by="salary", ascending=True
# )
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
                        className="kpi-card",
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
                        f"Last Updated {(bans_df['scrape_time'][0]).strftime('%A, %B %d %-I:%M %p UTC')}"
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
                                style_cell={"background-color": "#15171a"},
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
                                style_cell={"background-color": "#15171a"},
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
                    width={"size": 3},  # Set the width to 50% (6 out of 12 columns)
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="player-scoring-efficiency-plot"),
                        width=6,
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id="team-ratings-plot",
                            figure=px.scatter(
                                team_ratings_df,
                                x="ortg",
                                y="drtg",
                                text="team",
                                labels={
                                    "ortg": "Offensive Rating (ORTG)",
                                    "drtg": "Defensive Rating (DRTG)",
                                },
                                hover_name="team",
                            ),
                        ),
                        width=6,
                    ),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="player-value-analysis-plot",
                            figure=px.scatter(
                                contract_value_analysis_df,
                                x="salary",
                                y="player_mvp_calc_avg",
                                labels={
                                    "salary": "Salary",
                                    "player_mvp_calc_avg": "Average MVP Score",
                                },
                                custom_data=[
                                    "player",
                                    "team",
                                    "player_mvp_calc_avg",
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
                            ).update_traces(
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
                            ),
                        ),
                        width={"size": 6},
                    ),
                    dbc.Col(
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
                            ).update_traces(
                                hoverlabel=dict(
                                    bgcolor="white",
                                    font_size=12,
                                    font_family="Rockwell",
                                ),
                                hovertemplate="<b>%{customdata[0]}</b><br>"
                                "<b>Win %:</b> %{customdata[1]:.1%}<br>"
                                "<b>% Salary Value Earned:</b> %{customdata[4]:.1%}<br>"
                                "<b>% Salary Value Lost from Injury:</b> %{customdata[6]:.1%}<br>"
                                "<b>Total Salary Value Earned:</b> %{customdata[2]:$,}<br>"
                                "<b>Total Salary Value Lost from Injury:</b> %{customdata[5]:$,}",
                            ),
                        ),
                        width={"size": 6},
                    ),
                ],
            ),
        ],
        className="custom-padding",
    ),
)

# avg_ortg = team_ratings_df["ortg"].mean()
# avg_drtg = team_ratings_df["drtg"].mean()

# average_ortg_line = go.Scatter(
#     x=[avg_ortg, avg_ortg],
#     y=[team_ratings_df["drtg"].min(), team_ratings_df["drtg"].max()],
#     mode="lines",
#     name="Average ORTG",
#     line=dict(color="red", dash="dash"),
# )

# average_drtg_line = go.Scatter(
#     x=[team_ratings_df["ortg"].min(), team_ratings_df["ortg"].max()],
#     y=[avg_drtg, avg_drtg],
#     mode="lines",
#     name="Average DRTG",
#     line=dict(color="blue", dash="dash"),
# )

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
            labels={
                "season_avg_ppg": "Average PPG",
                "season_ts_percent": "Average TS%",
            },
            color="top5_candidates",
            color_discrete_map={
                "Top 5 MVP Candidate": "orange",
                "Other": "grey",
            },
            custom_data=[
                "player",
                "team",
                "season_avg_ppg",
                "season_ts_percent",
                "top5_candidates",
            ],
        )

        fig.update_layout(legend_title_text="")

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
            hover_data=["team", "playoffs_ts_percent"],
        )

        fig.update_layout(legend_title_text="")

        return fig
