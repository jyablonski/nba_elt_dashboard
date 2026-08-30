-- Home/away split. The CASE below must stay identical to the `venue` dimension's expr
-- in the dbt `team_games` semantic model, or the metric and fallback paths disagree.
select
    case when home_team = team then 'home' else 'away' end as venue,
    count(*) as games_played,
    sum(case when outcome = 'W' then 1 else 0 end) as wins,
    round(avg(case when outcome = 'W' then 1.0 else 0.0 end), 3) as win_pct,
    round(avg(pts_scored), 1) as avg_points_scored,
    round(avg(mov), 1) as avg_margin
from recent_games_teams
where team = :abbreviation
group by
    venue
order by
    venue
