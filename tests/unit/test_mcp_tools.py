from datetime import date

import pytest

from src.mcp_server import gold_queries, tools
from src.mcp_server.semantic import MetricQueryResult, SemanticLayerError, UnavailableSemanticLayer
from src.mcp_server.settings import Settings
from src.mcp_server.tools import ServerContext


class _StubSemanticLayer:
    def __init__(self, rows=None, error=None):
        self._rows = rows or []
        self._error = error
        self.calls = []

    @property
    def available(self):
        return True

    def status(self):
        return {"available": True, "metrics": ["win_pct"]}

    def query(self, *, metrics, group_by=(), where=(), order_by=(), limit=None):
        self.calls.append(
            {"metrics": tuple(metrics), "group_by": tuple(group_by), "where": tuple(where)}
        )
        if self._error is not None:
            raise self._error
        return MetricQueryResult(
            metrics=tuple(metrics), group_by=tuple(group_by), rows=self._rows, sql="select 1"
        )


def _settings(**overrides):
    defaults = dict(
        auth_token="token",
        host="0.0.0.0",
        port=9100,
        semantic_manifest_path=None,
        max_rows=10,
        config_path="config.yaml",
        env_type="dev",
        team_dimension="team_game__team",
        venue_dimension="team_game__venue",
        allowed_hosts=(),
        allowed_origins=(),
    )
    defaults.update(overrides)
    return Settings(**defaults)


def _context(semantic):
    return ServerContext(engine=object(), semantic=semantic, settings=_settings())


@pytest.fixture
def stub_gold(monkeypatch):
    """Stub every direct `gold` read so tool shaping is testable without a database."""
    calls = {}

    def record(name, value):
        def _stub(*args, **kwargs):
            calls[name] = (args, kwargs)
            return value

        monkeypatch.setattr(gold_queries, name, _stub)

    record("team_standings", {"rank": "1st", "wins": 57})
    record("team_ratings", {"nrtg": 6.5})
    record("team_blown_leads", [{"season_type": "Regular Season"}])
    record("team_payroll", {"total_payroll": 1})
    record("team_recent_games", [{"outcome": "W"}])
    record("team_form_from_recent_games", {"games_played": 4, "win_pct": 0.75})
    record(
        "team_form_by_venue",
        [{"venue": "home", "win_pct": 1.0}, {"venue": "away", "win_pct": 0.5}],
    )
    record("player_value", [{"player_name": "Test Player"}])
    record("tonights_games", [{"home_team": "Boston Celtics", "away_team": "Miami Heat"}])
    record("scheduled_games", [{"home_team": "Chicago Bulls", "away_team": "Toronto Raptors"}])
    record("team_odds_outcomes", [{"team": "BOS"}])
    record("data_freshness", {"latest_game_date": "2024-04-01"})
    return calls


def test_team_snapshot_prefers_the_semantic_layer(stub_gold):
    semantic = _StubSemanticLayer(rows=[{"team_game__team": "BOS", "win_pct": 0.7}])

    result = tools.get_team_snapshot(_context(semantic), team="celtics")

    assert result["team"] == {"abbreviation": "BOS", "name": "Boston Celtics"}
    assert result["form"] == {"team_game__team": "BOS", "win_pct": 0.7}
    assert result["form_source"] == "metricflow"
    assert result["form_error"] is None
    assert semantic.calls[0]["where"] == ("{{ Dimension('team_game__team') }} = 'BOS'",)


def test_team_snapshot_falls_back_to_gold_when_the_layer_is_unavailable(stub_gold):
    semantic = UnavailableSemanticLayer("manifest missing")

    result = tools.get_team_snapshot(_context(semantic), team="BOS")

    assert result["form"] == {"games_played": 4, "win_pct": 0.75}
    assert result["form_source"] == "gold_fallback"
    assert result["form_error"] == "manifest missing"


def test_team_snapshot_falls_back_when_a_metric_query_fails(stub_gold):
    semantic = _StubSemanticLayer(error=SemanticLayerError("unknown metric win_pct"))

    result = tools.get_team_snapshot(_context(semantic), team="BOS")

    # A broken metric shouldn't sink the whole snapshot.
    assert result["form_source"] == "gold_fallback"
    assert "unknown metric" in result["form_error"]
    assert result["standings"] == {"rank": "1st", "wins": 57}


def test_team_snapshot_reports_an_empty_metric_result(stub_gold):
    result = tools.get_team_snapshot(_context(_StubSemanticLayer(rows=[])), team="BOS")

    assert result["form"] is None
    assert result["form_error"] == "no metric rows for this team"


