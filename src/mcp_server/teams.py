from __future__ import annotations

from dataclasses import dataclass

from src.data_access.tables import team_name_to_abbreviation, team_names

# The gold tables are inconsistent about which team identifier they carry: `standings`,
# `player_salary_value` and `team_blown_leads` use the abbreviation, while `team_ratings`
# and the schedule tables use the full name. Tools resolve once, up front, and then use
# whichever form the table wants.


@dataclass(frozen=True)
class Team:
    abbreviation: str
    full_name: str


class UnknownTeamError(ValueError):
    """The caller's team string matched zero or more than one team."""


TEAMS: tuple[Team, ...] = tuple(
    Team(abbreviation=team_name_to_abbreviation[name], full_name=name) for name in team_names
)

_BY_ABBREVIATION = {team.abbreviation.lower(): team for team in TEAMS}
_BY_FULL_NAME = {team.full_name.lower(): team for team in TEAMS}


def resolve_team(query: str) -> Team:
    """Map a loose team reference ("lakers", "LAL", "Los Angeles Lakers") to one team.

    LLM callers pass whatever the user typed, so nickname-only input is the common case.
    An ambiguous prefix ("Los Angeles") raises rather than guessing.
    """
    normalized = " ".join(query.strip().lower().split())
    if not normalized:
        raise UnknownTeamError("no team was provided")

    if normalized in _BY_ABBREVIATION:
        return _BY_ABBREVIATION[normalized]
    if normalized in _BY_FULL_NAME:
        return _BY_FULL_NAME[normalized]

    # Nickname match ("celtics", "76ers"), then a looser substring pass that catches
    # multi-word nicknames ("trail blazers") and cities ("brooklyn").
    matches = [team for team in TEAMS if team.full_name.lower().split()[-1] == normalized]
    if not matches:
        matches = [team for team in TEAMS if normalized in team.full_name.lower()]

    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        options = ", ".join(team.full_name for team in matches)
        raise UnknownTeamError(f"'{query}' is ambiguous; did you mean one of: {options}?")
    raise UnknownTeamError(f"'{query}' did not match an NBA team")


def team_directory() -> list[dict[str, str]]:
    """Payload for the `nba://teams` resource."""
    return [{"abbreviation": team.abbreviation, "name": team.full_name} for team in TEAMS]
