import dash
import dash_bootstrap_components as dbc

# from dash.dependencies import Input, Output
from dash import dcc, html

# import plotly.express as px

from src.pages.about import about_layout
from src.pages.overview import (
    average_drtg_line,
    average_ortg_line,
    overview_layout,
    team_logos,
)
from src.pages.recent_games import recent_games_layout
from src.pages.schedule import schedule_layout
from src.pages.social_media_analysis import social_media_analysis_layout
from src.pages.team_analysis import team_analysis_layout


print("whole app is loading boi")
app = dash.Dash(
    __name__,
    assets_folder="../static",
    external_stylesheets=[dbc.themes.COSMO],
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

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=9000)
