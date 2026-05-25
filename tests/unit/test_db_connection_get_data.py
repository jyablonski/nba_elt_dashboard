from unittest.mock import MagicMock

import pandas as pd

from src.data_access.database import get_data


def test_get_data_with_schema_qualifies_table_and_limit(monkeypatch):
    captured: list[str] = []

    def fake_read_sql(sql, con):
        captured.append(sql)
        return pd.DataFrame()

    monkeypatch.setattr("src.data_access.database.pd.read_sql_query", fake_read_sql)
    conn = MagicMock()
    get_data(table_name="bans", schema="gold", conn=conn, limit_amount=42)
    sql = captured[0].lower().replace("\n", " ")
    assert "gold.bans" in sql
    assert "limit 42" in sql


def test_get_data_without_schema_uses_table_name_verbatim(monkeypatch):
    captured: list[str] = []

    def fake_read_sql(sql, con):
        captured.append(sql)
        return pd.DataFrame()

    monkeypatch.setattr("src.data_access.database.pd.read_sql_query", fake_read_sql)
    conn = MagicMock()
    get_data(table_name="gold.reddit_comments", schema=None, conn=conn)
    sql = captured[0].lower().replace("\n", " ")
    assert "from gold.reddit_comments" in sql
    assert "limit 2000" in sql
