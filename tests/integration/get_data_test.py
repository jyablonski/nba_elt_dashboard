import pandas as pd
import pytest

from src.data_access import cache as database_module
from src.data_access.tables import source_tables
from src.data_access.cache import generate_data
from src.data_access.database import get_data


@pytest.fixture(autouse=True)
def restore_dashboard_snapshot():
    snapshot_before_test = {
        table_name: df.copy() for table_name, df in database_module._data_snapshot.items()
    }
    metadata_before_test = database_module.get_snapshot_metadata()

    yield

    database_module._data_snapshot = snapshot_before_test
    database_module._snapshot_metadata = metadata_before_test


def _table_key(table: str) -> str:
    if "." in table:
        return table.split(".")[1]
    return table


def test_generate_data(postgres_engine):
    generate_data(postgres_engine=postgres_engine, source_tables=source_tables)

    for table in source_tables:
        assert len(database_module.get_table(_table_key(table))) > 0

    standings = database_module.get_table("standings")
    assert len(standings) > 0
    assert database_module.get_snapshot_metadata()["row_counts"]["standings"] == len(standings)


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
        assert len(database_module.get_table("bans")) == 1
    finally:
        monkeypatch.undo()
        generate_data(postgres_engine=postgres_engine, source_tables=["bans"])
    assert "scrape_time" in database_module.get_table("bans").columns


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


def test_refresh_data_failed_load_keeps_previous_snapshot(monkeypatch):
    class FakeEngine:
        def begin(self):
            return self

        def __enter__(self):
            return object()

        def __exit__(self, exc_type, exc, tb):
            return False

    def successful_get_data(table_name, conn, limit_amount=2000, schema=None):
        return pd.DataFrame({"table": [table_name], "limit": [limit_amount]})

    monkeypatch.setattr(database_module, "get_data", successful_get_data)
    database_module.refresh_data(postgres_engine=FakeEngine(), tables=["standings"])
    before = database_module.get_table("standings")

    def failing_get_data(table_name, conn, limit_amount=2000, schema=None):
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(database_module, "get_data", failing_get_data)
    with pytest.raises(RuntimeError, match="database unavailable"):
        database_module.refresh_data(postgres_engine=FakeEngine(), tables=["standings"])

    after = database_module.get_table("standings")
    pd.testing.assert_frame_equal(before, after)
