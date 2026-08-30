from __future__ import annotations

from pathlib import Path

import pytest

from src.mcp_server.database import create_readonly_engine
from src.mcp_server.semantic import build_semantic_layer
from src.mcp_server.settings import Settings
from src.mcp_server.tools import ServerContext

pytestmark = [pytest.mark.integration]

SEMANTIC_MANIFEST_FIXTURE = (
    Path(__file__).resolve().parent.parent / "fixtures" / "semantic_manifest_fixture.json"
)


@pytest.fixture(scope="session")
def mcp_engine(postgres_engine):
    return create_readonly_engine(config_path="config.yaml", env_type="ci")


@pytest.fixture(scope="session")
def mcp_settings():
    return Settings(
        auth_token="test-token",
        host="127.0.0.1",
        port=9100,
        semantic_manifest_path=SEMANTIC_MANIFEST_FIXTURE,
        max_rows=10,
        config_path="config.yaml",
        env_type="ci",
        team_dimension="team_game__team",
        venue_dimension="team_game__venue",
        allowed_hosts=("mcp.test",),
        allowed_origins=(),
    )


@pytest.fixture(scope="session")
def semantic_layer(mcp_engine):
    layer = build_semantic_layer(SEMANTIC_MANIFEST_FIXTURE, mcp_engine)
    if not layer.available:
        pytest.fail(f"semantic layer failed to load: {layer.status()['reason']}")
    return layer


@pytest.fixture(scope="session")
def mcp_context(mcp_engine, semantic_layer, mcp_settings):
    return ServerContext(engine=mcp_engine, semantic=semantic_layer, settings=mcp_settings)
