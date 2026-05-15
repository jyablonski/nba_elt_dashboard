from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pandas as pd
import pytest
from sqlalchemy import create_engine

from src.db_connection import sql_connection
from src.yaml_config import load_yaml_with_env
from tests.postgres_bootstrap import apply_bootstrap

if TYPE_CHECKING:
    from sqlalchemy.engine.base import Engine


def _needs_postgres(config: pytest.Config) -> bool:
    """True when the suite is not restricted to unit tests only."""
    if getattr(config.option, "collectonly", False):
        return False
    args = getattr(config, "args", []) or []
    if not args:
        return True
    normalized = [str(a).replace("\\", "/") for a in args if not str(a).startswith("-")]
    if not normalized:
        return True
    for p in normalized:
        if "integration" in p:
            return True
    if all("unit" in p for p in normalized):
        return False
    return True


def _docker_available() -> bool:
    try:
        import docker

        docker.from_env().ping()
        return True
    except Exception:
        return False


def pytest_configure(config: pytest.Config) -> None:
    if getattr(config.option, "collectonly", False):
        return
    if not _needs_postgres(config):
        return
    if os.environ.get("SKIP_INTEGRATION") == "1":
        return
    if not _docker_available():
        return

    from testcontainers.postgres import PostgresContainer

    postgres = PostgresContainer(
        "postgres:16-alpine",
        username="nba_dashboard_user",
        password="postgres",
        dbname="postgres",
    )
    postgres.start()
    engine = create_engine(postgres.get_connection_url())
    apply_bootstrap(engine)

    os.environ["ENV_TYPE"] = "ci"
    os.environ["RDS_USER"] = "nba_dashboard_user"
    os.environ["RDS_HOST"] = postgres.get_container_host_ip()
    os.environ["RDS_PORT"] = str(postgres.get_exposed_port(5432))

    config._tc_postgres_container = postgres  # noqa: SLF001
    config._tc_engine = engine  # noqa: SLF001


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if getattr(config.option, "collectonly", False):
        return
    if not _needs_postgres(config):
        return
    if os.environ.get("SKIP_INTEGRATION") == "1":
        skip = pytest.mark.skip(reason="SKIP_INTEGRATION=1")
        for item in items:
            if item.get_closest_marker("integration"):
                item.add_marker(skip)
        return
    if getattr(config, "_tc_engine", None) is None:
        skip = pytest.mark.skip(
            reason="Docker is not available; integration tests need Testcontainers Postgres."
        )
        for item in items:
            if item.get_closest_marker("integration"):
                item.add_marker(skip)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    postgres = getattr(session.config, "_tc_postgres_container", None)
    if postgres is not None:
        try:
            postgres.stop()
        except Exception:
            pass


@pytest.fixture(scope="session")
def postgres_engine(request: pytest.FixtureRequest) -> Engine:
    engine = getattr(request.config, "_tc_engine", None)
    if engine is None:
        pytest.skip("Postgres Testcontainers engine not initialized for this session.")
    return engine


@pytest.fixture(scope="session")
def postgres_conn(request: pytest.FixtureRequest):
    env = load_yaml_with_env("config.yaml")[os.environ["ENV_TYPE"]]
    port = env["port"]
    if isinstance(port, str):
        port = int(port)
    conn_engine = sql_connection(
        schema="nba_source",
        user=env["user"],
        password=env["pass"],
        host=env["host"],
        database=env["database"],
        port=port,
    )
    with conn_engine.begin() as connection:
        yield connection


@pytest.fixture
def pbp_fixture() -> pd.DataFrame:
    file_name = os.path.join(os.path.dirname(__file__), "fixtures/pbp_fixture.csv")
    return pd.read_csv(file_name)


@pytest.fixture
def team_ratings_fixture() -> pd.DataFrame:
    file_name = os.path.join(os.path.dirname(__file__), "fixtures/team_ratings_fixture.csv")
    return pd.read_csv(file_name)


@pytest.fixture
def config_fixture() -> dict[str, str]:
    file_name = os.path.join(os.path.dirname(__file__), "fixtures/config_fixture.yaml")
    env_type = os.environ.get("ENV_TYPE", "dev")
    env_vars = load_yaml_with_env(file_name)[env_type]
    return env_vars
