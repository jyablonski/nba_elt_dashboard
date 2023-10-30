import dash
import dash_bootstrap_components as dbc
from dash import html

from src.pages.about import about_layout
from src.pages.overview import (
    overview_layout,
)
from src.pages.recent_games import recent_games_layout
from src.pages.schedule import schedule_layout
from src.pages.social_media_analysis import social_media_analysis_layout
from src.pages.team_analysis import team_analysis_layout


app = dash.Dash(
    __name__,
    assets_folder="../static",
    external_stylesheets=[dbc.themes.SLATE],
    title="NBA Dashboard",
)

app.layout = html.Div(
    [
        dbc.Tabs(
            id="tabs",
            children=[
                dbc.Tab(
                    label="Overview",
                    tab_id="overview",
                    children=overview_layout,
                    tabClassName="flex-grow-1 text-center",
                ),
                dbc.Tab(
                    label="Recent Games",
                    tab_id="recent-games",
                    children=recent_games_layout,
                    tabClassName="flex-grow-1 text-center",
                ),
                dbc.Tab(
                    label="Team Analysis",
                    tab_id="team-analysis",
                    children=team_analysis_layout,
                    tabClassName="flex-grow-1 text-center",
                ),
                dbc.Tab(
                    label="Schedule",
                    tab_id="schedule",
                    children=schedule_layout,
                    tabClassName="flex-grow-1 text-center",
                ),
                dbc.Tab(
                    label="Social Media Analysis",
                    tab_id="social-media-analysis",
                    children=social_media_analysis_layout,
                    tabClassName="flex-grow-1 text-center",
                ),
                dbc.Tab(
                    label="About",
                    tab_id="about",
                    children=about_layout,
                    tabClassName="flex-grow-1 text-center",
                ),
            ],
        ),
        html.Div(id="tab-content"),
    ]
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
