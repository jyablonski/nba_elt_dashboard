from src.database import get_data, engine

team_names = [
    "Atlanta Hawks",
    "Boston Celtics",
    "Brooklyn Nets",
    "Charlotte Hornets",
    "Chicago Bulls",
    "Cleveland Cavaliers",
    "Dallas Mavericks",
    "Denver Nuggets",
    "Detroit Pistons",
    "Golden State Warriors",
    "Houston Rockets",
    "Indiana Pacers",
    "Los Angeles Clippers",
    "Los Angeles Lakers",
    "Memphis Grizzlies",
    "Miami Heat",
    "Milwaukee Bucks",
    "Minnesota Timberwolves",
    "New Orleans Pelicans",
    "New York Knicks",
    "Oklahoma City Thunder",
    "Orlando Magic",
    "Philadelphia 76ers",
    "Phoenix Suns",
    "Portland Trail Blazers",
    "Sacramento Kings",
    "San Antonio Spurs",
    "Toronto Raptors",
    "Utah Jazz",
    "Washington Wizards",
]

team_names_abbreviations = [
    "ATL",
    "BOS",
    "BKN",
    "CHA",
    "CHI",
    "CLE",
    "DAL",
    "DEN",
    "DET",
    "GSW",
    "HOU",
    "IND",
    "LAC",
    "LAL",
    "MEM",
    "MIA",
    "MIL",
    "MIN",
    "NOP",
    "NYK",
    "OKC",
    "ORL",
    "PHI",
    "PHX",
    "POR",
    "SAC",
    "SAS",
    "TOR",
    "UTA",
    "WAS",
]

source_tables = [
    "bans",
    "contract_value_analysis",
    "feature_flags",
    "game_types",
    "injuries",
    "injury_tracker",
    "mov",
    "opp_stats",
    "past_schedule_analysis",
    "pbp",
    "player_stats",
    "preseason_odds",
    "recent_games_players",
    "recent_games_teams",
    "reddit_comments",
    "reddit_sentiment_time_series",
    "rolling_avg_stats",
    "schedule_season_remaining",
    "social_media_aggs",
    "standings",
    "team_record_daily_rollup",
    "team_adv_stats",
    "team_blown_leads",
    "team_contracts_analysis",
    "team_ratings",
    "transactions",
    "twitter_comments",
    "ml_models.schedule_tonights_games",
    "ml_models.tonights_games_ml",
]

with engine.begin() as connection:
    for table in source_tables:
        if "." in table:
            table_name = table.split(".")[1]
            globals()[f"{table_name}_df"] = get_data(table_name=table, conn=connection)
        elif table == "reddit_sentiment_time_series":
            globals()[f"{table}_df"] = get_data(
                table_name=table, conn=connection, limit_amount=10000000
            )
        else:
            globals()[f"{table}_df"] = get_data(table_name=table, conn=connection)
