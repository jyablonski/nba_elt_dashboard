from dash import dash_table, dcc, html

from src.data_cols.standings import standings_columns
from src.data import standings_df

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
                dash_table.DataTable(
                    id="ml-predictions-table",
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
