-- Latest timestamps across gold, analogous to the dashboard's /internal/health payload.
select
    (select max(game_date) from recent_games_teams) as latest_game_date,
    (select max(scrape_time) from bans) as latest_scrape_time,
    (select max(game_date) from schedule_tonights_games) as schedule_date,
    (select max(updated_at) from player_salary_value) as salary_updated_at
