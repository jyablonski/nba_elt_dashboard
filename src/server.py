from datetime import datetime
import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from src.pages.about import about_layout
from src.pages.overview import overview_layout
from src.pages.recent_games import recent_games_layout
from src.pages.schedule import schedule_layout
from src.pages.social_media_analysis import social_media_analysis_layout
from src.pages.team_analysis import team_analysis_layout

print(f"whole app is loading boi")
# Initialize the Dash app
app = dash.Dash(
    __name__, assets_folder="../static", external_stylesheets=[dbc.themes.COSMO]
)
app.title = "NBA Dashboard"

app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            value="overview",
            children=[
                dcc.Tab(label="Overview", value="overview", children=overview_layout),
                dcc.Tab(
                    label="Recent Games",
                    value="recent-games",
                    children=recent_games_layout,
                ),
                dcc.Tab(
                    label="Team Analysis",
                    value="team-analysis",
                    children=team_analysis_layout,
                ),
                dcc.Tab(label="Schedule", value="schedule", children=schedule_layout),
                dcc.Tab(
                    label="Social Media Analysis",
                    value="social-media-analysis",
                    children=social_media_analysis_layout,
                ),
                dcc.Tab(label="About", value="about", children=about_layout),
            ],
        ),
        html.Div(id="tab-content"),
    ]
)


@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "tab-1":
        return html.Div(
            [
                html.H1("Welcome to Tab 1"),
                html.P("This is the content of Tab 1."),
            ]
        )
    elif tab == "tab-2":
        return html.Div(
            [
                html.H1("Welcome to Tab 2"),
                html.P("This is the content of Tab 2."),
            ]
        )
    elif tab == "tab-3":
        return html.Div(
            [
                html.H1("Welcome to Tab 3"),
                html.P("This is the content of Tab 3."),
            ]
        )


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=9000)
