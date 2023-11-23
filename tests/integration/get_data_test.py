from src.database import get_data


def test_get_data(postgres_conn):
    df = get_data(table_name="schedule", schema="nba_prod", conn=postgres_conn)
    df_limit = get_data(
        table_name="schedule", schema="nba_prod", conn=postgres_conn, limit_amount=1
    )

    assert list(df.columns) == [
        "game_date",
        "day_name",
        "game_ts",
        "avg_team_rank",
        "start_time",
        "home_team",
        "away_team",
        "home_moneyline_raw",
        "away_moneyline_raw",
        "home_team_logo",
        "away_team_logo",
        "home_team_odds",
        "away_team_odds",
    ]
    assert len(df) == 30
    assert len(df_limit) == 1
