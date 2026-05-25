from datetime import datetime, timezone
from unittest import mock

import dash_bootstrap_components as dbc
import pandas as pd

import src.server as srv
from src.data_access.cache import RefreshResult


def test_dash_app_title_and_layout():
    assert srv.app.title == srv.APP_TITLE == "NBA Dashboard"
    assert srv.app.layout is not None
    tabs = srv._tabs()
    assert isinstance(tabs, dbc.Tabs)
    assert tabs.id == "tabs"

    layout_dump = str(srv.serve_layout().to_plotly_json())
    assert "app-navbar" not in layout_dump
    assert "app-brand" not in layout_dump
    assert "app-season-pill" not in layout_dump


def test_recent_games_count_returns_none_without_game_description_column():
    with mock.patch.object(srv, "get_table", return_value=pd.DataFrame({"x": [1]})):
        assert srv._recent_games_count() is None
    with mock.patch.object(srv, "get_table", return_value=None):
        assert srv._recent_games_count() is None


def test_schedule_tonight_count_returns_none_when_missing_or_empty():
    with mock.patch.object(srv, "get_table", return_value=None):
        assert srv._schedule_tonight_count() is None
    with mock.patch.object(srv, "get_table", return_value=pd.DataFrame()):
        assert srv._schedule_tonight_count() is None


def test_refresh_data_endpoint_requires_configured_token(monkeypatch):
    monkeypatch.delenv("DATA_REFRESH_TOKEN", raising=False)
    response = srv.app.server.test_client().post("/internal/refresh-data")

    assert response.status_code == 500
    assert response.get_json() == {"error": "DATA_REFRESH_TOKEN is not configured"}


def test_refresh_data_endpoint_rejects_bad_token(monkeypatch):
    monkeypatch.setenv("DATA_REFRESH_TOKEN", "secret")
    with mock.patch.object(srv, "refresh_dashboard_data") as refresh_mock:
        response = srv.app.server.test_client().post(
            "/internal/refresh-data",
            headers={"X-Refresh-Token": "wrong"},
        )

    assert response.status_code == 401
    assert response.get_json() == {"error": "unauthorized"}
    refresh_mock.assert_not_called()


def test_refresh_data_endpoint_refreshes_with_valid_token(monkeypatch):
    monkeypatch.setenv("DATA_REFRESH_TOKEN", "secret")
    result = RefreshResult(
        refreshed_at=datetime(2026, 5, 25, 12, 0, tzinfo=timezone.utc),
        duration_seconds=1.25,
        row_counts={"standings": 30},
    )
    with mock.patch.object(srv, "refresh_dashboard_data", return_value=result) as refresh_mock:
        response = srv.app.server.test_client().post(
            "/internal/refresh-data",
            headers={"X-Refresh-Token": "secret"},
        )

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "refreshed_at": "2026-05-25T12:00:00+00:00",
        "duration_seconds": 1.25,
        "row_counts": {"standings": 30},
    }
    refresh_mock.assert_called_once_with()
