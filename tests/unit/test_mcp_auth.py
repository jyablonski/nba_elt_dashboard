import asyncio

from src.mcp_server.auth import BearerTokenMiddleware, extract_bearer_token, is_authorized


def test_extract_bearer_token_variants():
    assert extract_bearer_token("Bearer abc123") == "abc123"
    assert extract_bearer_token("bearer abc123") == "abc123"
    assert extract_bearer_token("Bearer  abc123 ") == "abc123"
    assert extract_bearer_token("Basic abc123") is None
    assert extract_bearer_token("Bearer ") is None
    assert extract_bearer_token(None) is None


def test_is_authorized_accepts_only_the_configured_token():
    assert is_authorized("Bearer secret", "secret") is True
    assert is_authorized("Bearer wrong", "secret") is False
    assert is_authorized(None, "secret") is False


def test_is_authorized_fails_closed_without_a_configured_token():
    # An unconfigured token must not mean "no auth required" on a public endpoint.
    assert is_authorized("Bearer anything", None) is False
    assert is_authorized(None, None) is False


def _call_middleware(middleware, path="/mcp", headers=None):
    scope = {
        "type": "http",
        "path": path,
        "headers": headers if headers is not None else [],
    }
    sent = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    asyncio.run(middleware(scope, receive, send))
    return sent


def test_middleware_rejects_missing_token():
    called = []

    async def app(scope, receive, send):
        called.append(scope)

    sent = _call_middleware(BearerTokenMiddleware(app, expected_token="secret"))

    assert called == []
    assert sent[0]["status"] == 401
    assert b"unauthorized" in sent[1]["body"]


def test_middleware_passes_valid_token_through():
    called = []

    async def app(scope, receive, send):
        called.append(scope)

    sent = _call_middleware(
        BearerTokenMiddleware(app, expected_token="secret"),
        headers=[(b"authorization", b"Bearer secret")],
    )

    assert len(called) == 1
    assert sent == []


def test_middleware_exempts_health_path_and_non_http_scopes():
    called = []

    async def app(scope, receive, send):
        called.append(scope)

    middleware = BearerTokenMiddleware(app, expected_token="secret", exempt_paths=("/health",))
    _call_middleware(middleware, path="/health")
    _call_middleware(middleware, path="/mcp")  # rejected

    scope = {"type": "lifespan"}

    async def receive():
        return {"type": "lifespan.startup"}

    async def send(message):
        return None

    asyncio.run(middleware(scope, receive, send))

    assert [scope["type"] for scope in called] == ["http", "lifespan"]
