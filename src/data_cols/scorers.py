scorers_playoffs_columns = [
    dict(id="player", name="Player"),
    dict(id="team", name="Team"),
    dict(id="playoffs_avg_ppg", name="Average PPG"),
    dict(id="playoffs_ts_percent", name="TS %"),
    dict(id="top5_candidates", name=""),
]

scorers_regular_season_columns = [
    dict(id="player", name="Player"),
    dict(id="team", name="Team"),
    dict(id="season_avg_ppg", name="Average PPG"),
    dict(id="season_ts_percent", name="TS %"),
    dict(id="top5_candidates", name=""),
]

# DROP TABLE IF EXISTS scorers;
# CREATE TABLE scorers(
#     player text,
#     team text,
#     full_team text,
#     season_avg_ppg numeric,
#     playoffs_avg_ppg numeric,
#     season_ts_percent numeric,
#     playoffs_ts_percent numeric,
#     games_played bigint,
#     playoffs_games_played bigint,
#     ppg_rank bigint,
#     top20_scorers text,
#     player_mvp_calc_adj numeric,
#     games_missed bigint,
#     penalized_games_missed numeric,
#     top5_candidates text,
#     mvp_rank bigint
# );
