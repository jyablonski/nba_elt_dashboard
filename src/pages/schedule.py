from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output

from src.data_cols.ml_predictions import ml_predictions_columns
from src.data_cols.schedule import schedule_columns
from src.data import tonights_games_ml_df, schedule_df

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
                # Dropdown for selecting the data table
                dcc.Dropdown(
                    id="schedule-table-selector",
                    options=[
                        {"label": "Tonight's Games", "value": "tonights-games"},
                        {"label": "Future Schedule", "value": "future-schedule"},
                    ],
                    value="tonights-games",  # Default selection
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
                dcc.Graph(
                    id="game-types-plot",
                    config={
                        "displayModeBar": False
                    },  # Optional: Hide the plotly toolbar
                    style={"width": "50%", "display": "inline-block"},
                ),
                dcc.Graph(
                    id="schedule-picker-plot",
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
