"""Apply `docker/postgres_bootstrap.sql` to a running Postgres instance (used by Testcontainers)."""

from __future__ import annotations

from pathlib import Path

import sqlparse
from sqlalchemy import text
from sqlalchemy.engine import Engine


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def bootstrap_sql_path() -> Path:
    return repo_root() / "docker" / "postgres_bootstrap.sql"


def apply_bootstrap(engine: Engine, *, sql_path: Path | None = None) -> None:
    path = sql_path or bootstrap_sql_path()
    raw = path.read_text(encoding="utf-8")
    statements = [s.strip() for s in sqlparse.split(raw) if s.strip()]
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
