from dash.dash_table import FormatTemplate

recent_games_players_columns = [
    dict(id="rank", name="Rank"),
    dict(id="player", name="Player"),
    dict(id="pts", name="PTS"),
    dict(id="ts_percent", name="TS %"),
    dict(id="plus_minus", name="+/-"),
    dict(id="outcome", name="Outcome"),
    dict(
        id="salary",
        name="Salary",
        type="numeric",
        format=FormatTemplate.money(2),
    ),
]
