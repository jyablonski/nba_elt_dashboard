-- Most recent games for one team, newest first.
select
    game_date,
    team,
    opponent,
    outcome,
    pts_scored,
    pts_scored_opp,
    mov,
    case when home_team = team then 'home' else 'away' end as venue,
    series_round
from recent_games_teams
where team = :abbreviation
order by
    game_date desc
limit :limit
