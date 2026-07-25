"""Semantic-layer adapter: the only module that imports MetricFlow internals.

MetricFlow's Python API is not a stable public contract, so everything above this file
talks to `SemanticLayer.query(...)` instead. If an upgrade breaks the internals, the
repair is contained here.

We use `metricflow` directly rather than `dbt-metricflow`: MetricFlow compiles metric
queries to SQL and hands them to a `SqlClient`, and we already have a SQLAlchemy engine
over `gold`. Skipping the dbt adapter layer means no dbt-core dependency (which does not
import on Python 3.14) and no `profiles.yml` in the image — the semantic manifest supplies
the definitions, our engine supplies the connection.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, Sequence

from sqlalchemy import text
from sqlalchemy.engine.base import Engine

logger = logging.getLogger(__name__)

# Metric names owned by the dbt track's `team_games` semantic model. Keep in sync with
# docs/mcp-server-plan.md; a rename there is a breaking change for `get_team_snapshot`.
TEAM_GAMES_METRICS = (
    "games_played",
    "wins",
    "win_pct",
    "avg_points_scored",
    "avg_margin",
    "net_points",
)

# MetricFlow qualifies dimensions by the semantic model's *primary entity*, not the model
# name — so the plan's `team_game` entity yields `team_game__team`. Overridable via
# MCP_TEAM_DIMENSION / MCP_VENUE_DIMENSION in case the dbt track renames the entity.
DEFAULT_TEAM_DIMENSION = "team_game__team"
# `venue` resolves to 'home'/'away'. Note this is NOT `home_team`, which holds the
# abbreviation of whichever side hosted and buckets by team rather than by venue.
DEFAULT_VENUE_DIMENSION = "team_game__venue"


def team_filter(dimension: str, abbreviation: str) -> str:
    """MetricFlow where-filter for one team. MF filters are Jinja, not raw SQL."""
    return f"{{{{ Dimension('{dimension}') }}}} = '{abbreviation}'"


class SemanticLayerError(RuntimeError):
    """A metric query was issued but could not be answered."""


class SemanticLayerUnavailable(SemanticLayerError):
    """No semantic layer is loaded (manifest missing, or MetricFlow not installed)."""


@dataclass(frozen=True)
class MetricQueryResult:
    metrics: tuple[str, ...]
    group_by: tuple[str, ...]
    rows: list[dict[str, Any]]
    sql: str | None = None


class SemanticLayer(Protocol):
    """What the tools depend on. Deliberately narrower than MetricFlow's engine."""

    @property
    def available(self) -> bool: ...

    def status(self) -> dict[str, Any]: ...

    def query(
        self,
        *,
        metrics: Sequence[str],
        group_by: Sequence[str] = (),
        where: Sequence[str] = (),
        order_by: Sequence[str] = (),
        limit: int | None = None,
    ) -> MetricQueryResult: ...


@dataclass(frozen=True)
class UnavailableSemanticLayer:
    """Stand-in used until the dbt track's manifest is baked into the image.

    Tools check `available` and fall back to direct `gold` reads rather than failing.
    """

    reason: str

    @property
    def available(self) -> bool:
        return False

    def status(self) -> dict[str, Any]:
        return {"available": False, "reason": self.reason, "metrics": []}

    def query(
        self,
        *,
        metrics: Sequence[str],
        group_by: Sequence[str] = (),
        where: Sequence[str] = (),
        order_by: Sequence[str] = (),
        limit: int | None = None,
    ) -> MetricQueryResult:
        raise SemanticLayerUnavailable(self.reason)


class MetricFlowSemanticLayer:
    """Warm MetricFlow engine built once from the baked semantic manifest.

    The manifest is loaded at construction (startup), not per request: a cold load costs
    hundreds of ms to seconds, which is unacceptable for interactive tool calls.
    """

    def __init__(self, manifest_path: Path, engine: Engine) -> None:
        from metricflow.engine.metricflow_engine import MetricFlowEngine
        from metricflow_semantics.model.dbt_manifest_parser import (
            parse_manifest_from_dbt_generated_manifest,
        )
        from metricflow_semantics.model.semantic_manifest_lookup import SemanticManifestLookup

        self._manifest_path = manifest_path
        manifest = parse_manifest_from_dbt_generated_manifest(
            manifest_json_string=manifest_path.read_text(encoding="utf-8")
        )
        localize_relations(manifest)
        self._sql_client = SqlAlchemySqlClient(engine)
        self._engine = MetricFlowEngine(
            semantic_manifest_lookup=SemanticManifestLookup(manifest),
            sql_client=self._sql_client,
        )

    @property
    def available(self) -> bool:
        return True

    def metric_names(self) -> list[str]:
        return sorted(metric.name for metric in self._engine.list_metrics())

    def status(self) -> dict[str, Any]:
        return {
            "available": True,
            "manifest_path": str(self._manifest_path),
            "metrics": self.metric_names(),
        }

    def query(
        self,
        *,
        metrics: Sequence[str],
        group_by: Sequence[str] = (),
        where: Sequence[str] = (),
        order_by: Sequence[str] = (),
        limit: int | None = None,
    ) -> MetricQueryResult:
        from metricflow.engine.metricflow_engine import MetricFlowQueryRequest

        request = MetricFlowQueryRequest.create(
            metric_names=list(metrics),
            group_by_names=list(group_by) or None,
            where_constraints=list(where) or None,
            order_by_names=list(order_by) or None,
            limit=limit,
        )
        try:
            result = self._engine.query(request)
        except Exception as exc:  # MetricFlow raises a wide range of internal errors
            raise SemanticLayerError(f"metric query failed: {exc}") from exc

        return MetricQueryResult(
            metrics=tuple(metrics),
            group_by=tuple(group_by),
            rows=rows_from_data_table(result.result_df),
            sql=result.sql,
        )


