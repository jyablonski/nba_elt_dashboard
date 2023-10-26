from dash.dash_table import FormatTemplate

standings_columns = [
    dict(id="rank", name="Rank"),
    dict(id="team_full", name="Team"),
    dict(id="wins", name="Wins"),
    dict(id="losses", name="Losses"),
    dict(id="games_played", name="Games Played"),
    dict(
        id="win_pct", name="Win %", type="numeric", format=FormatTemplate.percentage(1)
    ),
    dict(id="active_injuries", name="Active Injuries"),
    dict(id="last_10", name="Last 10"),
]
