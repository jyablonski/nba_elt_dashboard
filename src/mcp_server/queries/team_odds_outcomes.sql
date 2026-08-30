-- Against-the-spread coverage rates for the teams in a slate.
select
    team,
    season_type,
    games_played,
    pct_covered_spread,
    pct_favorite_covered,
    pct_underdog_covered
from team_odds_outcomes
where team = any(:teams)
limit 60
