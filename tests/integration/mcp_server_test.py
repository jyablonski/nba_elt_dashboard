"""End-to-end over the MCP Streamable HTTP transport: auth, tools/list, tool call."""

import asyncio
import json

import httpx
import pytest

from src.mcp_server.app import create_app

MCP_PATH = "/mcp"
MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def _rpc(method: str, params: dict | None = None, request_id: int = 1) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}}


def _parse_response(response: httpx.Response) -> dict:
    """Streamable HTTP replies with SSE; pull the single JSON-RPC message out of it."""
    if response.headers.get("content-type", "").startswith("application/json"):
        return response.json()
    for line in response.text.splitlines():
        if line.startswith("data: "):
            return json.loads(line[len("data: ") :])
    raise AssertionError(f"no SSE data frame in response: {response.text!r}")


def _request(app, send_request):
    """Drive the ASGI lifespan around one request.

    The Streamable HTTP session manager starts its task group in the app's lifespan, so
    httpx's ASGITransport alone (which never emits lifespan events) isn't enough.
    """

    async def _run():
        to_app: asyncio.Queue = asyncio.Queue()
        from_app: asyncio.Queue = asyncio.Queue()
        scope = {"type": "lifespan", "asgi": {"version": "3.0"}}
        lifespan = asyncio.create_task(app(scope, to_app.get, from_app.put))

        await to_app.put({"type": "lifespan.startup"})
        startup = await from_app.get()
        assert startup["type"] == "lifespan.startup.complete", startup

        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://mcp.test") as client:
                return await send_request(client)
        finally:
            await to_app.put({"type": "lifespan.shutdown"})
            await from_app.get()
            await lifespan

    return asyncio.run(_run())


def _post(app, payload: dict, token: str | None = "test-token") -> httpx.Response:
    headers = dict(MCP_HEADERS)
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"

    return _request(app, lambda client: client.post(MCP_PATH, json=payload, headers=headers))


@pytest.fixture
def mcp_app(mcp_context):
    # Fresh app per test: a StreamableHTTPSessionManager's lifespan can only run once.
    return create_app(mcp_context)


def test_requests_without_a_token_are_rejected(mcp_app):
    response = _post(mcp_app, _rpc("tools/list"), token=None)

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_requests_with_a_wrong_token_are_rejected(mcp_app):
    assert _post(mcp_app, _rpc("tools/list"), token="nope").status_code == 401


def test_tools_list_advertises_the_three_tools(mcp_app):
    response = _post(mcp_app, _rpc("tools/list"))

    assert response.status_code == 200
    tools = _parse_response(response)["result"]["tools"]
    assert {tool["name"] for tool in tools} == {
        "get_team_snapshot",
        "get_player_value",
        "get_upcoming_games",
    }


def test_resources_list_advertises_both_resources(mcp_app):
    resources = _parse_response(_post(mcp_app, _rpc("resources/list")))["result"]["resources"]

    assert {resource["uri"] for resource in resources} == {
        "nba://teams",
        "nba://data-freshness",
    }


def test_get_team_snapshot_round_trips_through_the_transport(mcp_app):
    response = _post(
        mcp_app,
        _rpc("tools/call", {"name": "get_team_snapshot", "arguments": {"team": "celtics"}}),
    )

    result = _parse_response(response)["result"]
    assert result.get("isError") is not True
    payload = result["structuredContent"]
    assert payload["team"]["abbreviation"] == "BOS"
    assert payload["form_source"] == "metricflow"
    assert payload["standings"]["team"] == "BOS"


def test_a_tool_error_comes_back_as_an_mcp_error(mcp_app):
    response = _post(
        mcp_app,
        _rpc("tools/call", {"name": "get_player_value", "arguments": {"mode": "cheapest"}}),
    )

    result = _parse_response(response)["result"]
    assert result["isError"] is True
    assert "overpaid" in result["content"][0]["text"]


def test_teams_resource_reads_back_as_json(mcp_app):
    response = _post(mcp_app, _rpc("resources/read", {"uri": "nba://teams"}))

    contents = _parse_response(response)["result"]["contents"][0]
    teams = json.loads(contents["text"])
    assert len(teams) == 30
    assert {"abbreviation": "LAL", "name": "Los Angeles Lakers"} in teams


def test_health_endpoint_is_exempt_from_auth(mcp_app):
    response = _request(mcp_app, lambda client: client.get("/health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "semantic_layer_available": True}
