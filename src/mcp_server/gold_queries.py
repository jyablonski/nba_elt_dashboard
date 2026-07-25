"""Direct `gold` reads for everything the semantic layer doesn't model yet.

The SQL itself lives in `src/mcp_server/queries/*.sql`, one file per query — this module
only binds parameters and shapes results. Keeping the statements out of Python means the
hardcoded table/column assumptions (see the schema-drift risk in docs/mcp-server-plan.md)
sit in one reviewable place, and no statement is ever assembled by string formatting.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from sqlalchemy.engine.base import Engine

from src.mcp_server.database import fetch_rows
from src.mcp_server.teams import Team

QUERY_DIR = Path(__file__).parent / "queries"

# `player_value.sql` sorts by `value_z_score * :direction`, so the sort order is a bound
# parameter rather than interpolated SQL.
_ASCENDING = 1  # most overpaid first
_DESCENDING = -1  # best surplus value first


@lru_cache(maxsize=None)
def load_query(name: str) -> str:
    """Read a statement from `queries/`, cached for the process lifetime."""
    if not name.isidentifier():
        raise ValueError(f"invalid query name: {name!r}")
    return (QUERY_DIR / f"{name}.sql").read_text(encoding="utf-8")


def team_standings(engine: Engine, team: Team) -> dict[str, Any] | None:
    rows = fetch_rows(
        engine,
        load_query("team_standings"),
        {"abbreviation": team.abbreviation},
    )
    return rows[0] if rows else None


def team_ratings(engine: Engine, team: Team) -> dict[str, Any] | None:
    rows = fetch_rows(
        engine,
        load_query("team_ratings"),
        {"abbreviation": team.abbreviation},
    )
    return rows[0] if rows else None


def team_blown_leads(engine: Engine, team: Team) -> list[dict[str, Any]]:
    return fetch_rows(
        engine,
        load_query("team_blown_leads"),
        {"abbreviation": team.abbreviation},
    )


def team_recent_games(engine: Engine, team: Team, limit: int) -> list[dict[str, Any]]:
    return fetch_rows(
        engine,
        load_query("team_recent_games"),
        {"abbreviation": team.abbreviation, "limit": limit},
    )


def team_form_from_recent_games(engine: Engine, team: Team) -> dict[str, Any] | None:
    """Aggregate fallback for `get_team_snapshot` when the semantic layer is unavailable."""
    rows = fetch_rows(
        engine,
        load_query("team_form_from_recent_games"),
        {"abbreviation": team.abbreviation},
    )
    if not rows or not rows[0].get("games_played"):
        return None
    return rows[0]


def team_form_by_venue(engine: Engine, team: Team) -> list[dict[str, Any]]:
    """Home/away split, mirroring the `venue` dimension in the dbt semantic model."""
    return fetch_rows(
        engine,
        load_query("team_form_by_venue"),
        {"abbreviation": team.abbreviation},
    )


def player_value(
    engine: Engine,
    *,
    team: Team | None,
    overpaid: bool,
    limit: int,
) -> list[dict[str, Any]]:
    """Production-vs-pay ranking from `player_salary_value`."""
    return fetch_rows(
        engine,
        load_query("player_value"),
        {
            "abbreviation": team.abbreviation if team is not None else None,
            "direction": _ASCENDING if overpaid else _DESCENDING,
            "limit": limit,
        },
    )


def team_payroll(engine: Engine, team: Team) -> dict[str, Any] | None:
    rows = fetch_rows(
        engine,
        load_query("team_payroll"),
        {"abbreviation": team.abbreviation},
    )
    return rows[0] if rows else None


def tonights_games(engine: Engine, limit: int) -> list[dict[str, Any]]:
    return fetch_rows(engine, load_query("tonights_games"), {"limit": limit})


def scheduled_games(engine: Engine, game_date: str, limit: int) -> list[dict[str, Any]]:
    return fetch_rows(
        engine,
        load_query("scheduled_games"),
        {"game_date": game_date, "limit": limit},
    )


def team_odds_outcomes(engine: Engine, teams: list[str]) -> list[dict[str, Any]]:
    if not teams:
        return []
    return fetch_rows(engine, load_query("team_odds_outcomes"), {"teams": teams})


def data_freshness(engine: Engine) -> dict[str, Any]:
    rows = fetch_rows(engine, load_query("data_freshness"))
    return rows[0] if rows else {}
