from __future__ import annotations

import os
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine

from src.data_access.database import coerce_engine_port, load_yaml_with_env

GOLD_SCHEMA = "gold"


def create_readonly_engine(
    config_path: str = "config.yaml",
    env_type: str | None = None,
) -> Engine:
    """Build the MCP service's own engine over `gold`.

    Separate from `get_dashboard_engine()` on purpose: the dashboard engine backs a
    2,000-row snapshot cache tuned for the UI, and the MCP service should be able to
    connect as a different (read-only) Postgres role. `MCP_DB_USER` / `MCP_DB_PASSWORD`
    override the config.yaml credentials for exactly that reason.
    """
    env = load_yaml_with_env(config_path)[env_type or os.environ.get("ENV_TYPE", "dev")]
    user = os.environ.get("MCP_DB_USER") or env["user"]
    password = os.environ.get("MCP_DB_PASSWORD") or env["pass"]
    schema = env.get("schema", GOLD_SCHEMA)

    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{env['host']}"
        f":{coerce_engine_port(env['port'])}/{env['database']}",
        # Belt-and-braces alongside the read-only role: every session in this process
        # refuses writes even if the role is over-provisioned.
        connect_args={
            "options": f"-csearch_path={schema} -cdefault_transaction_read_only=on",
        },
        pool_pre_ping=True,
        echo=False,
    )


def fetch_rows(
    engine: Engine,
    sql: str,
    params: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Run a read query and return JSON-ready rows."""
    with engine.connect() as connection:
        result = connection.execute(text(sql), params or {})
        columns = list(result.keys())
        return [dict(zip(columns, _jsonify_row(row))) for row in result.fetchall()]


def _jsonify_row(row: Any) -> list[Any]:
    return [_jsonify_value(value) for value in row]


def _jsonify_value(value: Any) -> Any:
    """Coerce Postgres types the JSON encoder can't handle (Decimal, date, ...)."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if hasattr(value, "as_integer_ratio"):  # Decimal
        return float(value)
    return str(value)
