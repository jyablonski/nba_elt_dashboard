from __future__ import annotations

import os
import socket
from typing import TYPE_CHECKING

import pandas as pd
import pytest

from src.database import sql_connection, load_yaml_with_env

if TYPE_CHECKING:
    from sqlalchemy.engine.base import Engine


def guard(*args, **kwargs):
    raise Exception("you're using the internet hoe")


socket.socket = guard


@pytest.fixture(scope="session")
def postgres_engine() -> Engine:
    """Fixture to generate SQLAlchemy Engine Object"""

    if os.environ.get("ENV_TYPE") == "docker_dev":
        host = "postgres"
    else:
        host = "localhost"

    engine = sql_connection(
        schema="nba_prod",
        user="nba_dashboard_user",
        password="postgres",
        host=host,
        database="postgres",
    )

    return engine


@pytest.fixture(scope="session")
def postgres_conn() -> Engine:
    """Fixture to connect to Docker Postgres Container"""

    if os.environ.get("ENV_TYPE") == "docker_dev":
        host = "postgres"
    else:
        host = "localhost"

    conn = sql_connection(
        schema="nba_source",
        user="nba_dashboard_user",
        password="postgres",
        host=host,
        database="postgres",
    )
    with conn.begin() as conn:
        yield conn


@pytest.fixture(scope="function")
def pbp_fixture() -> pd.DataFrame:
    """
    Fixture to load PBP CSV Fixture for Testing
    """
    file_name = os.path.join(os.path.dirname(__file__), "fixtures/pbp_fixture.csv")
    df = pd.read_csv(file_name)

    return df


@pytest.fixture(scope="function")
def team_ratings_fixture() -> pd.DataFrame:
    """
    Fixture to load Team Ratings CSV Fixture for Testing
    """
    file_name = os.path.join(
        os.path.dirname(__file__), "fixtures/team_ratings_fixture.csv"
    )
    df = pd.read_csv(file_name)

    return df


@pytest.fixture(scope="function")
def config_fixture() -> dict[str, str]:
    """
    Fixture to load player stats data from an html file for testing.
    """

    file_name = os.path.join(os.path.dirname(__file__), "fixtures/config_fixture.yaml")
    env_vars = load_yaml_with_env(file_name)[os.environ.get("ENV_TYPE")]

    return env_vars
