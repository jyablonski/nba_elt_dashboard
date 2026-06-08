from datetime import datetime, timezone
from unittest import mock

import dash_bootstrap_components as dbc
import pandas as pd
from dash import html

import src.routes as routes
import src.server as srv
from src.data_access.cache import RefreshResult


def test_dash_app_title_and_layout():
    assert srv.app.title == srv.APP_TITLE == "NBA Dashboard"
    assert srv.app.layout is not None

    with (
        mock.patch.object(srv, "overview_layout", return_value=html.Div()),
        mock.patch.object(srv, "recent_games_layout", return_value=html.Div()),
        mock.patch.object(srv, "team_analysis_layout", return_value=html.Div()),
        mock.patch.object(srv, "schedule_layout", return_value=html.Div()),
        mock.patch.object(srv, "social_media_analysis_layout", return_value=html.Div()),
        mock.patch.object(srv, "_recent_games_count", return_value=None),
        mock.patch.object(srv, "_schedule_tonight_count", return_value=None),
        mock.patch.object(srv, "has_snapshot", return_value=True),
    ):
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
    with mock.patch.object(routes, "refresh_dashboard_data") as refresh_mock:
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
    with mock.patch.object(routes, "refresh_dashboard_data", return_value=result) as refresh_mock:
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


def test_health_endpoint_requires_configured_token(monkeypatch):
    monkeypatch.delenv("DATA_REFRESH_TOKEN", raising=False)
    response = srv.app.server.test_client().get("/internal/health")

    assert response.status_code == 500
    assert response.get_json() == {"error": "DATA_REFRESH_TOKEN is not configured"}


def test_health_endpoint_rejects_bad_token(monkeypatch):
    monkeypatch.setenv("DATA_REFRESH_TOKEN", "secret")
    response = srv.app.server.test_client().get(
        "/internal/health",
        headers={"X-Refresh-Token": "wrong"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"error": "unauthorized"}


def test_health_endpoint_returns_snapshot_metadata(monkeypatch):
    monkeypatch.setenv("DATA_REFRESH_TOKEN", "secret")
    metadata = {
        "last_refreshed_at": datetime(2026, 5, 25, 12, 0, tzinfo=timezone.utc),
        "duration_seconds": 1.25,
        "row_counts": {"standings": 30, "player_stats": 562},
    }

    with (
        mock.patch.object(routes, "has_snapshot", return_value=True),
        mock.patch.object(routes, "get_snapshot_metadata", return_value=metadata),
        mock.patch.object(
            routes,
            "_memory_metadata",
            return_value={
                "process_rss_mb": 355.4,
                "container_current_mb": 362.1,
                "container_limit_mb": 31979.5,
            },
        ),
    ):
        response = srv.app.server.test_client().get(
            "/internal/health",
            headers={"X-Refresh-Token": "secret"},
        )

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "has_snapshot": True,
        "last_refreshed_at": "2026-05-25T12:00:00+00:00",
        "duration_seconds": 1.25,
        "row_counts": {"standings": 30, "player_stats": 562},
        "memory": {
            "process_rss_mb": 355.4,
            "container_current_mb": 362.1,
            "container_limit_mb": 31979.5,
        },
    }


def test_health_endpoint_reports_unavailable_without_snapshot(monkeypatch):
    monkeypatch.setenv("DATA_REFRESH_TOKEN", "secret")
    metadata = {
        "last_refreshed_at": None,
        "duration_seconds": None,
        "row_counts": {},
    }

    with (
        mock.patch.object(routes, "has_snapshot", return_value=False),
        mock.patch.object(routes, "get_snapshot_metadata", return_value=metadata),
        mock.patch.object(
            routes,
            "_memory_metadata",
            return_value={
                "process_rss_mb": None,
                "container_current_mb": None,
                "container_limit_mb": None,
            },
        ),
    ):
        response = srv.app.server.test_client().get(
            "/internal/health",
            headers={"X-Refresh-Token": "secret"},
        )

    assert response.status_code == 503
    assert response.get_json() == {
        "status": "unavailable",
        "has_snapshot": False,
        "last_refreshed_at": None,
        "duration_seconds": None,
        "row_counts": {},
        "memory": {
            "process_rss_mb": None,
            "container_current_mb": None,
            "container_limit_mb": None,
        },
    }


def test_memory_metadata_reads_process_and_cgroup_values(monkeypatch, tmp_path):
    proc_statm = tmp_path / "statm"
    memory_current = tmp_path / "memory.current"
    memory_max = tmp_path / "memory.max"
    proc_statm.write_text("100 256 0 0 0 0 0")
    memory_current.write_text(str(128 * 1024 * 1024))
    memory_max.write_text(str(512 * 1024 * 1024))

    monkeypatch.setattr(routes, "PROC_STATM_PATH", proc_statm)
    monkeypatch.setattr(routes, "CGROUP_V2_MEMORY_CURRENT_PATH", memory_current)
    monkeypatch.setattr(routes, "CGROUP_V2_MEMORY_MAX_PATH", memory_max)
    monkeypatch.setattr(routes.os, "sysconf", lambda _name: 4096)

    assert routes._memory_metadata() == {
        "process_rss_mb": 1.0,
        "container_current_mb": 128.0,
        "container_limit_mb": 512.0,
    }


def test_memory_metadata_handles_missing_files(monkeypatch, tmp_path):
    missing = tmp_path / "missing"

    monkeypatch.setattr(routes, "PROC_STATM_PATH", missing)
    monkeypatch.setattr(routes, "CGROUP_V2_MEMORY_CURRENT_PATH", missing)
    monkeypatch.setattr(routes, "CGROUP_V2_MEMORY_MAX_PATH", missing)
    monkeypatch.setattr(routes, "CGROUP_V1_MEMORY_CURRENT_PATH", missing)
    monkeypatch.setattr(routes, "CGROUP_V1_MEMORY_LIMIT_PATH", missing)

    assert routes._memory_metadata() == {
        "process_rss_mb": None,
        "container_current_mb": None,
        "container_limit_mb": None,
    }
