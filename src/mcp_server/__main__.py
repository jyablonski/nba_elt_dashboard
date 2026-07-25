"""Entrypoint: `python -m src.mcp_server` serves Streamable HTTP MCP on :9100."""

from __future__ import annotations

import logging

import uvicorn

from src.mcp_server.app import create_app, build_context
from src.mcp_server.settings import load_settings


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    settings = load_settings()
    if not settings.auth_token:
        # The gate fails closed, so this would serve nothing but 401s. Say so loudly.
        logging.getLogger(__name__).error(
            "MCP_AUTH_TOKEN is not set; every request will be rejected with 401"
        )

    context = build_context(settings)
    logging.getLogger(__name__).info(
        "semantic layer: %s", context.semantic.status().get("reason", "loaded")
    )
    uvicorn.run(
        create_app(context),
        host=settings.host,
        port=settings.port,
        log_level="info",
        # Streamable HTTP holds long-lived SSE responses open; don't reap them.
        timeout_keep_alive=120,
    )


if __name__ == "__main__":
    main()
