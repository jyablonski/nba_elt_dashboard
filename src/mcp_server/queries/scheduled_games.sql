-- Games on a future date, from the remaining-season schedule.
select
    game_date,
    day_name,
    start_time,
    home_team,
    away_team,
    home_moneyline_raw as home_moneyline,
    away_moneyline_raw as away_moneyline,
    series_round,
    series_game_number
from schedule_season_remaining
where game_date = cast(:game_date as date)
order by
    start_time
limit :limit
