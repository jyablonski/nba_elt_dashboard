import os

from sqlalchemy.engine.base import Engine

from src.data import source_tables
from src.db_connection import get_data, sql_connection
from src.yaml_config import load_yaml_with_env


def generate_data(postgres_engine: Engine, source_tables: list[str]) -> None:
    with postgres_engine.begin() as connection:
        for table in source_tables:
            if "." in table:
                table_name = table.split(".")[1]
                globals()[f"{table_name}_df"] = get_data(table_name=table, conn=connection)
            elif table in ("reddit_sentiment_time_series", "mov"):
                globals()[f"{table}_df"] = get_data(
                    table_name=table, conn=connection, limit_amount=10000000
                )
            else:
                globals()[f"{table}_df"] = get_data(table_name=table, conn=connection)


env = load_yaml_with_env("config.yaml")[os.environ.get("ENV_TYPE", "dev")]
_port = env["port"]
if isinstance(_port, str):
    _port = int(_port)

engine = sql_connection(
    user=env["user"],
    password=env["pass"],
    host=env["host"],
    database=env["database"],
    schema=env["schema"],
    port=_port,
)

generate_data(postgres_engine=engine, source_tables=source_tables)
