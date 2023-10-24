from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from src.data_cols.injuries import injuries_columns
from src.data_cols.transactions import transactions_columns
from src.data import (
    injuries_df,
    mov_df,
    scorers_df,
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
                        style={"width": "250px"},
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
                        html.Div(id="injuries-table"),
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.H1("Team Transactions"),
                        html.Div(id="transactions-table"),
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
    filtered_df = mov_df.query(f"full_team == '{selected_team}'")

    fig = px.bar(
        filtered_df,
        x="date",
        y="mov",
        text="team",
        color="outcome",
        labels={"date": "Date", "mov": "Margin of Victory"},
    )

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

    return fig


@callback(Output("injuries-table", "children"), Input("team-selector", "value"))
def update_injuries(selected_team):
    filtered_injuries = injuries_df.query(f"team == '{selected_team}'")

    return (
        dash_table.DataTable(
            columns=injuries_columns,
            data=filtered_injuries.to_dict("records"),
            css=[{"selector": ".show-hide", "rule": "display: none"}],
        ),
    )


@callback(Output("transactions-table", "children"), Input("team-selector", "value"))
def update_transactions(selected_team):
    filtered_transactions = transactions_df.query(
        f'transaction.str.contains("{selected_team}")', engine="python"
    )
    return (
        dash_table.DataTable(
            columns=transactions_columns,
            data=filtered_transactions.to_dict("records"),
            css=[{"selector": ".show-hide", "rule": "display: none"}],
        ),
    )
