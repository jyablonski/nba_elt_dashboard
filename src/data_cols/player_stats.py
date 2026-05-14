from dash.dash_table import FormatTemplate
from dash.dash_table.Format import Format, Scheme

player_stats_columns = [
    dict(id="player", name="Player"),
    dict(id="team", name="Team"),
    dict(id="avg_ppg", name="Average PPG"),
    dict(id="avg_ts_percent", name="TS %"),
    dict(id="is_mvp_candidate", name=""),
]

player_scoring_efficiency_columns = [
    dict(id="player", name="Player"),
    dict(id="team", name="Team"),
    dict(
        id="avg_ppg",
        name="PPG",
        type="numeric",
        format=Format(precision=1, scheme=Scheme.fixed),
    ),
    dict(
        id="avg_ts_percent",
        name="True shooting %",
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(id="games_played", name="Games", type="numeric"),
    dict(id="is_mvp_candidate", name="Player type"),
    dict(
        id="ts_vs_reg_pp",
        name="vs reg. season TS avg (pp)",
        type="numeric",
        format=Format(precision=1, scheme=Scheme.fixed),
    ),
]
