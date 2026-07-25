from pathlib import Path

from src.mcp_server.settings import DEFAULT_MAX_ROWS, ROW_LIMIT_CEILING, clamp_limit, load_settings


def test_load_settings_defaults(monkeypatch):
    for name in (
        "MCP_AUTH_TOKEN",
        "MCP_HOST",
        "MCP_PORT",
        "MCP_SEMANTIC_MANIFEST_PATH",
        "MCP_MAX_ROWS",
        "MCP_CONFIG_PATH",
        "MCP_TEAM_DIMENSION",
        "MCP_ALLOWED_HOSTS",
        "MCP_ALLOWED_ORIGINS",
        "ENV_TYPE",
    ):
        monkeypatch.delenv(name, raising=False)

    settings = load_settings()

    assert settings.auth_token is None
    assert settings.host == "0.0.0.0"
    assert settings.port == 9100
    assert settings.semantic_manifest_path is None
    assert settings.max_rows == DEFAULT_MAX_ROWS
    assert settings.team_dimension == "team_game__team"
    assert settings.allowed_hosts == ()


def test_load_settings_reads_the_environment(monkeypatch):
    monkeypatch.setenv("MCP_AUTH_TOKEN", "secret")
    monkeypatch.setenv("MCP_PORT", "9999")
    monkeypatch.setenv("MCP_SEMANTIC_MANIFEST_PATH", "/tmp/semantic_manifest.json")
    monkeypatch.setenv("MCP_TEAM_DIMENSION", "team__team")

    settings = load_settings()

    assert settings.auth_token == "secret"
    assert settings.port == 9999
    assert settings.semantic_manifest_path == Path("/tmp/semantic_manifest.json")
    assert settings.team_dimension == "team__team"


def test_load_settings_parses_the_host_allowlist(monkeypatch):
    monkeypatch.setenv("MCP_ALLOWED_HOSTS", "mcp.jyablonski.dev, localhost:9100 ,")
    monkeypatch.setenv("MCP_ALLOWED_ORIGINS", "")

    settings = load_settings()

    assert settings.allowed_hosts == ("mcp.jyablonski.dev", "localhost:9100")
    assert settings.allowed_origins == ()


def test_load_settings_ignores_a_non_numeric_port(monkeypatch):
    monkeypatch.setenv("MCP_PORT", "not-a-port")

    assert load_settings().port == 9100


def test_clamp_limit_bounds_caller_supplied_limits():
    assert clamp_limit(None) == DEFAULT_MAX_ROWS
    assert clamp_limit(None, default=5) == 5
    assert clamp_limit(0) == 1
    assert clamp_limit(-10) == 1
    assert clamp_limit(25) == 25
    assert clamp_limit(10_000) == ROW_LIMIT_CEILING
