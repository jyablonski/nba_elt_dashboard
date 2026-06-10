import pandas as pd

from src.recent_games_helpers import (
    biggest_scoring_run,
    build_game_card_specs,
    pbp_flow_stats,
)


def _run_events(rows):
    """Build a minimal scoring-event frame: (time_remaining, score_home, score_away)."""
    return pd.DataFrame(
        {
            "time_remaining_final": [r[0] for r in rows],
            "score_home": [r[1] for r in rows],
            "score_away": [r[2] for r in rows],
            "home_team": "DEN",
            "away_team": "MIA",
            "winning_team": "DEN",
            "home_primary_color": "#4d90cd",
            "away_primary_color": "#98002e",
            "quarter": "1st Quarter",
            "time_quarter": "0:00",
        }
    )


def test_biggest_scoring_run_finds_winner_burst():
    # DEN (home) scores 12 unanswered, then MIA gets 2 -> 12-2 run.
    rows = [(48.0, 0, 0)]
    rows += [(47.0 - k, 3 * (k + 1), 0) for k in range(4)]  # DEN 12-0
    rows += [(42.0, 12, 2)]  # MIA answers
    df = _run_events(rows)
    run = biggest_scoring_run(df, min_net=8)
    assert run is not None
    assert run["qualified"] is True
    assert run["winner"] == "DEN"
    assert run["win_pts"] == 12
    assert run["los_pts"] in (0, 2)
    assert run["label"] == f"{run['win_pts']}-{run['los_pts']}"


def test_biggest_scoring_run_ratio_cap_avoids_choppy_stretch():
    # Build a choppy lead-the-whole-way stretch (DEN nets +11 but opponent keeps
    # answering, share ~0.5) preceded by a clean 12-2 burst. The choppy window has
    # the higher raw net, so only the ratio cap steers us to the clean run.
    rows = [(48.0, 0, 0)]
    # clean 12-2 burst
    rows += [(47.0, 3, 0), (46.5, 6, 0), (46.0, 9, 0), (45.5, 12, 0), (45.0, 12, 2)]
    # choppy trade: DEN and MIA alternate 3s, DEN stays ~one basket ahead
    sh, sa, t = 12, 2, 44.5
    for _ in range(8):
        sh += 3
        rows.append((t, sh, sa))
        t -= 0.3
        sa += 3
        rows.append((t, sh, sa))
        t -= 0.3
    df = _run_events(rows)
    run = biggest_scoring_run(df, min_net=8, max_loser_ratio=0.40)
    assert run is not None
    assert run["los_pts"] <= 0.40 * run["win_pts"]
    assert run["qualified"] is True


def test_biggest_scoring_run_always_returns_when_no_clean_run():
    # Tight defensive trades: nothing clears min_net=8, but a run is still forced.
    rows = [(48.0 - 0.5 * k, 2 * (k // 2 + (k % 2)), 2 * ((k + 1) // 2)) for k in range(12)]
    df = _run_events(rows)
    run = biggest_scoring_run(df, min_net=8)
    assert run is not None
    assert run["qualified"] is False
    assert run["win_pts"] >= run["los_pts"]  # still the winner's best stretch


def test_biggest_scoring_run_handles_overtime():
    # In OT the clock continues past 0 into negative time_remaining_final. A run
    # there (or spanning Q4 -> OT) must still sort chronologically, measure a
    # positive span, and land its band in the OT region (negative x).
    rows = [(0.5, 100, 100)]  # tie at end of regulation
    rows += [(-0.5, 103, 100), (-1.5, 106, 100), (-2.5, 109, 100), (-3.5, 112, 100)]
    df = _run_events(rows)
    df["quarter"] = ["4th Quarter"] + ["1st Overtime"] * 4
    run = biggest_scoring_run(df)
    assert run is not None
    assert run["label"] == "12-0"
    assert run["x_start"] < 0 and run["x_end"] < 0  # band sits in OT
    assert run["x_start"] > run["x_end"]  # ordered start (earlier) -> end (later)
    assert run["x_start"] - run["x_end"] > 0  # positive span across the OT clock


def test_biggest_scoring_run_on_real_fixture(pbp_fixture):
    run = biggest_scoring_run(pbp_fixture)
    assert run is not None
    assert run["winner"] == "DEN"
    assert run["win_pts"] - run["los_pts"] >= 8
    assert run["win_pts"] <= 30 and run["los_pts"] <= 30
    assert run["los_pts"] <= 0.40 * run["win_pts"]


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
