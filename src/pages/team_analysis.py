from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from src.data_cols.injuries import injuries_columns
from src.data_cols.transactions import transactions_columns
from src.data import (
    injuries_df,
    mov_df,
    player_stats_df,
    team_adv_stats_df,
    team_names,
    transactions_df,
)

team_analysis_layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="team-selector",
                        options=[{"label": team, "value": team} for team in team_names],
                        value=team_names[0],
                        clearable=False,
                    ),
                    className="kpi-card",
                ),
                html.Div(
                    id="kpi-boxes-1",
                    className="kpi-card",
                ),
                html.Div(
                    id="kpi-boxes-2",
                    className="kpi-card",
                ),
                html.Div(
                    id="kpi-boxes-3",
                    className="kpi-card",
                ),
            ],
            className="kpi-container",
            style={"display": "flex", "justify-content": "space-between"},
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Game Margin of Victory"),
                        dcc.Graph(
                            id="mov-plot",
                            config={"displayModeBar": False},
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H3("Player Scoring Efficiency"),
                        dcc.Graph(
                            id="team-player-efficiency-plot",
                            config={"displayModeBar": False},
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
                        html.H3("Team Injuries"),
                        html.Div(id="injuries-table"),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H3("Team Transactions"),
                        html.Div(id="transactions-table"),
                    ],
                    width=6,
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
        x="game_date",
        y="mov",
        labels={
            "game_date": "Date",
            "opponent": "Opponent",
            "mov": "Margin of Victory",
            "outcome": "Outcome",
        },
        color="outcome",
        color_discrete_map={
            "W": "green",
            "L": "red",
        },
        custom_data=[
            "game_date",
            "opponent",
            "mov",
            "outcome",
        ],
    )

    fig.update_traces(
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        hovertemplate="<b>%{customdata[0]}</b> vs <b>%{customdata[1]}</b><br>"
        "<b>Margin of Victory:</b> %{customdata[2]}<br>"
        "<b>Outcome:</b> %{customdata[3]}<br>",
    )

    return fig


@callback(
    Output("team-player-efficiency-plot", "figure"), Input("team-selector", "value")
)
def update_team_player_efficiency(selected_team):
    team_player_efficiency = player_stats_df.query(f"full_team == '{selected_team}'")

    fig = px.scatter(
        team_player_efficiency,
        x="avg_ppg",
        y="avg_ts_percent",
        color="is_mvp_candidate",
        text="player",
        labels={"avg_ppg": "Average PPG", "avg_ts_percent": "Average TS%"},
        custom_data=[
            "player",
            "avg_ppg",
            "avg_ts_percent",
            "is_mvp_candidate",
        ],
    )

    fig.update_layout(legend_title_text="", yaxis_tickformat=".0%")

    fig.update_traces(
        textposition="top center",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        hovertemplate="<b>%{customdata[0]}</b><br>"
        "<b>Average PPG:</b> %{customdata[1]}<br>"
        "<b>Average TS%:</b> %{customdata[2]:.1%}<br>"
        "<b>Type:</b> %{customdata[3]}<br>",
    )

    return fig


@callback(Output("injuries-table", "children"), Input("team-selector", "value"))
def update_injuries(selected_team):
    filtered_injuries = injuries_df.query(f"team == '{selected_team}'")

    return (
        dash_table.DataTable(
            columns=injuries_columns,
            data=filtered_injuries.to_dict("records"),
            css=[
                {
                    "selector": ".dash-table-tooltip",
                    "rule": "background-color: grey; font-family: font-family: 'Gill Sans',\
                        'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; color: white",
                }
            ],
            sort_action="native",
            page_size=10,
            style_cell={
                "overflow": "hidden",
                "textOverflow": "ellipsis",
                "maxWidth": 0,
                "background-color": "#15171a",
            },
            tooltip_data=[
                {
                    column: {"value": str(value), "type": "markdown"}
                    for column, value in row.items()
                }
                for row in filtered_injuries.to_dict("records")
            ],
            tooltip_duration=None,
            style_cell_conditional=[
                {"if": {"column_id": "player"}, "width": "15%"},
                {"if": {"column_id": "team"}, "width": "15%"},
                {"if": {"column_id": "date"}, "width": "15%"},
                {"if": {"column_id": "status"}, "width": "10%"},
                {"if": {"column_id": "injury"}, "width": "10%"},
                {"if": {"column_id": "description"}, "width": "50%"},
            ],
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
            css=[
                {
                    "selector": ".dash-table-tooltip",
                    "rule": "background-color: grey; font-family: font-family: 'Gill Sans',\
                    'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; color: white",
                }
            ],
            sort_action="native",
            page_size=10,
            style_cell={
                "overflow": "hidden",
                "textOverflow": "ellipsis",
                "maxWidth": 0,
                "background-color": "#15171a",
            },
            tooltip_data=[
                {
                    column: {"value": str(value), "type": "markdown"}
                    for column, value in row.items()
                }
                for row in filtered_transactions.to_dict("records")
            ],
            tooltip_duration=None,
            style_cell_conditional=[
                {"if": {"column_id": "date"}, "width": "20%"},
                {"if": {"column_id": "transaction"}, "width": "80%"},
            ],
        ),
    )


# Define callback to update KPI boxes
@callback(Output("kpi-boxes-1", "children"), [Input("team-selector", "value")])
def update_kpi_boxes_1(selected_team):
    kpi_values = team_adv_stats_df.query(f"team == '{selected_team}'")

    kpi_box_content = [
        html.Div("Team Ratings", style={"fontSize": 24}),
        html.Div(f"Net Rating: {kpi_values['nrtg'].iloc[0]}"),
        html.Div(f"Offensive Rating: {kpi_values['ortg'].iloc[0]}"),
        html.Div(f"Defensive Rating: {kpi_values['drtg'].iloc[0]}"),
    ]

    return kpi_box_content


@callback(Output("kpi-boxes-2", "children"), [Input("team-selector", "value")])
def update_kpi_boxes_2(selected_team):
    kpi_values = team_adv_stats_df.query(f"team == '{selected_team}'")

    kpi_box_content = [
        html.Div("Advanced Stats", style={"fontSize": 24}),
        html.Div(f"SRS: {kpi_values['srs'].iloc[0]}"),
        html.Div(f"Pace: {kpi_values['pace'].iloc[0]}"),
        html.Div(f"TS %: {kpi_values['ts_percent'].iloc[0]:.1%}"),
    ]

    return kpi_box_content


@callback(Output("kpi-boxes-3", "children"), [Input("team-selector", "value")])
def update_kpi_boxes_3(selected_team):
    kpi_values = team_adv_stats_df.query(f"team == '{selected_team}'")

    kpi_box_content = [
        html.Div("Opponent Stats", style={"fontSize": 24}),
        html.Div(f"TOV %: {kpi_values['tov_percent_opp'].iloc[0]}%"),
        html.Div(f"eFG %: {kpi_values['efg_percent_opp'].iloc[0]:.1%}"),
    ]

    return kpi_box_content
