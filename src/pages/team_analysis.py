from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from src.data_cols.injuries import injuries_columns
from src.data_cols.standings import standings_columns
from src.data_cols.transactions import transactions_columns
from src.data import (
    injuries_df,
    mov_df,
    scorers_df,
    standings_df,
    team_adv_stats_df,
    team_names,
    transactions_df,
)

team_analysis_layout = html.Div(
    [
        # Single div to contain all four KPIs
        html.Div(
            [
                # KPI 1
                html.Div(
                    dcc.Dropdown(
                        id="team-selector",
                        options=[{"label": team, "value": team} for team in team_names],
                        value=team_names[0],
                        clearable=False,
                        style={"width": "250px"},  # Set the width to 300 pixels
                    ),
                ),
                # KPI 2
                html.Div(
                    [
                        html.Div("KPI 2 Value", style={"fontSize": 24}),
                        html.Div("KPI 2 Description"),
                    ],
                    className="kpi-box",
                ),
                # KPI 3
                html.Div(
                    [
                        html.Div("KPI 3 Value", style={"fontSize": 24}),
                        html.Div("KPI 3 Description"),
                    ],
                    className="kpi-box",
                ),
                # KPI 4
                html.Div(
                    [
                        html.Div("KPI 4 Value", style={"fontSize": 24}),
                        html.Div("KPI 4 Description"),
                    ],
                    className="kpi-box",
                ),
            ],
            className="kpi-container",
            style={"display": "flex", "justify-content": "space-between"},
        ),
        html.Div(
            [
                dcc.Graph(
                    id="mov-plot",
                    config={"displayModeBar": False},
                    style={"width": "50%", "display": "inline-block"},
                ),
                dcc.Graph(
                    id="team-player-efficiency-plot",
                    config={"displayModeBar": False},
                    style={"width": "50%", "display": "inline-block"},
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Team Injuries"),
                        dash_table.DataTable(
                            id="team-injuries-table",
                            columns=standings_columns,
                            data=standings_df.query('conference == "Western"').to_dict(
                                "records"
                            ),
                            hidden_columns=[
                                "active_protocols",
                                "conference",
                                "team",
                            ],
                            css=[{"selector": ".show-hide", "rule": "display: none"}],
                        ),
                    ],
                    style={
                        "width": "49%",
                        "display": "inline-block",
                        "margin-right": "30px",
                    },
                ),
                html.Div(
                    [
                        html.H1("Team Transactions"),
                        dash_table.DataTable(
                            id="team-transactions-table",
                            columns=standings_columns,
                            data=standings_df.query('conference == "Eastern"').to_dict(
                                "records"
                            ),
                            hidden_columns=[
                                "active_protocols",
                                "conference",
                                "team",
                            ],
                            css=[{"selector": ".show-hide", "rule": "display: none"}],
                        ),
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
            ]
        ),
    ],
    className="custom-padding",
)


@callback(Output("mov-plot", "figure"), Input("team-selector", "value"))
def update_mov(selected_team):
    # filtered_df = mov_df[mov_df["full_team"] == selected_team]
    filtered_df = mov_df.query(f"full_team == '{selected_team}'")

    fig = px.bar(
        filtered_df,
        x="date",
        y="mov",
        text="team",
        color="outcome",
        labels={"date": "Date", "mov": "Margin of Victory"},
    )

    # Customize the tooltip display
    fig.update_traces(texttemplate="%{text}", textposition="outside")

    return fig


@callback(
    Output("team-player-efficiency-plot", "figure"), Input("team-selector", "value")
)
def update_team_player_efficiency(selected_team):
    team_player_efficiency = scorers_df.query(f"full_team == '{selected_team}'")

    fig = px.scatter(
        team_player_efficiency,
        x="season_avg_ppg",
        y="season_ts_percent",
        color="top5_candidates",
        text="player",
        labels={"season_avg_ppg": "Season Avg PPG", "season_ts_percent": "Season TS%"},
    )

    # Customize the tooltip display
    # fig.update_traces(texttemplate="%{text}", textposition="outside")

    return fig
