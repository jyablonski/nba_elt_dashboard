from src.mcp_server import __main__ as entrypoint
from src.mcp_server.semantic import UnavailableSemanticLayer
from src.mcp_server.tools import ServerContext


def _stub_run(monkeypatch, settings):
    """Stand in for uvicorn/engine so `main()` can be exercised without a server or DB."""
    captured = {}
    context = ServerContext(
        engine=object(), semantic=UnavailableSemanticLayer("no manifest"), settings=settings
    )

    monkeypatch.setattr(entrypoint, "load_settings", lambda: settings)
    monkeypatch.setattr(entrypoint, "build_context", lambda resolved: context)
    monkeypatch.setattr(entrypoint, "create_app", lambda ctx: "asgi-app")
    monkeypatch.setattr(
        entrypoint.uvicorn,
        "run",
        lambda app, **kwargs: captured.update({"app": app, **kwargs}),
    )
    return captured


def test_main_serves_on_the_configured_host_and_port(monkeypatch):
    from src.mcp_server.settings import load_settings

    monkeypatch.setenv("MCP_AUTH_TOKEN", "secret")
    monkeypatch.setenv("MCP_PORT", "9100")
    captured = _stub_run(monkeypatch, load_settings())

    entrypoint.main()

    assert captured["app"] == "asgi-app"
    assert captured["port"] == 9100
    assert captured["timeout_keep_alive"] == 120


def test_main_warns_when_no_auth_token_is_configured(monkeypatch, caplog):
    from src.mcp_server.settings import load_settings

    monkeypatch.delenv("MCP_AUTH_TOKEN", raising=False)
    _stub_run(monkeypatch, load_settings())

    entrypoint.main()

    assert "MCP_AUTH_TOKEN is not set" in caplog.text