def localize_relations(manifest: Any) -> None:
    """Strip dbt's target database from the manifest's table references.

    dbt bakes its own target database into every `node_relation`, so metrics compile to
    `"jacob_db"."gold"."recent_games_teams"`. Postgres rejects a three-part name unless
    the database part is the one you're connected to, so that qualifier can only ever be
    a no-op or a hard failure (`cross-database references are not implemented`) — never a
    benefit. Dropping it also matches how the rest of this server addresses `gold`:
    schema-qualified, database-agnostic.
    """
    relations = [model.node_relation for model in manifest.semantic_models]
    relations += [spine.node_relation for spine in manifest.project_configuration.time_spines]
    for relation in relations:
        relation.database = None
        relation.relation_name = f'"{relation.schema_name}"."{relation.alias}"'


def rows_from_data_table(data_table: Any) -> list[dict[str, Any]]:
    """Convert a `MetricFlowDataTable` to JSON-ready dicts."""
    if data_table is None:
        return []
    columns = list(data_table.column_names)
    return [
        {column: _jsonify(value) for column, value in zip(columns, row)} for row in data_table.rows
    ]


def _jsonify(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if hasattr(value, "as_integer_ratio"):  # Decimal
        return float(value)
    return str(value)


@dataclass
class SqlAlchemySqlClient:
    """Minimal `metricflow.protocols.sql_client.SqlClient` over our read-only engine.

    Implements only what MetricFlowEngine calls: render the Postgres dialect and execute
    the compiled SQL. Writes are not part of the surface (`execute` exists to satisfy the
    protocol and is refused).
    """

    engine: Engine
    _renderer: Any = field(default=None, init=False, repr=False)

    @property
    def sql_engine_type(self) -> Any:
        from metricflow.protocols.sql_client import SqlEngine

        return SqlEngine.POSTGRES

    @property
    def sql_plan_renderer(self) -> Any:
        if self._renderer is None:
            from metricflow.sql.render.postgres import PostgresSQLSqlPlanRenderer

            self._renderer = PostgresSQLSqlPlanRenderer()
        return self._renderer

    def query(self, stmt: str, sql_bind_parameter_set: Any = None) -> Any:
        from metricflow.data_table.mf_table import MetricFlowDataTable

        with self.engine.connect() as connection:
            result = connection.execute(text(stmt), _bind_params(sql_bind_parameter_set))
            return MetricFlowDataTable.create_from_rows(
                column_names=list(result.keys()),
                rows=[tuple(row) for row in result.fetchall()],
            )

    def execute(self, stmt: str, sql_bind_parameter_set: Any = None) -> None:
        raise SemanticLayerError("the MCP semantic layer is read-only; execute() is not supported")

    def dry_run(self, stmt: str, sql_bind_parameter_set: Any = None) -> None:
        with self.engine.connect() as connection:
            connection.execute(text(f"EXPLAIN {stmt}"), _bind_params(sql_bind_parameter_set))

    def close(self) -> None:
        self.engine.dispose()

    def render_bind_parameter_key(self, bind_parameter_key: str) -> str:
        return f":{bind_parameter_key}"


def _bind_params(sql_bind_parameter_set: Any) -> dict[str, Any]:
    if sql_bind_parameter_set is None:
        return {}
    return dict(sql_bind_parameter_set.param_dict)


def build_semantic_layer(manifest_path: Path | None, engine: Engine) -> SemanticLayer:
    """Load the semantic layer, degrading to `UnavailableSemanticLayer` on any failure.

    A missing manifest or a MetricFlow that won't load must not stop the server from
    booting — the direct-read tools stay useful, and `nba://data-freshness` reports why.
    """
    if manifest_path is None:
        return UnavailableSemanticLayer("MCP_SEMANTIC_MANIFEST_PATH is not set")
    if not manifest_path.exists():
        return UnavailableSemanticLayer(f"semantic manifest not found at {manifest_path}")

    try:
        layer = MetricFlowSemanticLayer(manifest_path=manifest_path, engine=engine)
    except ImportError as exc:
        return UnavailableSemanticLayer(f"metricflow is not installed: {exc}")
    except Exception as exc:
        logger.exception("failed to load semantic manifest from %s", manifest_path)
        return UnavailableSemanticLayer(f"failed to load semantic manifest: {exc}")

    logger.info("semantic layer loaded from %s", manifest_path)
    return layer
