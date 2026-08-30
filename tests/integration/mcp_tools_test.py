"""Tools against the seeded `gold` schema — guards the hardcoded table/column assumptions."""

import pytest
from sqlalchemy.exc import DBAPIError

from src.mcp_server import tools
from src.mcp_server.database import fetch_rows


def test_team_snapshot_answers_through_metricflow(mcp_context):
    result = tools.get_team_snapshot(mcp_context, team="celtics")

    assert result["form_source"] == "metricflow"
    assert result["form_error"] is None
    assert result["form"]["win_pct"] == 1.0
    assert result["standings"]["team"] == "BOS"
    assert result["ratings"]["nrtg"] == 6.5
    assert result["recent_games"]
    assert {"game_date", "opponent", "outcome", "venue"} <= set(result["recent_games"][0])


def test_team_snapshot_includes_a_home_away_split(mcp_context):
    result = tools.get_team_snapshot(mcp_context, team="celtics")

    assert result["form_source"] == "metricflow"
    venues = {row["team_game__venue"] for row in result["venue_splits"]}
    assert venues <= {"home", "away"} and venues
    assert (
        sum(row["games_played"] for row in result["venue_splits"])
        == (result["form"]["games_played"])
    )


def test_venue_split_fallback_matches_the_metric_split(mcp_context):
    """The direct-read CASE expression must mirror the dbt `venue` dimension's expr."""
    from dataclasses import replace

    from src.mcp_server.semantic import UnavailableSemanticLayer

    metric_split = tools.get_team_snapshot(mcp_context, team="LAC")["venue_splits"]
    degraded = replace(mcp_context, semantic=UnavailableSemanticLayer("no manifest"))
    gold_split = tools.get_team_snapshot(degraded, team="LAC")["venue_splits"]

    assert {r["team_game__venue"]: r["games_played"] for r in metric_split} == {
        r["venue"]: r["games_played"] for r in gold_split
    }


def test_team_snapshot_supplements_metrics_with_direct_reads(mcp_context):
    result = tools.get_team_snapshot(mcp_context, team="MIA")

    # Blown leads and payroll aren't modeled as metrics yet; they come from `gold`.
    assert any(row["season_type"] == "Playoffs" for row in result["blown_leads"])
    assert result["payroll"] is None or "total_payroll" in result["payroll"]


def test_team_snapshot_falls_back_to_gold_without_a_semantic_layer(mcp_context, mcp_engine):
    """The direct-read fallback must answer the same question the metrics do."""
    from dataclasses import replace

    from src.mcp_server.semantic import UnavailableSemanticLayer

    degraded = replace(mcp_context, semantic=UnavailableSemanticLayer("no manifest"))
    metric_backed = tools.get_team_snapshot(mcp_context, team="BOS")

    result = tools.get_team_snapshot(degraded, team="BOS")

    assert result["form_source"] == "gold_fallback"
    assert result["form_error"] == "no manifest"
    assert result["form"]["games_played"] == metric_backed["form"]["games_played"]
    assert float(result["form"]["win_pct"]) == metric_backed["form"]["win_pct"]
    assert float(result["form"]["avg_margin"]) == metric_backed["form"]["avg_margin"]


def test_team_form_fallback_returns_none_for_a_team_with_no_games(mcp_engine):
    from src.mcp_server.gold_queries import team_form_from_recent_games
    from src.mcp_server.teams import resolve_team

    # `recent_games_teams` is a recent-games window; not every team appears in it.
    assert team_form_from_recent_games(mcp_engine, resolve_team("UTA")) is None


def test_odds_lookup_short_circuits_without_teams(mcp_engine):
    from src.mcp_server.gold_queries import team_odds_outcomes

    assert team_odds_outcomes(mcp_engine, []) == []


def test_team_snapshot_rejects_an_unknown_team(mcp_context):
    with pytest.raises(ValueError, match="did not match"):
        tools.get_team_snapshot(mcp_context, team="Seattle Supersonics")


def test_player_value_ranks_overpaid_before_underpaid(mcp_context):
    overpaid = tools.get_player_value(mcp_context, mode="overpaid", limit=5)
    underpaid = tools.get_player_value(mcp_context, mode="underpaid", limit=5)

    assert len(overpaid["players"]) == 5
    worst = overpaid["players"][0]["value_z_score"]
    best = underpaid["players"][0]["value_z_score"]
    assert worst < best
    # Ascending for overpaid, descending for underpaid.
    assert [p["value_z_score"] for p in overpaid["players"]] == sorted(
        p["value_z_score"] for p in overpaid["players"]
    )


def test_player_value_scoped_to_a_team_includes_payroll(mcp_context):
    result = tools.get_player_value(mcp_context, team="hawks", limit=3)

    assert result["team"]["abbreviation"] == "ATL"
    assert all(player["team"] == "ATL" for player in result["players"])
    assert result["payroll"]["team"] == "ATL"


def test_upcoming_games_returns_tonights_slate_with_win_probabilities(mcp_context):
    result = tools.get_upcoming_games(mcp_context)

    assert result["source_table"] == "schedule_tonights_games"
    assert result["games"]
    game = result["games"][0]
    assert game["home_team_predicted_win_pct"] is not None
    assert game["away_moneyline"] is not None
    assert result["against_the_spread"]


def test_upcoming_games_reads_the_remaining_schedule_for_a_future_date(mcp_context, mcp_engine):
    tomorrow = fetch_rows(mcp_engine, "select (current_date + 1) as day")[0]["day"]

    result = tools.get_upcoming_games(mcp_context, game_date=tomorrow)

    assert result["source_table"] == "schedule_season_remaining"
    assert result["games"]
    assert all(game["game_date"] == tomorrow for game in result["games"])


def test_upcoming_games_respects_the_row_limit(mcp_context):
    assert len(tools.get_upcoming_games(mcp_context, limit=2)["games"]) == 2


def test_data_freshness_reports_gold_and_semantic_status(mcp_context):
    result = tools.get_data_freshness(mcp_context)

    assert result["gold"]["latest_game_date"]
    assert result["semantic_layer"]["available"] is True


def test_the_mcp_engine_refuses_writes(mcp_engine):
    # Belt-and-braces alongside the read-only role the service connects as in prod.
    with pytest.raises(DBAPIError, match="read-only"):
        fetch_rows(mcp_engine, "create table gold.mcp_write_probe (id int)")
