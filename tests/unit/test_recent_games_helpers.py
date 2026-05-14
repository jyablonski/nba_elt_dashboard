import pandas as pd

from src.recent_games_helpers import build_game_card_specs, pbp_flow_stats


def test_pbp_flow_stats_basic():
    df = pd.DataFrame(
        {
            "time_remaining_final": [48.0, 47.0, 46.0],
            "margin_score": [0, 5, -3],
        }
    )
    st = pbp_flow_stats(df)
    assert st["plays"] == 3
    assert st["max_lead"] == 5


def test_build_game_card_specs_minimal():
    pbp = pd.DataFrame(
        {
            "game_description": ["A vs B"],
            "home_team": ["H"],
            "away_team": ["V"],
            "score_home": [100],
            "score_away": [90],
            "winning_team": ["H"],
            "home_team_full": ["Home Full"],
            "away_team_full": ["Away Full"],
        }
    )
    teams = pd.DataFrame()
    specs = build_game_card_specs(pbp, teams)
    assert len(specs) == 1
    assert specs[0].home_pts == 100
    assert specs[0].away_pts == 90
