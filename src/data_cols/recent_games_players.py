from dash.dash_table import FormatTemplate

recent_games_players_columns = [
    dict(id="player_logo", name="", presentation="markdown"),
    dict(id="player", name="Player"),
    dict(id="pts", name="PTS"),
    dict(
        id="game_ts_percent",
        name="TS %",
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(id="plus_minus", name="+/-"),
    dict(id="outcome", name="Outcome"),
    dict(
        id="salary",
        name="Salary",
        type="numeric",
        format=FormatTemplate.money(0),
    ),
]
