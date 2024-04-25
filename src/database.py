from datetime import datetime
import os
import yaml

import pandas as pd
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy import create_engine

from src.data import source_tables


# pyyaml is fucking useless lmfao, how does this not come w/ the package ??????
def substitute_env_vars(yaml_content: dict) -> None:
    for key, value in yaml_content.items():
        if isinstance(value, str):
            yaml_content[key] = os.path.expandvars(value)
        elif isinstance(value, dict):
            substitute_env_vars(value)


def load_yaml_with_env(filename: str) -> dict:
    with open(filename) as file:
        yaml_content = yaml.safe_load(file)
        substitute_env_vars(yaml_content)
        return yaml_content


def sql_connection(
    user: str, password: str, host: str, database: str, schema: str
) -> Engine:
    """
    SQL Connection Function for connecting to Postgres Database

    Args:
        user (str): Database User

        password (str): Database password

        host (str): Database Host IP

        database (str): Database to connect to

        schema (str): The Schema in the DB to connect to.

    Returns:
        SQL Engine variable to a specified schema in the DB
    """
    connection = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}",
        connect_args={"options": f"-csearch_path={schema}"},
        # defining schema to connect to
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


def generate_data(postgres_engine: Engine, source_tables: list[str]):
    """
    Function to pull tables from Postgres and load them into Global
    Memory as Pandas DataFrames to be used in Data Tables + Plots
    for the Dashboard

    Args:
        postgres_engine (Engine): SQLAlchemy Engine Object to the Postgres
            Database

        source_tables (list[str]): List of Source Tables to load in.

    Returns:
        None, but loads all source tables into Pandas DataFrames

    """
    with postgres_engine.begin() as connection:
        for table in source_tables:
            if "." in table:
                table_name = table.split(".")[1]
                globals()[f"{table_name}_df"] = get_data(
                    table_name=table, conn=connection
                )
            elif table in ("reddit_sentiment_time_series", "mov"):
                globals()[f"{table}_df"] = get_data(
                    table_name=table, conn=connection, limit_amount=10000000
                )
            else:
                globals()[f"{table}_df"] = get_data(table_name=table, conn=connection)


env = load_yaml_with_env("config.yaml")[os.environ.get("ENV_TYPE")]

engine = sql_connection(
    user=env["user"],
    password=env["pass"],
    host=env["host"],
    database=env["database"],
    schema=env["schema"],
)

generate_data(postgres_engine=engine, source_tables=source_tables)
