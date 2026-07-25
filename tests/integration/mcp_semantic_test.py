"""The MetricFlow path, end to end: baked manifest -> compiled SQL -> seeded `gold`."""

import pytest

from src.mcp_server.semantic import TEAM_GAMES_METRICS, SemanticLayerError, team_filter


def test_manifest_exposes_the_team_games_metrics(semantic_layer):
    metrics = semantic_layer.status()["metrics"]

    assert set(TEAM_GAMES_METRICS).issubset(metrics)


def test_metrics_compile_and_run_grouped_by_team(semantic_layer):
    result = semantic_layer.query(metrics=["win_pct", "avg_margin"], group_by=["team_game__team"])

    assert result.rows
    assert set(result.rows[0]) == {"team_game__team", "win_pct", "avg_margin"}
    # The seeded fixture rows are all wins, so every team's win_pct is 1.0.
    assert all(row["win_pct"] == 1.0 for row in result.rows)
    sql = result.sql or ""
    assert '"gold"."recent_games_teams"' in sql
    # The dbt target database must not survive into the SQL: Postgres rejects a
    # three-part name unless it matches the connected database. See localize_relations.
    assert "jacob_db" not in sql


def test_every_snapshot_metric_resolves_for_one_team(semantic_layer):
    result = semantic_layer.query(
        metrics=TEAM_GAMES_METRICS,
        group_by=["team_game__team"],
        where=[team_filter("team_game__team", "BOS")],
        limit=1,
    )

    assert len(result.rows) == 1
    row = result.rows[0]
    assert row["team_game__team"] == "BOS"
    assert set(row) == {"team_game__team", *TEAM_GAMES_METRICS}
    # Ratio (win_pct, avg_margin) and derived (net_points) metrics both resolve, which is
    # the point of routing through the semantic layer rather than hand-written SQL.
    assert row["wins"] == row["games_played"] * row["win_pct"]
    assert row["net_points"] == pytest.approx(row["avg_margin"] * row["games_played"])


def test_time_grain_rollup_uses_the_time_spine(semantic_layer):
    result = semantic_layer.query(
        metrics=["win_pct"],
        group_by=["team_game__team", "metric_time__month"],
        where=[team_filter("team_game__team", "BOS")],
    )

    assert result.rows
    assert "metric_time__month" in result.rows[0]


def test_venue_dimension_splits_home_from_away(semantic_layer):
    """`venue` must bucket by home/away — unlike `home_team`, which buckets by host team."""
    result = semantic_layer.query(
        metrics=["games_played", "avg_points_scored"], group_by=["team_game__venue"]
    )

    assert {row["team_game__venue"] for row in result.rows} == {"home", "away"}


def test_venue_splits_reconcile_with_team_totals(semantic_layer):
    overall = {
        row["team_game__team"]: row["games_played"]
        for row in semantic_layer.query(metrics=["games_played"], group_by=["team_game__team"]).rows
    }
    split = semantic_layer.query(
        metrics=["games_played"], group_by=["team_game__team", "team_game__venue"]
    ).rows

    totals: dict[str, float] = {}
    for row in split:
        totals[row["team_game__team"]] = totals.get(row["team_game__team"], 0) + row["games_played"]

    assert totals == overall


def test_home_team_is_not_a_venue_flag(semantic_layer):
    """Regression guard for the trap that prompted the `venue` dimension."""
    rows = semantic_layer.query(metrics=["games_played"], group_by=["team_game__home_team"]).rows

    values = {row["team_game__home_team"] for row in rows}
    assert values & {"home", "away"} == set()
    assert len(values) > 2


def test_unknown_metric_raises_a_contained_error(semantic_layer):
    # MetricFlow's internal exceptions must not leak past the adapter.
    with pytest.raises(SemanticLayerError, match="metric query failed"):
        semantic_layer.query(metrics=["not_a_metric"], group_by=["team_game__team"])
