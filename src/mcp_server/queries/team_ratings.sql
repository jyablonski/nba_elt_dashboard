-- Offensive / defensive / net rating with their league ranks.
select
    team,
    team_acronym,
    wins,
    losses,
    ortg,
    ortg_rank,
    drtg,
    drtg_rank,
    nrtg,
    nrtg_rank
from team_ratings
where team_acronym = :abbreviation
limit 1
