from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from src.mcp_server.semantic import DEFAULT_TEAM_DIMENSION, DEFAULT_VENUE_DIMENSION

DEFAULT_PORT = 9100
DEFAULT_MAX_ROWS = 50
# Absolute cap on rows any tool may return, regardless of a caller-supplied `limit`.
# Tool payloads are fed straight into an LLM context, so a runaway result set is a real cost.
ROW_LIMIT_CEILING = 200


@dataclass(frozen=True)
class Settings:
    auth_token: str | None
    host: str
    port: int
    semantic_manifest_path: Path | None
    max_rows: int
    config_path: str
    env_type: str
    team_dimension: str
    venue_dimension: str
    allowed_hosts: tuple[str, ...]
    allowed_origins: tuple[str, ...]


def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def load_settings() -> Settings:
    manifest = os.environ.get("MCP_SEMANTIC_MANIFEST_PATH")
    return Settings(
        auth_token=os.environ.get("MCP_AUTH_TOKEN") or None,
        host=os.environ.get("MCP_HOST", "0.0.0.0"),
        port=_int_env("MCP_PORT", DEFAULT_PORT),
        semantic_manifest_path=Path(manifest) if manifest else None,
        max_rows=clamp_limit(_int_env("MCP_MAX_ROWS", DEFAULT_MAX_ROWS)),
        config_path=os.environ.get("MCP_CONFIG_PATH", "config.yaml"),
        env_type=os.environ.get("ENV_TYPE", "dev"),
        team_dimension=os.environ.get("MCP_TEAM_DIMENSION", DEFAULT_TEAM_DIMENSION),
        venue_dimension=os.environ.get("MCP_VENUE_DIMENSION", DEFAULT_VENUE_DIMENSION),
        # The MCP SDK's DNS-rebinding protection rejects any Host it doesn't know with a
        # 421. Behind Caddy the Host is the public domain, so it must be listed here or
        # the deployed server answers nothing. Empty = the SDK's localhost-only default.
        allowed_hosts=_csv_env("MCP_ALLOWED_HOSTS"),
        allowed_origins=_csv_env("MCP_ALLOWED_ORIGINS"),
    )


def _csv_env(name: str) -> tuple[str, ...]:
    raw = os.environ.get(name, "")
    return tuple(item.strip() for item in raw.split(",") if item.strip())


def clamp_limit(limit: int | None, default: int = DEFAULT_MAX_ROWS) -> int:
    """Bound a caller-supplied row limit into [1, ROW_LIMIT_CEILING]."""
    if limit is None:
        return default
    return max(1, min(int(limit), ROW_LIMIT_CEILING))
