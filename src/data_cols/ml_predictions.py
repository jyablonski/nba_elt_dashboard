from dash.dash_table import FormatTemplate

ml_predictions_columns = [
    dict(id="proper_date", name="Date"),
    dict(id="start_time", name="Start Time (EST)"),
    dict(id="home_team", name="Home Team"),
    dict(id="away_team", name="Road Team"),
    dict(id="avg_team_rank", name="Average Team Rank"),
    dict(
        id="home_team_predicted_win_pct",
        name="Home Predicted Win %",
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(
        id="away_team_predicted_win_pct",
        name="Road Predicted Win %",
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
]
