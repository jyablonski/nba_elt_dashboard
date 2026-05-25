from dash.dash_table import FormatTemplate

tonights_schedule_columns = [
    dict(id="game_date", name=["", "Date"]),
    dict(id="start_time", name=["", "Start Time (EST)"]),
    dict(id="home_team_odds", name=["", "Home Team"]),
    dict(id="away_team_odds", name=["", "Road Team"]),
    dict(id="avg_team_rank", name=["", "Average Team Rank"]),
    dict(
        id="home_team_predicted_win_pct",
        name=["ML Win Predictions", "Home Win %"],
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(
        id="away_team_predicted_win_pct",
        name=["ML Win Predictions", "Road Win %"],
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
]
