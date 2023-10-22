import os
import socket

import pytest
from sqlalchemy.engine.base import Engine

from src.database import sql_connection


def guard(*args, **kwargs):
    raise Exception("you're using the internet hoe")


socket.socket = guard


@pytest.fixture(scope="session")
def postgres_conn() -> Engine:
    """Fixture to connect to Docker Postgres Container"""
    # small override for local + docker testing to work fine
    if os.environ.get("ENV_TYPE") == "docker_dev":
        host = "postgres"
    else:
        host = "localhost"

    conn = sql_connection(
        rds_schema="nba_source",
        rds_user="postgres",
        rds_pw="postgres",
        rds_ip=host,
        rds_db="postgres",
    )
    with conn.begin() as conn:
        yield conn
