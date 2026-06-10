from unittest.mock import patch

import pandas as pd

from src.pages import overview


def _fake_contract_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "player": ["A", "B", "C", "D"],
            "team": ["DEN", "DEN", "LAL", "BOS"],
            "salary": [1_000_000, 5_000_000, 30_000_000, 12_000_000],
            "avg_mvp_score": [5.0, 12.0, 40.0, 22.0],
            "color_var": ["Bad Value", "Normal", "Superstars", "Great Value"],
            "games_played": [50, 60, 70, 65],
            "games_missed": [20, 10, 5, 7],
        }
    )


def _npoints(fig) -> int:
    return sum(len(trace.x) for trace in fig.data)


def test_player_value_team_options_lists_all_teams_then_sorted_teams():
    with patch.object(overview, "get_table", return_value=_fake_contract_df()):
        opts = overview._player_value_team_options()
    assert opts[0] == {"label": "All Teams", "value": "All Teams"}
    assert [o["value"] for o in opts[1:]] == ["BOS", "DEN", "LAL"]  # sorted, de-duped


def test_player_value_chart_unfiltered_shows_every_player():
    with patch.object(overview, "get_table", return_value=_fake_contract_df()):
        fig = overview.create_player_value_analysis_chart()
        fig_all = overview.create_player_value_analysis_chart(team="All Teams")
    assert _npoints(fig) == 4
    assert _npoints(fig_all) == 4


def test_player_value_chart_filters_to_one_team():
    with patch.object(overview, "get_table", return_value=_fake_contract_df()):
        fig = overview.create_player_value_analysis_chart(team="DEN")
    assert _npoints(fig) == 2  # only the two DEN players
