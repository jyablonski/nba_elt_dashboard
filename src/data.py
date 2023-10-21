from src.database import get_data, engine

source_tables = [
    # "bans",
    # "contract_value_analysis",
    # "feature_flags",
    # "game_types",
    # "injuries",
    # "injury_tracker",
    # "mov",
    # "opp_stats",
    # "pbp",
    # "preseason_odds",
    # "recent_games_players",
    # "recent_games_teams",
    # "reddit_comments",
    # "reddit_sentiment_time_series",
    # "rolling_avg_stats",
    # "schedule",
    # "scorers",
    # "social_media_stats",
    "standings",
    # "team_record_daily_rollup",
    # "team_adv_stats",
    # "team_blown_leads",
    # "team_contracts_analysis",
    # "team_ratings",
    # "transactions",
    # "twitter_comments",
    # "ml_models.tonights_games_ml",
]


print("STARTING WEB SCRAPE")

with engine.begin() as connection:
    for table in source_tables:
        if table == "x":
            pass
        else:
            globals()[f"{table}_df"] = get_data(table_name=table, conn=connection)
