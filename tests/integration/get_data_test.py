from src.database import get_data, generate_data
from src.data import source_tables


def test_generate_data(postgres_engine):
    generate_data(postgres_engine=postgres_engine, source_tables=source_tables)

    for table in source_tables:
        assert len(f"{table}_df") > 0


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


def test_get_data_no_schema(postgres_conn):
    df = get_data(
        table_name="nba_prod.reddit_comments", schema=None, conn=postgres_conn
    )

    assert list(df.columns) == [
        "scrape_date",
        "author",
        "comment",
        "flair",
        "score",
        "url",
        "compound",
        "pos",
        "neu",
        "neg",
    ]
    assert len(df) == 30