def test_venue_split_follows_the_metric_path(stub_gold):
    semantic = _StubSemanticLayer(rows=[{"team_game__venue": "home", "win_pct": 1.0}])

    result = tools.get_team_snapshot(_context(semantic), team="BOS")

    assert result["venue_splits"] == [{"team_game__venue": "home", "win_pct": 1.0}]
    # Grouped by venue, still filtered to the one team.
    split_call = semantic.calls[1]
    assert split_call["group_by"] == ("team_game__venue",)
    assert split_call["where"] == ("{{ Dimension('team_game__team') }} = 'BOS'",)


def test_venue_split_falls_back_to_gold_with_the_headline_numbers(stub_gold):
    # Splits must not come from a different source than `form` — that would mix
    # metric-derived and SQL-derived numbers in one payload.
    result = tools.get_team_snapshot(_context(UnavailableSemanticLayer("no manifest")), team="BOS")

    assert result["form_source"] == "gold_fallback"
    assert result["venue_splits"] == [
        {"venue": "home", "win_pct": 1.0},
        {"venue": "away", "win_pct": 0.5},
    ]


def test_venue_split_falls_back_when_only_the_split_query_fails(monkeypatch, stub_gold):
    semantic = _StubSemanticLayer(rows=[{"team_game__team": "BOS", "win_pct": 0.7}])
    calls = {"n": 0}
    original = semantic.query

    def flaky(**kwargs):
        calls["n"] += 1
        if calls["n"] > 1:  # headline query succeeds, venue split blows up
            raise SemanticLayerError("unknown dimension team_game__venue")
        return original(**kwargs)

    monkeypatch.setattr(semantic, "query", flaky)
    result = tools.get_team_snapshot(_context(semantic), team="BOS")

    assert result["form_source"] == "metricflow"
    assert result["venue_splits"][0]["venue"] == "home"


def test_player_value_rejects_an_unknown_mode(stub_gold):
    with pytest.raises(ValueError, match="overpaid"):
        tools.get_player_value(_context(_StubSemanticLayer()), mode="cheapest")


def test_player_value_clamps_the_limit_and_orders_by_mode(stub_gold):
    context = _context(_StubSemanticLayer())

    result = tools.get_player_value(context, team="suns", mode="underpaid", limit=9999)

    _, kwargs = stub_gold["player_value"]
    assert kwargs["overpaid"] is False
    assert kwargs["limit"] == 200  # ROW_LIMIT_CEILING
    assert result["team"] == {"abbreviation": "PHX", "name": "Phoenix Suns"}
    assert result["players"] == [{"player_name": "Test Player"}]


def test_player_value_league_wide_skips_team_lookups(stub_gold):
    result = tools.get_player_value(_context(_StubSemanticLayer()))

    assert result["team"] is None
    assert result["payroll"] is None
    assert "team_payroll" not in stub_gold


def test_upcoming_games_defaults_to_tonight(stub_gold):
    result = tools.get_upcoming_games(_context(_StubSemanticLayer()))

    assert result["date"] == date.today().isoformat()
    assert result["source_table"] == "schedule_tonights_games"
    # Team names in the schedule are resolved to abbreviations for the spread lookup.
    assert stub_gold["team_odds_outcomes"][0][1] == ["BOS", "MIA"]


def test_upcoming_games_uses_the_remaining_schedule_for_a_future_date(stub_gold):
    result = tools.get_upcoming_games(_context(_StubSemanticLayer()), game_date="2030-01-15")

    assert result["date"] == "2030-01-15"
    assert result["source_table"] == "schedule_season_remaining"


def test_upcoming_games_rejects_a_malformed_date(stub_gold):
    with pytest.raises(ValueError, match="ISO format"):
        tools.get_upcoming_games(_context(_StubSemanticLayer()), game_date="tomorrow")


def test_upcoming_games_skips_unresolvable_team_names(monkeypatch, stub_gold):
    # Schedule rows carry free-text team names; a rename upstream must not break the tool.
    monkeypatch.setattr(
        gold_queries,
        "tonights_games",
        lambda *args, **kwargs: [
            {"home_team": "Boston Celtics", "away_team": "Seattle Supersonics"},
            {"home_team": None, "away_team": "Miami Heat"},
        ],
    )
    captured = {}
    monkeypatch.setattr(
        gold_queries,
        "team_odds_outcomes",
        lambda engine, teams: captured.setdefault("teams", teams),
    )

    tools.get_upcoming_games(_context(_StubSemanticLayer()))

    assert captured["teams"] == ["BOS", "MIA"]


def test_data_freshness_includes_semantic_layer_status(stub_gold):
    result = tools.get_data_freshness(_context(UnavailableSemanticLayer("no manifest")))

    assert result["gold"] == {"latest_game_date": "2024-04-01"}
    assert result["semantic_layer"]["reason"] == "no manifest"


def test_get_teams_lists_all_thirty():
    assert len(tools.get_teams()) == 30
