from dash.dash_table import FormatTemplate

injury_tracker_columns = [
    dict(id="player", name="Player"),
    dict(id="status", name="Status"),
    dict(id="continuous_games_missed", name="Continuous Games Missed"),
    dict(id="average_ppg", name="Average PPG"),
    dict(
        id="average_ts",
        name="Average TS%",
        type="numeric",
        format=FormatTemplate.percentage(2),
    ),
    dict(id="average_plus_minus", name="Average +/-"),
    dict(id="avg_mvp_score", name="MVP Score"),
]
