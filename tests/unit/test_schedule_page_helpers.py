"""Unit tests for schedule page helpers and tonight's card builder."""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd

from src.pages import schedule as schedule_mod


def test_truthy_great_value_cases():
    assert schedule_mod._truthy_great_value(1) is True
    assert schedule_mod._truthy_great_value(1.0) is True
    assert schedule_mod._truthy_great_value(0) is False
    assert schedule_mod._truthy_great_value(None) is False
    assert schedule_mod._truthy_great_value("no") is False


def test_fmt_game_date():
    assert "Mar" in schedule_mod._fmt_game_date(pd.Timestamp("2024-03-14"))
    assert schedule_mod._fmt_game_date(None) == "-"
    assert schedule_mod._fmt_game_date(float("nan")) == "-"


def test_fmt_pct():
    assert schedule_mod._fmt_pct(0.876) == "87.6%"
    assert schedule_mod._fmt_pct(None) == "-"


def test_fmt_rank():
    assert schedule_mod._fmt_rank(3) == "3"
    assert schedule_mod._fmt_rank(9.5) == "9.5"
    assert schedule_mod._fmt_rank(None) == "-"


def test_clean_text_cases():
    assert schedule_mod._clean_text("NBA Finals") == "NBA Finals"
    assert schedule_mod._clean_text(3.0) == "3"  # whole float -> int
    assert schedule_mod._clean_text(3) == "3"
    assert schedule_mod._clean_text(None) == ""
    assert schedule_mod._clean_text(float("nan")) == ""


def test_series_line_shown_when_playoffs_active():
    line = schedule_mod._series_line("NBA Finals", 3, "Series tied 1-1", playoffs_active=True)
    flat = str(line)
    assert "NBA Finals" in flat
    assert "Game 3" in flat
    assert "Series tied 1-1" in flat
    assert "schedule-card-series" in flat


def test_series_line_hidden_when_flag_off_even_with_data():
    assert (
        schedule_mod._series_line("NBA Finals", 3, "Series tied 1-1", playoffs_active=False) == ""
    )


def test_series_line_hidden_when_no_series_data():
    assert schedule_mod._series_line(None, None, None, playoffs_active=True) == ""


def test_create_tonight_games_cards_series_gated_by_flag():
    row = {
        "home_team": "Atlanta Hawks",
        "away_team": "New York Knicks",
        "avg_team_rank": 10,
        "home_team_odds": "Atlanta Hawks (-125)",
        "away_team_odds": "New York Knicks (+105)",
        "start_time": "7:30 PM",
        "game_date": pd.Timestamp("2024-05-20"),
        "home_moneyline": -125.0,
        "away_moneyline": 105.0,
        "home_team_predicted_win_pct": 0.531,
        "away_team_predicted_win_pct": 0.469,
        "home_is_great_value": 0,
        "away_is_great_value": 0,
        "series_round": "NBA Finals",
        "series_status": "Series tied 1-1",
        "series_game_number": 3,
    }
    df = pd.DataFrame([row])

    with patch.object(schedule_mod, "get_table", return_value=df):
        with patch.object(schedule_mod, "playoffs_enabled", return_value=True):
            shown = str(schedule_mod.create_tonight_games_cards())
        with patch.object(schedule_mod, "playoffs_enabled", return_value=False):
            hidden = str(schedule_mod.create_tonight_games_cards())

    assert "schedule-card-series" in shown
    assert "Series tied 1-1" in shown
    assert "schedule-card-series" not in hidden
    assert "Series tied 1-1" not in hidden


def test_create_tonight_games_cards_empty_slate():
    empty = pd.DataFrame(
        columns=[
            "home_team",
            "away_team",
            "avg_team_rank",
            "home_team_odds",
            "away_team_odds",
            "start_time",
            "game_date",
            "home_moneyline",
            "away_moneyline",
            "home_team_predicted_win_pct",
            "away_team_predicted_win_pct",
            "home_is_great_value",
            "away_is_great_value",
        ]
    )
    with patch.object(schedule_mod, "get_table", return_value=empty):
        out = schedule_mod.create_tonight_games_cards()
    assert "No games on the slate" in str(out)


def test_create_tonight_games_cards_value_highlight():
    row = {
        "home_team": "Charlotte Hornets",
        "away_team": "Detroit Pistons",
        "avg_team_rank": 3,
        "home_team_odds": "Charlotte Hornets (-170)",
        "away_team_odds": "Detroit Pistons (+140)",
        "start_time": "7:00 PM",
        "game_date": pd.Timestamp("2024-03-14"),
        "home_moneyline": -170.0,
        "away_moneyline": 140.0,
        "home_team_predicted_win_pct": 0.876,
        "away_team_predicted_win_pct": 0.124,
        "home_is_great_value": 0,
        "away_is_great_value": 1,
    }
    df = pd.DataFrame([row])
    with patch.object(schedule_mod, "get_table", return_value=df):
        out = schedule_mod.create_tonight_games_cards()
    flat = str(out)
    assert "Detroit Pistons" in flat
    assert "schedule-card-team--value" in flat
    assert "87.6%" in flat
    assert "schedule-tonight-grid" in flat
    assert "schedule-tonight-slate" in flat
    assert "schedule-tonight-slate-date" in flat
    assert flat.count("Mar 14") == 1


def test_create_tonight_games_cards_multi_day_repeats_date_on_cards():
    base = {
        "home_team": "Charlotte Hornets",
        "away_team": "Detroit Pistons",
        "avg_team_rank": 3,
        "home_team_odds": "Charlotte Hornets (-170)",
        "away_team_odds": "Detroit Pistons (+140)",
        "start_time": "7:00 PM",
        "home_moneyline": -170.0,
        "away_moneyline": 140.0,
        "home_team_predicted_win_pct": 0.876,
        "away_team_predicted_win_pct": 0.124,
        "home_is_great_value": 0,
        "away_is_great_value": 0,
    }
    df = pd.DataFrame(
        [
            {**base, "game_date": pd.Timestamp("2024-03-14")},
            {**base, "game_date": pd.Timestamp("2024-03-15"), "start_time": "8:00 PM"},
        ]
    )
    with patch.object(schedule_mod, "get_table", return_value=df):
        out = schedule_mod.create_tonight_games_cards()
    flat = str(out)
    assert "schedule-tonight-slate-date" not in flat
    assert flat.count("schedule-card-date") == 2
    assert "Mar 14" in flat and "Mar 15" in flat
