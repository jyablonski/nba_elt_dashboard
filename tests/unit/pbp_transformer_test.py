import pandas as pd

from src.utils import pbp_transformer


def test_pbp_transformer(pbp_fixture):
    pbp_plot_kpis, pbp_plot_df = pbp_transformer(df=pbp_fixture)

    assert len(pbp_plot_kpis) == 1
    assert pbp_plot_kpis.columns.tolist() == [
        "game_description",
        "DEN",
        "MIA",
        "TIE",
        "home_team",
        "away_team",
        "home_pct_leading",
        "away_pct_leading",
        "tie_pct",
    ]
    assert pbp_plot_kpis.loc[0, "home_pct_leading"] == 0.352
    assert pbp_plot_kpis.loc[0, "away_pct_leading"] == 0.582
    assert pbp_plot_kpis.loc[0, "tie_pct"] == 0.066

    assert len(pbp_plot_df) == 99
    assert pbp_plot_df.columns.tolist() == [
        "time_quarter",
        "play",
        "time_remaining_final",
        "quarter",
        "away_score",
        "score",
        "home_score",
        "home_team",
        "away_team",
        "score_away",
        "score_home",
        "margin_score",
        "date",
        "leading_team",
        "home_team_full",
        "home_primary_color",
        "away_team_full",
        "away_primary_color",
        "game_description",
        "away_fill",
        "home_fill",
        "scoring_team_color",
        "scoring_team",
        "max_home_lead",
        "max_away_lead",
        "winning_team",
        "losing_team",
        "leading_team_text",
        "prev_time",
        "time_difference",
        "game_plot_team_text",
    ]


def test_pbp_transformer_empty_df():
    empty = pd.DataFrame()
    k, d = pbp_transformer(empty)
    assert k.empty and d.empty


def _minimal_pbp(times: list[float], scorers: list[str]) -> pd.DataFrame:
    n = len(times)
    return pd.DataFrame(
        {
            "game_description": ["G"] * n,
            "time_remaining_final": times,
            "scoring_team": scorers,
            "leading_team": scorers,
            "home_team": ["DEN"] * n,
            "away_team": ["MIA"] * n,
            "home_fill": ["DEN"] * n,
            "away_fill": ["MIA"] * n,
            "time_quarter": ["x"] * n,
            "quarter": ["q"] * n,
        }
    )


def test_pbp_transformer_end_row_at_zero_for_regulation():
    # Last play is in regulation (positive clock) -> 0:00 marker sits at end of Q4 (0.0).
    _, plot = pbp_transformer(_minimal_pbp([48.0, 1.0], ["DEN", "MIA"]))
    end = plot[plot["time_quarter"] == "0:00"]
    assert end["time_remaining_final"].tolist() == [0.0]


def test_pbp_transformer_end_row_at_period_boundary_for_overtime():
    # Clock counts past 0 into OT (OT1: 0 -> -5). The 0:00 marker must land at the OT
    # period boundary, not back at end of regulation (the bug that drew a stray point).
    _, plot_ot1 = pbp_transformer(_minimal_pbp([48.0, -0.5, -4.9], ["DEN", "MIA", "DEN"]))
    assert plot_ot1[plot_ot1["time_quarter"] == "0:00"]["time_remaining_final"].tolist() == [-5.0]

    # Second overtime (-5 -> -10) lands on -10.0.
    _, plot_ot2 = pbp_transformer(_minimal_pbp([48.0, -6.0, -9.5], ["DEN", "MIA", "DEN"]))
    assert plot_ot2[plot_ot2["time_quarter"] == "0:00"]["time_remaining_final"].tolist() == [-10.0]


def test_pbp_transformer_adds_tie_column_when_absent_from_pivot(pbp_fixture):
    sub = pbp_fixture[pbp_fixture["leading_team_text"] != "TIE"].copy()
    kpis, _ = pbp_transformer(sub)
    assert "TIE" in kpis.columns


def test_pbp_transformer_lead_pct_uses_game_teams_not_hardcoded_finals(pbp_fixture):
    sub = pbp_fixture.replace(
        {
            "DEN": "SAS",
            "MIA": "OKC",
            "Denver Nuggets Vs. Miami Heat": "San Antonio Spurs Vs. Oklahoma City Thunder",
        }
    )

    kpis, _ = pbp_transformer(sub)

    assert "SAS" in kpis.columns
    assert "OKC" in kpis.columns
    assert kpis.loc[0, "home_team"] == "SAS"
    assert kpis.loc[0, "away_team"] == "OKC"
    assert kpis.loc[0, "home_pct_leading"] == 0.352
    assert kpis.loc[0, "away_pct_leading"] == 0.582
