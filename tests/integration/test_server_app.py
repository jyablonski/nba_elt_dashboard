from unittest import mock

import dash_bootstrap_components as dbc
import pandas as pd


def test_dash_app_title_and_layout():
    import src.server as server

    assert server.app.title == server.APP_TITLE == "NBA Dashboard"
    assert server.app.layout is not None
    tabs = server._tabs
    assert isinstance(tabs, dbc.Tabs)
    assert tabs.id == "tabs"

    layout_dump = str(server.app.layout.to_plotly_json())
    assert "app-navbar" not in layout_dump
    assert "app-brand" not in layout_dump
    assert "app-season-pill" not in layout_dump


def test_recent_games_count_returns_none_without_game_description_column():
    import src.server as srv

    with mock.patch.object(srv, "pbp_df", pd.DataFrame({"x": [1]})):
        assert srv._recent_games_count() is None
    with mock.patch.object(srv, "pbp_df", None):
        assert srv._recent_games_count() is None


def test_schedule_tonight_count_returns_none_when_missing_or_empty():
    import src.server as srv

    with mock.patch.object(srv, "schedule_tonights_games_df", None):
        assert srv._schedule_tonight_count() is None
    with mock.patch.object(srv, "schedule_tonights_games_df", pd.DataFrame()):
        assert srv._schedule_tonight_count() is None
