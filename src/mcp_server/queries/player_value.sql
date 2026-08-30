-- Production-vs-pay ranking. `value_z_score` is production z-score minus salary
-- z-score, so ascending = most overpaid, descending = best surplus value.
--
-- Both the optional team filter and the sort direction are parameters rather than
-- interpolated SQL: pass :abbreviation as null to rank league-wide, and :direction as
-- 1 for overpaid (ascending) or -1 for underpaid (descending).
select
    player_name,
    team,
    position,
    age,
    season,
    salary_usd,
    avg_mvp_score,
    mvp_z_score,
    salary_z_score,
    value_z_score,
    pct_of_team_production,
    production_minus_salary_pct,
    value_tier,
    is_overpaid,
    salary_rank
from player_salary_value
where value_z_score is not null
    and (:abbreviation is null or team = :abbreviation)
order by
    value_z_score * :direction
limit :limit
