from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from src.mcp_server.semantic import (
    DEFAULT_TEAM_DIMENSION,
    TEAM_GAMES_METRICS,
    SemanticLayerError,
    SemanticLayerUnavailable,
    SqlAlchemySqlClient,
    UnavailableSemanticLayer,
    build_semantic_layer,
    localize_relations,
    rows_from_data_table,
    team_filter,
)


@dataclass
class _FakeDataTable:
    column_names: list
    rows: list


def test_team_filter_renders_metricflow_jinja():
    # MetricFlow where-filters are Jinja over Dimension(), not raw SQL.
    assert team_filter("team_game__team", "BOS") == "{{ Dimension('team_game__team') }} = 'BOS'"


def test_rows_from_data_table_coerces_non_json_types():
    table = _FakeDataTable(
        column_names=["team", "game_date", "win_pct", "missing"],
        rows=[("BOS", date(2024, 1, 2), Decimal("0.625"), None)],
    )

    assert rows_from_data_table(table) == [
        {"team": "BOS", "game_date": "2024-01-02", "win_pct": 0.625, "missing": None}
    ]


def test_rows_from_data_table_handles_no_result():
    assert rows_from_data_table(None) == []


def test_rows_from_data_table_stringifies_unknown_types():
    class _Opaque:
        def __str__(self):
            return "opaque"

    table = _FakeDataTable(column_names=["value"], rows=[(_Opaque(),)])

    assert rows_from_data_table(table) == [{"value": "opaque"}]


def test_unavailable_layer_reports_reason_and_refuses_queries():
    layer = UnavailableSemanticLayer("manifest missing")

    assert layer.available is False
    assert layer.status() == {"available": False, "reason": "manifest missing", "metrics": []}
    with pytest.raises(SemanticLayerUnavailable, match="manifest missing"):
        layer.query(metrics=["win_pct"])


def test_build_semantic_layer_degrades_when_manifest_is_unset():
    layer = build_semantic_layer(None, engine=None)

    assert layer.available is False
    assert "MCP_SEMANTIC_MANIFEST_PATH" in layer.status()["reason"]


def test_build_semantic_layer_degrades_when_manifest_is_missing(tmp_path):
    layer = build_semantic_layer(tmp_path / "nope.json", engine=None)

    assert layer.available is False
    assert "not found" in layer.status()["reason"]


def test_build_semantic_layer_degrades_on_a_corrupt_manifest(tmp_path):
    # A truncated artifact must not stop the server from booting.
    manifest = tmp_path / "semantic_manifest.json"
    manifest.write_text("{not json", encoding="utf-8")

    layer = build_semantic_layer(manifest, engine=None)

    assert layer.available is False
    assert "failed to load semantic manifest" in layer.status()["reason"]


def test_default_team_dimension_is_entity_qualified():
    # MetricFlow qualifies dimensions by primary entity (`team_game`), not model name.
    assert DEFAULT_TEAM_DIMENSION == "team_game__team"


def test_sql_client_refuses_writes():
    client = SqlAlchemySqlClient(engine=None)

    with pytest.raises(SemanticLayerError, match="read-only"):
        client.execute("insert into gold.standings values (1)")


def test_sql_client_reports_postgres_dialect():
    client = SqlAlchemySqlClient(engine=None)

    assert client.sql_engine_type.value == "Postgres"
    assert client.render_bind_parameter_key("team") == ":team"
    # Renderer is built lazily and memoized.
    assert client.sql_plan_renderer is client.sql_plan_renderer


def test_localize_relations_strips_the_dbt_target_database():
    """dbt bakes its own database into node_relation; Postgres can't use it."""

    class _Relation:
        def __init__(self):
            self.alias = "recent_games_teams"
            self.schema_name = "gold"
            self.database = "jacob_db"
            self.relation_name = '"jacob_db"."gold"."recent_games_teams"'

    class _Manifest:
        def __init__(self):
            self.semantic_models = [type("M", (), {"node_relation": _Relation()})()]
            self.project_configuration = type(
                "C", (), {"time_spines": [type("S", (), {"node_relation": _Relation()})()]}
            )()

    manifest = _Manifest()
    localize_relations(manifest)

    for relation in (
        manifest.semantic_models[0].node_relation,
        manifest.project_configuration.time_spines[0].node_relation,
    ):
        assert relation.database is None
        assert relation.relation_name == '"gold"."recent_games_teams"'


def test_pinned_metricflow_loads_the_semantic_manifest_fixture():
    """CI guard for the manifest/version coupling called out in the plan.

    The pinned MetricFlow must be able to parse a dbt-shaped semantic manifest and expose
    the metric names the tools ask for. Loading needs no database — only querying does.
    """
    fixture = Path(__file__).resolve().parents[1] / "fixtures" / "semantic_manifest_fixture.json"

    layer = build_semantic_layer(fixture, engine=None)

    assert layer.available, layer.status().get("reason")
    assert set(TEAM_GAMES_METRICS).issubset(layer.status()["metrics"])


def test_build_semantic_layer_reports_missing_metricflow(monkeypatch, tmp_path):
    manifest = tmp_path / "semantic_manifest.json"
    manifest.write_text("{}", encoding="utf-8")

    def _raise(*args, **kwargs):
        raise ImportError("No module named 'metricflow'")

    monkeypatch.setattr("src.mcp_server.semantic.MetricFlowSemanticLayer", _raise)
    layer = build_semantic_layer(Path(manifest), engine=None)

    assert layer.available is False
    assert "metricflow is not installed" in layer.status()["reason"]
