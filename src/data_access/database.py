from __future__ import annotations

import os
from datetime import datetime
from typing import Any

import pandas as pd
import yaml
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection, Engine

_engine: Engine | None = None


def substitute_env_vars(yaml_content: dict[str, Any]) -> None:
    for key, value in yaml_content.items():
        if isinstance(value, str):
            yaml_content[key] = os.path.expandvars(value)
        elif isinstance(value, dict):
            substitute_env_vars(value)


def load_yaml_with_env(filename: str) -> dict[str, Any]:
    with open(filename) as file:
        yaml_content = yaml.safe_load(file)
        substitute_env_vars(yaml_content)
        return yaml_content


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


def create_dashboard_engine(
    config_path: str = "config.yaml",
    env_type: str | None = None,
) -> Engine:
    env = load_yaml_with_env(config_path)[env_type or os.environ.get("ENV_TYPE", "dev")]
    return sql_connection(
        user=env["user"],
        password=env["pass"],
        host=env["host"],
        database=env["database"],
        schema=env["schema"],
        port=coerce_engine_port(env["port"]),
    )


def get_dashboard_engine() -> Engine:
    global _engine

    if _engine is None:
        _engine = create_dashboard_engine()
    return _engine


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
