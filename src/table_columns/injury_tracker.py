from dash.dash_table import FormatTemplate

injury_tracker_columns = [
    dict(id="player_logo", name="", presentation="markdown"),
    dict(
        id="player",
        name="",
        presentation="markdown",
    ),
    dict(id="status", name="Status"),
    dict(id="continuous_games_missed", name="Continuous Games Missed"),
    dict(id="avg_ppg", name="Average PPG"),
    dict(
        id="avg_ts_percent",
        name="Average TS%",
        type="numeric",
        format=FormatTemplate.percentage(2),
    ),
    dict(id="avg_plus_minus", name="Average +/-"),
    dict(id="avg_mvp_score", name="MVP Score"),
]
