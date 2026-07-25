import pytest

from src.mcp_server.teams import TEAMS, UnknownTeamError, resolve_team, team_directory


@pytest.mark.parametrize(
    "query,expected",
    [
        ("LAL", "Los Angeles Lakers"),
        ("lal", "Los Angeles Lakers"),
        ("lakers", "Los Angeles Lakers"),
        ("Boston Celtics", "Boston Celtics"),
        ("  celtics  ", "Boston Celtics"),
        ("76ers", "Philadelphia 76ers"),
        ("trail blazers", "Portland Trail Blazers"),
        ("blazers", "Portland Trail Blazers"),
        ("brooklyn", "Brooklyn Nets"),
        ("new york", "New York Knicks"),
    ],
)
def test_resolve_team_accepts_loose_references(query, expected):
    assert resolve_team(query).full_name == expected


def test_resolve_team_rejects_ambiguous_city():
    with pytest.raises(UnknownTeamError, match="ambiguous"):
        resolve_team("los angeles")


def test_resolve_team_rejects_unknown_and_empty():
    with pytest.raises(UnknownTeamError, match="did not match"):
        resolve_team("Seattle Supersonics")
    with pytest.raises(UnknownTeamError, match="no team"):
        resolve_team("   ")


def test_team_directory_covers_every_team():
    directory = team_directory()
    assert len(directory) == len(TEAMS) == 30
    assert {"abbreviation": "BOS", "name": "Boston Celtics"} in directory
