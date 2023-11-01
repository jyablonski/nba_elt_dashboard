from src.utils import pbp_transformer


def test_pbp_transformer(pbp_fixture):
    pbp_plot_kpis, pbp_plot_df = pbp_transformer(df=pbp_fixture)

    assert len(pbp_plot_kpis) == 2
    assert pbp_plot_kpis.columns.tolist() == [
        "scoring_team",
        "Leading",
        "TIE",
        "pct_leading",
    ]

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
