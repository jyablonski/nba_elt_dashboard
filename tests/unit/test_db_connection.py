from sqlalchemy.engine import make_url

from src.db_connection import coerce_engine_port, sql_connection


def test_coerce_engine_port_string_and_int():
    assert coerce_engine_port("5432") == 5432
    assert coerce_engine_port(5432) == 5432


def test_sql_connection_url_contains_components():
    eng = sql_connection(
        user="nba_dashboard_user",
        password="postgres",
        host="127.0.0.1",
        database="postgres",
        schema="gold",
        port=5433,
    )
    u = make_url(str(eng.url))
    assert u.username == "nba_dashboard_user"
    assert u.host == "127.0.0.1"
    assert u.port == 5433
    assert u.database == "postgres"
