from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from src.data_cols.game_types import game_types_columns
from src.data_cols.ml_predictions import ml_predictions_columns
from src.data_cols.schedule import schedule_columns
from src.data import (
    game_types_df,
    past_schedule_analysis_df,
    preseason_odds_df,
    schedule_df,
    team_blown_leads_df,
    tonights_games_ml_df,
)

past_schedule_analysis_df = past_schedule_analysis_df.sort_values(
    by="pct_vs_below_500", ascending=True
)

preseason_odds_df = preseason_odds_df.sort_values(
    by="wins_differential", ascending=True
)

team_blown_leads_df = team_blown_leads_df.query(
    f"season_type == 'Regular Season'"
).sort_values(by="net_comebacks", ascending=True)


schedule_layout = html.Div(
    [
        "Moneyline Odds for tonight's games provided by ",
        html.A(
            html.Img(src="../assets/draftkings.png", height="60px"),
            href="https://www.draftkings.com",
        ),
        html.Div(
            [
                html.H1("Upcoming Games"),
                dcc.Dropdown(
                    id="schedule-table-selector",
                    options=[
                        {"label": "Tonight's Games", "value": "tonights-games"},
                        {"label": "Future Schedule", "value": "future-schedule"},
                    ],
                    value="tonights-games",
                    clearable=False,
                ),
                html.Div(id="schedule-table"),
            ],
            style={
                "width": "98%",
                "display": "inline-block",
            },
        ),
        html.Div(
            [
                html.Div(
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
                        style={"width": "250px"},
                    ),
                ),
                dcc.Graph(
                    id="game-types-plot",
                    config={
                        "displayModeBar": False
                    },  # Optional: Hide the plotly toolbar
                    style={"width": "50%", "display": "inline-block"},
                ),
                dcc.Graph(
                    id="schedule-plot",
                    config={
                        "displayModeBar": False
                    },  # Optional: Hide the plotly toolbar
                    style={"width": "50%", "display": "inline-block"},
                ),
            ]
        ),
    ],
    className="custom-padding",
)


# Define a callback to update the selected data table
@callback(
    Output("schedule-table", "children"), [Input("schedule-table-selector", "value")]
)
def update_data_table(selected_value):
    if selected_value == "tonights-games":
        return (
            dash_table.DataTable(
                columns=ml_predictions_columns,
                data=tonights_games_ml_df.to_dict("records"),
                # hidden_columns=[
                #     "active_protocols",
                #     "conference",
                #     "team",
                # ],
                css=[{"selector": ".show-hide", "rule": "display: none"}],
            ),
        )
    elif selected_value == "future-schedule":
        return (
            dash_table.DataTable(
                columns=schedule_columns,
                data=schedule_df.to_dict("records"),
                # hidden_columns=[
                #     "active_protocols",
                #     "conference",
                #     "team",
                # ],
                css=[{"selector": ".show-hide", "rule": "display: none"}],
            ),
        )


@callback(Output("game-types-plot", "figure"), Input("game-types-plot", "hoverData"))
def update_game_types(hoverData):
    fig = px.bar(
        game_types_df,
        x="game_type",
        y="n",
        text="explanation",
        labels={"n": "Count", "game_type": "Type"},
    )

    # Customize the tooltip display
    fig.update_traces(texttemplate="%{text}", textposition="outside")

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
            text="team",
        )

        # Customize the tooltip display
        fig.update_traces(texttemplate="%{text}", textposition="outside")

        return fig
    elif selected_schedule_plot == "vegas-preseason-odds":
        fig = px.bar(
            preseason_odds_df,
            x="wins_differential",
            y="team",
            text="team",
            color="wins_differential",
            color_discrete_map={True: "lightblue", False: "red"},
        )

        # Customize the tooltip display
        fig.update_traces(texttemplate="%{text}", textposition="outside")

        return fig
    else:
        fig = px.bar(
            team_blown_leads_df,
            x="net_comebacks",
            y="team",
            text="team",
            color="net_comebacks",
            color_discrete_map={True: "lightblue", False: "red"},
        )

        # Customize the tooltip display
        fig.update_traces(texttemplate="%{text}", textposition="outside")

        return fig
