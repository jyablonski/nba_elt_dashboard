import asyncio

import pytest

from src.mcp_server import app as app_module
from src.mcp_server.app import build_context, create_app, create_mcp_server
from src.mcp_server.semantic import UnavailableSemanticLayer
from src.mcp_server.settings import Settings
from src.mcp_server.tools import ServerContext


def _settings(**overrides):
    defaults = dict(
        auth_token="token",
        host="127.0.0.1",
        port=9100,
        semantic_manifest_path=None,
        max_rows=10,
        config_path="config.yaml",
        env_type="dev",
        team_dimension="team_game__team",
        venue_dimension="team_game__venue",
        allowed_hosts=(),
        allowed_origins=(),
    )
    defaults.update(overrides)
    return Settings(**defaults)


def _context(**overrides):
    return ServerContext(
        engine=object(),
        semantic=UnavailableSemanticLayer("no manifest"),
        settings=_settings(**overrides),
    )


def test_server_registers_the_three_tools_and_two_resources():
    server = create_mcp_server(_context())

    assert {tool.name for tool in asyncio.run(server.list_tools())} == {
        "get_team_snapshot",
        "get_player_value",
        "get_upcoming_games",
    }
    assert {str(resource.uri) for resource in asyncio.run(server.list_resources())} == {
        "nba://teams",
        "nba://data-freshness",
    }


def test_transport_security_is_unset_without_an_allowlist():
    assert app_module._transport_security(_context()) is None


def test_transport_security_uses_the_configured_allowlist():
    security = app_module._transport_security(
        _context(allowed_hosts=("mcp.jyablonski.dev",), allowed_origins=("https://claude.ai",))
    )

    assert security.allowed_hosts == ["mcp.jyablonski.dev"]
    assert security.allowed_origins == ["https://claude.ai"]


def test_create_app_wraps_the_transport_in_the_bearer_gate():
    wrapped = create_app(_context(auth_token="secret"))

    assert wrapped.expected_token == "secret"
    assert wrapped.exempt_paths == ("/health",)


def test_build_context_loads_the_engine_and_semantic_layer(monkeypatch):
    engine = object()
    monkeypatch.setattr(app_module, "create_readonly_engine", lambda **kwargs: engine)
    monkeypatch.setattr(
        app_module,
        "build_semantic_layer",
        lambda manifest, engine: UnavailableSemanticLayer("stubbed"),
    )

    context = build_context(_settings())

    assert context.engine is engine
    assert context.semantic.status()["reason"] == "stubbed"


@pytest.mark.parametrize("resource_uri", ["nba://teams", "nba://data-freshness"])
def test_resources_render_json(monkeypatch, resource_uri):
    monkeypatch.setattr(app_module.tools, "get_data_freshness", lambda context: {"gold": {}})
    server = create_mcp_server(_context())

    contents = asyncio.run(server.read_resource(resource_uri))

    assert list(contents)[0].mime_type == "application/json"
