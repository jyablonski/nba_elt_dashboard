import os
import socket

import pandas as pd
import pytest

# from sqlalchemy.engine.base import Engine


def guard(*args, **kwargs):
    raise Exception("you're using the internet hoe")


socket.socket = guard


# @pytest.fixture(scope="session")
# def postgres_conn() -> Engine:
#     """Fixture to connect to Docker Postgres Container"""
#     # small override for local + docker testing to work fine
#     if os.environ.get("ENV_TYPE") == "docker_dev":
#         host = "postgres"
#     else:
#         host = "localhost"

#     conn = sql_connection(
#         rds_schema="nba_source",
#         rds_user="postgres",
#         rds_pw="postgres",
#         rds_ip=host,
#         rds_db="postgres",
#     )
#     with conn.begin() as conn:
#         yield conn


@pytest.fixture(scope="function")
def pbp_fixture() -> pd.DataFrame:
    """
    Fixture to load player stats data from an html file for testing.
    """
    file_name = os.path.join(os.path.dirname(__file__), "fixtures/pbp_fixture.csv")
    df = pd.read_csv(file_name)

    return df


@pytest.fixture(scope="function")
def team_ratings_fixture() -> pd.DataFrame:
    """
    Fixture to load player stats data from an html file for testing.
    """
    file_name = os.path.join(
        os.path.dirname(__file__), "fixtures/team_ratings_fixture.csv"
    )
    df = pd.read_csv(file_name)

    return df
