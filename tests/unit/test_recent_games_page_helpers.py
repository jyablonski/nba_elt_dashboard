"""Unit tests for Recent Games page UI helpers (slate bar, PBP insights)."""

from __future__ import annotations

import pandas as pd
import pytest
from dash import html

import src.pages.recent_games as recent_games_page
from src.pages.recent_games import (
    _flow_legend_and_stats,
    _pbp_chart_subtitle,
    _pbp_stat_tile,
    _series_chip,
    _slate_date_label,
    _slate_summary_bar,
)


def _recent_games_teams_fixture() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "team": "DEN",
                "opponent": "MIA",
                "home_team": "DEN",
                "mov": 5,
                "team_logo": "logos/den.png",
                "opp_logo": "logos/mia.png",
            }
        ]
    )


@pytest.fixture(autouse=True)
def recent_games_tables(monkeypatch, pbp_fixture):
    tables = {
        "pbp": pbp_fixture,
        "recent_games_teams": _recent_games_teams_fixture(),
    }

    def fake_get_table(table_name: str) -> pd.DataFrame:
        return tables[table_name].copy()

    monkeypatch.setattr(recent_games_page, "get_table", fake_get_table)


def test_pbp_chart_subtitle_non_empty():
    s = _pbp_chart_subtitle()
    assert "play-by-play" in s.lower()
    assert len(s) > 10


def test_slate_date_label_format():
    label = _slate_date_label()
    assert len(label) >= 8
    # e.g. "Mon, Jan 01, 2024" from strftime
    assert "," in label


def test_slate_summary_bar_structure():
    bar = _slate_summary_bar()
    assert isinstance(bar, html.Div)
    flat = str(bar)
    assert "games on slate" in flat
    assert "plays in feed" in flat
    assert "recent-games-slate-bar" in flat


def test_pbp_stat_tile_renders():
    tile = _pbp_stat_tile("Lead changes", 49)
    assert isinstance(tile, html.Div)
    s = str(tile)
    assert "Lead changes" in s
    assert "49" in s
    assert "recent-games-pbp-stat-tile" in s


def test_series_chip_shown_when_playoffs_active():
    chip = _series_chip("NBA Finals", "MIA leads 2-0", playoffs_active=True)
    assert isinstance(chip, html.Div)
    flat = str(chip)
    assert "NBA Finals" in flat
    assert "MIA leads 2-0" in flat
    assert "recent-games-card-series" in flat


def test_series_chip_hidden_when_flag_off_even_with_data():
    # Authoritative gate: stale series data must not leak in the regular season.
    assert _series_chip("NBA Finals", "MIA leads 2-0", playoffs_active=False) == ""


def test_series_chip_hidden_when_no_series_status():
    assert _series_chip("NBA Finals", None, playoffs_active=True) == ""
    assert _series_chip(None, "", playoffs_active=True) == ""


def test_series_chip_status_only_no_round():
    chip = _series_chip(None, "MIA leads 2-0", playoffs_active=True)
    assert chip.children == "MIA leads 2-0"


def test_flow_legend_and_stats_missing_game():
    legend, meta = _flow_legend_and_stats(None)
    assert legend == ""
    assert meta == {}

    legend2, meta2 = _flow_legend_and_stats("Not A Real Game Description Xyz")
    assert legend2 == ""
    assert meta2 == {}


def test_flow_legend_and_stats_known_game():
    legend, meta = _flow_legend_and_stats("Denver Nuggets Vs. Miami Heat")
    assert isinstance(legend, html.Div)
    flat = str(legend)
    assert "Miami Heat @ Denver Nuggets" in flat
    assert "DEN 94" in flat
    assert "MIA 89" in flat
    assert "Final" in flat
    assert "(BKN @ ATL)" not in flat
    assert "Chart context" not in flat
    assert "Max lead" in flat
    assert "Led" in flat
    assert "of game" in flat
    assert "ties (" not in flat
    assert "recent-games-pbp-heading" in flat
    assert "plays" in meta
    assert meta["plays"] != "-"
    assert meta["winner"] == "DEN"
    assert meta["home_pct_leading"] != "-"
    assert meta["away_pct_leading"] != "-"
