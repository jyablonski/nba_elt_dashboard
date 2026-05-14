import pandas as pd
import pytest

from src import database as database_module
from src.data import source_tables
from src.database import generate_data
from src.db_connection import get_data


def _df_attr_name(table: str) -> str:
    if "." in table:
        return f"{table.split('.')[1]}_df"
    return f"{table}_df"


def test_generate_data(postgres_engine):
    generate_data(postgres_engine=postgres_engine, source_tables=source_tables)

    for table in source_tables:
        attr = _df_attr_name(table)
        assert len(getattr(database_module, attr)) > 0


def test_get_data(postgres_conn):
    df = get_data(table_name="schedule", schema="gold", conn=postgres_conn)
    df_limit = get_data(table_name="schedule", schema="gold", conn=postgres_conn, limit_amount=1)

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


def test_generate_data_splits_qualified_table_name(postgres_engine, monkeypatch):
    def fake_get_data(table_name, conn, limit_amount=2000, schema=None):
        assert table_name == "gold.bans"
        return pd.DataFrame({"ok": [1]})

    monkeypatch.setattr(database_module, "get_data", fake_get_data)
    try:
        generate_data(postgres_engine=postgres_engine, source_tables=["gold.bans"])
        assert len(database_module.bans_df) == 1
    finally:
        monkeypatch.undo()
        generate_data(postgres_engine=postgres_engine, source_tables=["bans"])
    assert "scrape_time" in database_module.bans_df.columns


@pytest.mark.parametrize("table", ("mov", "reddit_sentiment_time_series"))
def test_generate_data_special_tables_use_high_limit(postgres_engine, monkeypatch, table):
    real = database_module.get_data
    captured: dict[str, int] = {}

    def wrap(table_name, conn, limit_amount=2000, schema=None):
        captured[table_name] = limit_amount
        return real(table_name=table_name, conn=conn, limit_amount=limit_amount, schema=schema)

    monkeypatch.setattr(database_module, "get_data", wrap)
    generate_data(postgres_engine=postgres_engine, source_tables=[table])
    assert captured[table] == 10_000_000


def test_get_data_no_schema(postgres_conn):
    df = get_data(table_name="gold.reddit_comments", schema=None, conn=postgres_conn)

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
