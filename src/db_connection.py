from __future__ import annotations

from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection, Engine


def coerce_engine_port(port: object) -> int:
    """Normalize DB port from config (YAML may supply a string or numeric type)."""
    return int(port)


def sql_connection(
    user: str, password: str, host: str, database: str, schema: str, port: int
) -> Engine:
    connection = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",
        connect_args={"options": f"-csearch_path={schema}"},
        echo=False,
    )
    print(f"SQL Engine created for {schema} at {datetime.now()}")
    return connection


def get_data(
    table_name: str,
    conn: Connection,
    limit_amount: int = 2000,
    schema: str | None = None,
) -> pd.DataFrame:
    if schema is None:
        df = pd.read_sql_query(
            sql=f"""
            select *
            from {table_name}
            limit {limit_amount};""",
            con=conn,
        )
    else:
        df = pd.read_sql_query(
            sql=f"""
                select *
                from {schema}.{table_name}
                limit {limit_amount};""",
            con=conn,
        )

    print(f"Grabbed {len(df)} Rows from {table_name} at {datetime.now()}")
    return df
