-- Fallback for the `team_games` metrics when the semantic layer is unavailable.
-- Keep these aggregates equivalent to the metric definitions in the dbt project;
-- if they drift, the two paths quietly answer different questions.
select
    count(*) as games_played,
    sum(case when outcome = 'W' then 1 else 0 end) as wins,
    round(avg(case when outcome = 'W' then 1.0 else 0.0 end), 3) as win_pct,
    round(avg(pts_scored), 1) as avg_points_scored,
    round(avg(pts_scored_opp), 1) as avg_points_allowed,
    round(avg(mov), 1) as avg_margin
from recent_games_teams
where team = :abbreviation
