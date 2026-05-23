"""Unit tests for Recent Games page UI helpers (slate bar, PBP insights)."""

from __future__ import annotations

from dash import html

from src.pages.recent_games import (
    _flow_legend_and_stats,
    _pbp_chart_subtitle,
    _pbp_stat_tile,
    _slate_date_label,
    _slate_summary_bar,
)


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


def test_flow_legend_and_stats_missing_game():
    legend, meta = _flow_legend_and_stats(None)
    assert legend == ""
    assert meta == {}

    legend2, meta2 = _flow_legend_and_stats("Not A Real Game Description Xyz")
    assert legend2 == ""
    assert meta2 == {}


def test_flow_legend_and_stats_known_game():
    legend, meta = _flow_legend_and_stats("Atlanta Hawks Vs. Brooklyn Nets")
    assert isinstance(legend, html.Div)
    flat = str(legend)
    assert "Brooklyn Nets @ Atlanta Hawks" in flat
    assert "ATL 147" in flat
    assert "BKN 145" in flat
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
    assert meta["winner"] == "ATL"
    assert meta["home_pct_leading"] != "-"
    assert meta["away_pct_leading"] != "-"
