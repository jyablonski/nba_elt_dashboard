from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from src.data_cols.future_schedule import future_schedule_columns
from src.data_cols.tonights_schedule import tonights_schedule_columns
from src.data import (
    game_types_df,
    past_schedule_analysis_df,
    preseason_odds_df,
    schedule_df,
    schedule_tonights_games_df,
    team_blown_leads_df,
)

past_schedule_analysis_df = past_schedule_analysis_df.sort_values(
    by="pct_vs_below_500", ascending=True
)

preseason_odds_df = preseason_odds_df.sort_values(
    by="wins_differential", ascending=True
)

team_blown_leads_df = team_blown_leads_df.query(
    "season_type == 'Regular Season'"
).sort_values(by="net_comebacks", ascending=True)


schedule_layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        "Moneyline Odds for tonight's games provided by ",
                        html.A(
                            html.Img(src="../assets/draftkings.png", height="60px"),
                            href="https://www.draftkings.com",
                        ),
                    ]
                )
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Upcoming Games", style={"text-align": "left"}),
                        dcc.Dropdown(
                            id="schedule-table-selector",
                            options=[
                                {"label": "Tonight's Games", "value": "tonights-games"},
                                {
                                    "label": "Full Schedule",
                                    "value": "full-schedule",
                                },
                            ],
                            value="tonights-games",
                            clearable=False,
                        ),
                    ],
                    width=3,
                ),
            ]
        ),
        dbc.Row(
            [
                html.Br(),
                dbc.Col(
                    id="schedule-table",
                    width=12,
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id="schedule-plot-selector",
                            options=[
                                {
                                    "label": "Stength of Schedule (as of Today)",
                                    "value": "strength-of-schedule",
                                },
                                {
                                    "label": "Vegas Preseason Over / Under Odds",
                                    "value": "vegas-preseason-odds",
                                },
                                {
                                    "label": "Team Comebacks Analysis (Regular Season)",
                                    "value": "team-comebacks",
                                },
                            ],
                            value="strength-of-schedule",
                            clearable=False,
                        ),
                        width={"size": 3, "offset": 9},
                    ),
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("League Average Margins of Victory"),
                                dcc.Graph(
                                    id="game-types-plot",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                html.H3("Team Schedule Analysis"),
                                dcc.Graph(
                                    id="schedule-plot",
                                ),
                            ],
                            width=6,
                        ),
                    ]
                ),
            ]
        ),
    ],
    className="custom-padding",
)


@callback(
    Output("schedule-table", "children"), [Input("schedule-table-selector", "value")]
)
def update_schedule_table(selected_value):
    if selected_value == "tonights-games":
        return (
            dash_table.DataTable(
                columns=tonights_schedule_columns,
                data=schedule_tonights_games_df.to_dict("records"),
                css=[{"selector": ".show-hide", "rule": "display: none"}],
                sort_action="native",
                page_size=15,
                merge_duplicate_headers=True,
                style_cell={"background-color": "#383b3d"},
                style_data_conditional=[
                    {
                        "if": {
                            "filter_query": "{home_is_great_value} = 1",
                            "column_id": "home_team_odds",
                        },
                        "backgroundColor": "green",
                    },
                    {
                        "if": {
                            "filter_query": "{away_is_great_value} = 1",
                            "column_id": "away_team_odds",
                        },
                        "backgroundColor": "green",
                    },
                ],
            ),
        )
    elif selected_value == "full-schedule":
        return (
            dash_table.DataTable(
                columns=future_schedule_columns,
                data=schedule_df.to_dict("records"),
                css=[{"selector": ".show-hide", "rule": "display: none"}],
                sort_action="native",
                page_size=15,
                style_cell={"background-color": "#383b3d"},
            ),
        )


@callback(Output("game-types-plot", "figure"), Input("game-types-plot", "hoverData"))
def update_game_types_plot(hoverData):
    fig = px.bar(
        game_types_df,
        x="game_type",
        y="n",
        text="n",
        labels={"n": "Count", "game_type": "Type", "explanation": "Explanation"},
        custom_data=[
            "game_type",
            "n",
            "explanation",
        ],
    )

    fig.update_traces(
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        hovertemplate="<b>Game Type:</b> %{customdata[0]}<br>"
        "<b># Games:</b> %{customdata[1]}<br>"
        "<b>Explanation:</b> %{customdata[0]}s are defined as"
        "the Margin of Victory being %{customdata[2]}<br>",
    )

    return fig


@callback(
    Output("schedule-plot", "figure"),
    Input("schedule-plot-selector", "value"),
)
def update_schedule_plot(selected_schedule_plot):
    if selected_schedule_plot == "strength-of-schedule":
        fig = px.bar(
            past_schedule_analysis_df,
            x="pct_vs_below_500",
            y="team",
            labels={"team": "Team", "pct_vs_below_500": "% Games Below .500 Teams"},
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

        fig.update_layout(legend_title_text="", xaxis_tickformat=".0%")

        fig.update_traces(
            hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
            hovertemplate="<b>%{customdata[0]}</b><br>"
            "<b>Record:</b> %{customdata[9]}<br>"
            "<b>Win %:</b> %{customdata[1]:.1%}<br>"
            "<b>AVG Win % Opp.:</b> %{customdata[2]:.1%}<br>"
            "<b>Home Record:</b> %{customdata[3]}<br>"
            "<b>Road Record:</b> %{customdata[4]}<br>"
            "<b>Record vs Above .500 Teams:</b> %{customdata[5]}<br>"
            "<b>Record vs Below .500 Teams:</b> %{customdata[6]}<br>"
            "<b>% Games vs Above .500 Teams:</b> %{customdata[7]:.1%}<br>"
            "<b>% Games vs Below .500 Teams:</b> %{customdata[8]:.1%}",
        )
        return fig

    elif selected_schedule_plot == "vegas-preseason-odds":
        fig = px.bar(
            preseason_odds_df,
            x="wins_differential",
            y="team",
            text="wins_differential",
            color="wins_differential",
            color_continuous_scale="RdYlGn",
            labels={"team": "Team", "wins_differential": "Wins Differential"},
            custom_data=[
                "team",
                "wins_differential",
                "predicted_stats",
                "projected_stats",
                "over_under",
                "championship_odds",
            ],
        )

        fig.update_traces(
            hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
            hovertemplate="<b>%{customdata[0]}</b><br>"
            "<b>Wins Differential:</b> %{customdata[1]}<br>"
            "<b>Preseason Over / Under:</b> %{customdata[2]}<br>"
            "<b>Projected Stats:</b> %{customdata[3]}<br>"
            "<b>Status:</b> %{customdata[4]}<br>"
            "<b>Championship Odds:</b> %{customdata[5]}<br>",
        )
        return fig

    else:
        fig = px.bar(
            team_blown_leads_df,
            x="net_comebacks",
            y="team",
            text="team",
            color="net_comebacks",
            color_continuous_scale="RdYlGn",
            labels={"team": "Team", "net_comebacks": "Net Comebacks"},
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

        fig.update_traces(
            hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
            hovertemplate="<b>%{customdata[0]}</b><br>"
            "<b>10+ Pt Blown Leads:</b> %{customdata[1]} (%{customdata[2]})<br>"
            "<b>10+ Pt Comebacks:</b> %{customdata[3]} (%{customdata[4]})<br>"
            "<b>Net Comebacks:</b> %{customdata[5]} (%{customdata[6]})<br>",
        )
        return fig
