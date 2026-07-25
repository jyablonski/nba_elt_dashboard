"""FastMCP registration: a thin layer over `tools.py`."""

from __future__ import annotations

import json
import logging
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.responses import JSONResponse

from src.mcp_server import tools
from src.mcp_server.auth import BearerTokenMiddleware
from src.mcp_server.database import create_readonly_engine
from src.mcp_server.semantic import build_semantic_layer
from src.mcp_server.settings import Settings, load_settings
from src.mcp_server.tools import ServerContext

logger = logging.getLogger(__name__)

HEALTH_PATH = "/health"

INSTRUCTIONS = """\
NBA data from a dbt-modeled `gold` warehouse behind jyablonski's NBA dashboard.

Use `get_team_snapshot` for "how are the <team> doing" questions, `get_player_value` for
contract value / overpaid / underpaid questions, and `get_upcoming_games` for schedule and
win-probability questions. Team arguments accept a nickname, city, abbreviation, or full
name ("lakers", "LAL", "Los Angeles Lakers").
"""


def build_context(settings: Settings | None = None) -> ServerContext:
    """Construct the shared engine + warm semantic layer once, at startup."""
    resolved = settings or load_settings()
    engine = create_readonly_engine(
        config_path=resolved.config_path,
        env_type=resolved.env_type,
    )
    semantic = build_semantic_layer(resolved.semantic_manifest_path, engine)
    return ServerContext(engine=engine, semantic=semantic, settings=resolved)


def _transport_security(context: ServerContext) -> TransportSecuritySettings | None:
    """Host/Origin allowlist for the SDK's DNS-rebinding protection.

    Unset means the SDK's localhost-only default, which 421s every request that arrives
    with the public Host header — so prod must set MCP_ALLOWED_HOSTS.
    """
    settings = context.settings
    if not settings.allowed_hosts and not settings.allowed_origins:
        return None
    return TransportSecuritySettings(
        allowed_hosts=list(settings.allowed_hosts),
        allowed_origins=list(settings.allowed_origins),
    )


def create_mcp_server(context: ServerContext) -> FastMCP:
    server = FastMCP(
        name="nba-elt-dashboard",
        instructions=INSTRUCTIONS,
        host=context.settings.host,
        port=context.settings.port,
        stateless_http=True,
        transport_security=_transport_security(context),
    )

    @server.tool(
        name="get_team_snapshot",
        description=(
            "Current picture for one NBA team: record and recent form (win %, average "
            "margin, points scored/allowed), a home/away split of the same numbers, "
            "offensive/defensive/net rating with league ranks, blown-lead and comeback "
            "counts, payroll position, and the last 10 games. Accepts a nickname, "
            "abbreviation, or full team name."
        ),
    )
    def get_team_snapshot(team: str) -> dict[str, Any]:
        return tools.get_team_snapshot(context, team=team)

    @server.tool(
        name="get_player_value",
        description=(
            "Rank players by production relative to pay. mode='overpaid' returns the "
            "worst value contracts, mode='underpaid' the best surplus contracts. Omit "
            "`team` to rank league-wide."
        ),
    )
    def get_player_value(
        team: str | None = None,
        mode: str = "overpaid",
        limit: int | None = None,
    ) -> dict[str, Any]:
        return tools.get_player_value(
            context,
            team=team,
            mode=mode,  # type: ignore[arg-type]  # validated in tools.get_player_value
            limit=limit,
        )

    @server.tool(
        name="get_upcoming_games",
        description=(
            "Scheduled games with moneylines and model win probabilities. Defaults to "
            "tonight's slate; pass `game_date` as YYYY-MM-DD for a future date."
        ),
    )
    def get_upcoming_games(
        game_date: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        return tools.get_upcoming_games(context, game_date=game_date, limit=limit)

    @server.custom_route(HEALTH_PATH, methods=["GET"])
    async def health(request):
        return JSONResponse(
            {"status": "ok", "semantic_layer_available": context.semantic.available}
        )

    @server.resource(
        "nba://teams",
        name="NBA teams",
        description="Canonical team names and abbreviations accepted by the tools.",
        mime_type="application/json",
    )
    def teams_resource() -> str:
        return json.dumps(tools.get_teams(), indent=2)

    @server.resource(
        "nba://data-freshness",
        name="Data freshness",
        description="Latest game/scrape timestamps in `gold` and semantic-layer status.",
        mime_type="application/json",
    )
    def freshness_resource() -> str:
        return json.dumps(tools.get_data_freshness(context), indent=2, default=str)

    return server


def create_app(context: ServerContext | None = None):
    """ASGI app: the MCP Streamable HTTP transport behind the bearer gate."""
    resolved = context or build_context()
    server = create_mcp_server(resolved)

    return BearerTokenMiddleware(
        server.streamable_http_app(),
        expected_token=resolved.settings.auth_token,
        # `/health` is what the container healthcheck hits; it exposes no data.
        exempt_paths=(HEALTH_PATH,),
    )
