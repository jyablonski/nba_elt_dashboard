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


def test_build_game_card_specs_empty_pbp():
    assert build_game_card_specs(None, pd.DataFrame()) == []
    assert build_game_card_specs(pd.DataFrame(), pd.DataFrame()) == []


def test_build_game_card_specs_winner_from_scores_when_no_winner():
    pbp = pd.DataFrame(
        {
            "game_description": ["G1", "G1"],
            "home_team": ["H", "H"],
            "away_team": ["V", "V"],
            "score_home": [100, 100],
            "score_away": [90, 90],
            "winning_team": [float("nan"), float("nan")],
        }
    )
    specs = build_game_card_specs(pbp, pd.DataFrame())
    assert specs[0].winner_abbr == "H"


def test_build_game_card_specs_tie_score_uses_away_as_winner_abbr_when_no_winner():
    pbp = pd.DataFrame(
        {
            "game_description": ["G1", "G1"],
            "home_team": ["H", "H"],
            "away_team": ["V", "V"],
            "score_home": [90, 90],
            "score_away": [90, 90],
            "winning_team": [float("nan"), float("nan")],
        }
    )
    specs = build_game_card_specs(pbp, pd.DataFrame())
    assert specs[0].winner_abbr == "V"
    pbp = pd.DataFrame(
        {
            "game_description": ["G1"],
            "home_team": ["H"],
            "away_team": ["V"],
            "score_home": [10],
            "score_away": [8],
            "winning_team": ["H"],
        }
    )
    teams = pd.DataFrame(
        [
            {
                "team": "V",
                "opponent": "H",
                "mov": 2,
                "home_team": "V",
                "team_logo": "logos/v.png",
                "opp_logo": "logos/h.png",
            }
        ]
    )
    specs = build_game_card_specs(pbp, teams)
    assert specs[0].away_logo == "logos/v.png"
    assert specs[0].home_logo == "logos/h.png"
    assert specs[0].margin == 2


def test_build_game_card_specs_carries_series_fields():
    pbp = pd.DataFrame(
        {
            "game_description": ["G1"],
            "home_team": ["H"],
            "away_team": ["V"],
            "score_home": [110],
            "score_away": [104],
            "winning_team": ["H"],
        }
    )
    teams = pd.DataFrame(
        [
            {
                "team": "H",
                "opponent": "V",
                "mov": 6,
                "home_team": "H",
                "team_logo": "logos/h.png",
                "opp_logo": "logos/v.png",
                "series_round": "NBA Finals",
                "series_status": "H leads 2-0",
                "series_game_number": 2.0,
            }
        ]
    )
    spec = build_game_card_specs(pbp, teams)[0]
    assert spec.series_round == "NBA Finals"
    assert spec.series_status == "H leads 2-0"
    assert spec.series_game_number == 2  # coerced to int


def test_build_game_card_specs_series_fields_default_none_without_columns():
    pbp = pd.DataFrame(
        {
            "game_description": ["G1"],
            "home_team": ["H"],
            "away_team": ["V"],
            "score_home": [100],
            "score_away": [90],
            "winning_team": ["H"],
        }
    )
    teams = pd.DataFrame(
        [
            {
                "team": "H",
                "opponent": "V",
                "mov": 10,
                "home_team": "H",
                "team_logo": "logos/h.png",
                "opp_logo": "logos/v.png",
            }
        ]
    )
    spec = build_game_card_specs(pbp, teams)[0]
    assert spec.series_round is None
    assert spec.series_status is None
    assert spec.series_game_number is None


def test_teams_row_no_match_falls_back_to_score_margin():
    pbp = pd.DataFrame(
        {
            "game_description": ["G1"],
            "home_team": ["H"],
            "away_team": ["V"],
            "score_home": [100],
            "score_away": [88],
            "winning_team": ["H"],
        }
    )
    teams = pd.DataFrame(
        [
            {
                "team": "X",
                "opponent": "Y",
                "mov": 99,
                "home_team": "X",
                "team_logo": "a",
                "opp_logo": "b",
            }
        ]
    )
    specs = build_game_card_specs(pbp, teams)
    assert specs[0].margin == 12


def test_pbp_flow_stats_empty_paths():
    assert pbp_flow_stats(None)["plays"] == "-"
    assert pbp_flow_stats(pd.DataFrame())["plays"] == "-"
    bad = pd.DataFrame({"time_remaining_final": [1.0]})
    assert pbp_flow_stats(bad)["plays"] == "-"
