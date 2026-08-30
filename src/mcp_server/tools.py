"""Tool implementations, kept free of FastMCP so they're testable on their own.

`app.py` is a thin registration layer over these functions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from typing import Any, Literal

from sqlalchemy.engine.base import Engine

from src.mcp_server import gold_queries
from src.mcp_server.semantic import (
    TEAM_GAMES_METRICS,
    SemanticLayer,
    SemanticLayerError,
    team_filter,
)
from src.mcp_server.settings import Settings, clamp_limit
from src.mcp_server.teams import Team, resolve_team, team_directory

logger = logging.getLogger(__name__)

RECENT_GAMES_IN_SNAPSHOT = 10
ValueMode = Literal["overpaid", "underpaid"]


@dataclass(frozen=True)
class ServerContext:
    engine: Engine
    semantic: SemanticLayer
    settings: Settings


def get_team_snapshot(context: ServerContext, team: str) -> dict[str, Any]:
    """One team's current picture: record, form, ratings, and payroll position."""
    resolved = resolve_team(team)
    form, form_source, form_error = _team_form(context, resolved)

    return {
        "team": {"abbreviation": resolved.abbreviation, "name": resolved.full_name},
        "form": form,
        "form_source": form_source,
        "form_error": form_error,
        "standings": gold_queries.team_standings(context.engine, resolved),
        "ratings": gold_queries.team_ratings(context.engine, resolved),
        "venue_splits": _venue_splits(context, resolved, form_source),
        "blown_leads": gold_queries.team_blown_leads(context.engine, resolved),
        "payroll": gold_queries.team_payroll(context.engine, resolved),
        "recent_games": gold_queries.team_recent_games(
            context.engine, resolved, limit=RECENT_GAMES_IN_SNAPSHOT
        ),
    }


def _team_form(context: ServerContext, team: Team) -> tuple[dict[str, Any] | None, str, str | None]:
    """Team form via the semantic layer, falling back to equivalent SQL over `gold`.

    Returns (form, source, error) so the caller can tell the LLM which path answered.
    """
    if context.semantic.available:
        dimension = context.settings.team_dimension
        try:
            result = context.semantic.query(
                metrics=TEAM_GAMES_METRICS,
                group_by=[dimension],
                where=[team_filter(dimension, team.abbreviation)],
                limit=1,
            )
            if result.rows:
                return result.rows[0], "metricflow", None
            return None, "metricflow", "no metric rows for this team"
        except SemanticLayerError as exc:
            # A broken metric query shouldn't sink the whole snapshot — report it and
            # answer from `gold` instead.
            logger.warning("semantic query failed for %s: %s", team.abbreviation, exc)
            fallback = gold_queries.team_form_from_recent_games(context.engine, team)
            return fallback, "gold_fallback", str(exc)

    fallback = gold_queries.team_form_from_recent_games(context.engine, team)
    return fallback, "gold_fallback", context.semantic.status().get("reason")


def _venue_splits(context: ServerContext, team: Team, form_source: str) -> list[dict[str, Any]]:
    """Home/away breakdown of the same metrics.

    Follows whichever path `_team_form` already settled on, so a snapshot never mixes
    metric-derived headline numbers with SQL-derived splits.
    """
    if form_source == "metricflow":
        try:
            return context.semantic.query(
                metrics=TEAM_GAMES_METRICS,
                group_by=[context.settings.venue_dimension],
                where=[team_filter(context.settings.team_dimension, team.abbreviation)],
            ).rows
        except SemanticLayerError as exc:
            logger.warning("venue split failed for %s: %s", team.abbreviation, exc)

    return gold_queries.team_form_by_venue(context.engine, team)


def get_player_value(
    context: ServerContext,
    team: str | None = None,
    mode: ValueMode = "overpaid",
    limit: int | None = None,
) -> dict[str, Any]:
    """Production-vs-pay ranking; the analysis the dashboard was built around."""
    if mode not in ("overpaid", "underpaid"):
        raise ValueError("mode must be 'overpaid' or 'underpaid'")

    resolved = resolve_team(team) if team else None
    row_limit = clamp_limit(limit, default=context.settings.max_rows)
    players = gold_queries.player_value(
        context.engine,
        team=resolved,
        overpaid=mode == "overpaid",
        limit=row_limit,
    )

    return {
        "mode": mode,
        "team": (
            {"abbreviation": resolved.abbreviation, "name": resolved.full_name}
            if resolved
            else None
        ),
        "payroll": gold_queries.team_payroll(context.engine, resolved) if resolved else None,
        "players": players,
        "metric_notes": (
            "value_z_score = production z-score minus salary z-score; negative means the "
            "player is producing less than his pay would suggest."
        ),
    }


def get_upcoming_games(
    context: ServerContext,
    game_date: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Tonight's slate (or a given date) with model win probabilities."""
    row_limit = clamp_limit(limit, default=context.settings.max_rows)
    today = date.today().isoformat()

    if game_date is None or game_date == today:
        games = gold_queries.tonights_games(context.engine, limit=row_limit)
        resolved_date = game_date or today
        source_table = "schedule_tonights_games"
    else:
        _validate_iso_date(game_date)
        games = gold_queries.scheduled_games(context.engine, game_date, limit=row_limit)
        resolved_date = game_date
        source_table = "schedule_season_remaining"

    return {
        "date": resolved_date,
        "source_table": source_table,
        "games": games,
        "against_the_spread": gold_queries.team_odds_outcomes(
            context.engine, _abbreviations_for_games(games)
        ),
    }


def _validate_iso_date(value: str) -> None:
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"date must be ISO format (YYYY-MM-DD), got '{value}'") from exc


def _abbreviations_for_games(games: list[dict[str, Any]]) -> list[str]:
    """Team abbreviations for the teams playing, for the spread-coverage lookup."""
    abbreviations: list[str] = []
    for game in games:
        for key in ("home_team", "away_team"):
            name = game.get(key)
            if not name:
                continue
            try:
                abbreviations.append(resolve_team(str(name)).abbreviation)
            except ValueError:
                continue
    return sorted(set(abbreviations))


def get_teams() -> list[dict[str, str]]:
    """Payload for the `nba://teams` resource."""
    return team_directory()


def get_data_freshness(context: ServerContext) -> dict[str, Any]:
    """Payload for the `nba://data-freshness` resource."""
    return {
        "gold": gold_queries.data_freshness(context.engine),
        "semantic_layer": context.semantic.status(),
    }
