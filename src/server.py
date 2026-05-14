import os

import dash
import dash_bootstrap_components as dbc
from dash import html

from src.pages.about import about_layout
from src.pages.overview import overview_layout

# from src.pages.player_analysis import player_analysis_layout
from src.pages.recent_games import recent_games_layout
from src.pages.schedule import schedule_layout
from src.pages.social_media_analysis import social_media_analysis_layout
from src.pages.team_analysis import team_analysis_layout

# Import pages first so `src.database` finishes loading globals used below.
from src.database import pbp_df, schedule_tonights_games_df
from src.shell import tab_label_with_badge

APP_TITLE = "NBA Dashboard"


def _recent_games_count() -> int | None:
    if pbp_df is None or pbp_df.empty or "game_description" not in pbp_df.columns:
        return None
    return int(pbp_df["game_description"].drop_duplicates().shape[0])


def _schedule_tonight_count() -> int | None:
    if schedule_tonights_games_df is None or schedule_tonights_games_df.empty:
        return None
    return int(len(schedule_tonights_games_df))


_RECENT_GAMES_TAB_COUNT = _recent_games_count()
_SCHEDULE_TAB_COUNT = _schedule_tonight_count()


app = dash.Dash(
    __name__,
    assets_folder="../static",
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600"
        "&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap",
        dbc.themes.SLATE,
    ],
    title=APP_TITLE,
)

_tabs = dbc.Tabs(
    id="tabs",
    className="justify-content-center border-0",
    children=[
        dbc.Tab(
            label="Overview",
            tab_id="overview",
            children=overview_layout,
            tabClassName="text-center",
            labelClassName="nba-tab-label",
        ),
        dbc.Tab(
            label=tab_label_with_badge("Recent Games", _RECENT_GAMES_TAB_COUNT),
            tab_id="recent-games",
            children=recent_games_layout,
            tabClassName="text-center",
            labelClassName="nba-tab-label",
        ),
        dbc.Tab(
            label="Team Analysis",
            tab_id="team-analysis",
            children=team_analysis_layout,
            tabClassName="text-center",
            labelClassName="nba-tab-label",
        ),
        dbc.Tab(
            label=tab_label_with_badge("Schedule", _SCHEDULE_TAB_COUNT),
            tab_id="schedule",
            children=schedule_layout,
            tabClassName="text-center",
            labelClassName="nba-tab-label",
        ),
        dbc.Tab(
            label="Social Media Analysis",
            tab_id="social-media-analysis",
            children=social_media_analysis_layout,
            tabClassName="text-center",
            labelClassName="nba-tab-label",
        ),
        dbc.Tab(
            label="About",
            tab_id="about",
            children=about_layout,
            tabClassName="text-center",
            labelClassName="nba-tab-label",
        ),
    ],
)

app.layout = dbc.Container(
    fluid=True,
    className="app-shell px-0",
    children=[
        dbc.Row(
            dbc.Col(
                html.Div(_tabs, className="nba-shell-tabs"),
                width=12,
                className="px-0 pt-3 pb-2",
            ),
            className="mx-0 g-0",
        ),
    ],
)

if __name__ == "__main__":
    # Local dev: DASH_RELOAD=1 enables Flask's stat reloader (bind-mounted src/ edits).
    # Do not set Dash debug=True here: on Python 3.12+ Dash calls pkgutil.find_loader (removed),
    # and Dash hot_reload uses the same path. Flask use_reloader alone is enough for .py changes.
    _reload = os.environ.get("DASH_RELOAD", "").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=9000, debug=False, use_reloader=_reload)
