import pandas as pd


def test_sql_connection(postgres_conn):
    df = pd.read_sql_query(
        sql="select count(*) from marts.recent_games_teams;", con=postgres_conn
    )

    assert isinstance(df, pd.DataFrame)
    assert df["count"][0] == 14
