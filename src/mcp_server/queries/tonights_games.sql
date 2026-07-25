-- Tonight's slate with moneylines and model win probabilities.
select
    game_date,
    start_time,
    home_team,
    away_team,
    home_moneyline,
    away_moneyline,
    home_team_predicted_win_pct,
    away_team_predicted_win_pct,
    home_is_great_value,
    away_is_great_value,
    series_round,
    series_status,
    series_game_number
from schedule_tonights_games
order by
    start_time
limit :limit
