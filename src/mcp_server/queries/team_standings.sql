-- One team's standings row: record, conference rank, recent form.
select
    rank,
    team,
    team_full,
    conference,
    wins,
    losses,
    games_played,
    win_pct,
    active_injuries,
    last_10
from standings
where team = :abbreviation
limit 1
