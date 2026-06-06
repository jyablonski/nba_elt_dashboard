import json
import math
from datetime import datetime

import pandas as pd
import plotly.express as px
from dash import callback, callback_context, dcc, html
from dash.dash_table import FormatTemplate
from dash.dependencies import ALL, Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from src.data_access.cache import get_table
from src.recent_games_helpers import build_game_card_specs, pbp_flow_stats
from src.shell import playoffs_enabled
from src.theme.plotly import TRACE_HOVERLABEL, apply_dark_layout
from src.ui.tables import dark_datatable
from src.utils import pbp_transformer

PERFORMANCE_COLORS = {
    1: "#9362DA",
    2: "#3fb7d9",
    3: "#e04848",
}

RECENT_PLAYERS_SIMPLE_COLUMNS = [
    dict(id="team", name="Tm"),
    dict(id="player", name="Player"),
    dict(id="pts", name="PTS"),
    dict(
        id="game_ts_percent",
        name="TS%",
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(id="plus_minus", name="+/-"),
    dict(id="outcome", name="W/L"),
]


def _pbp_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pbp_df = get_table("pbp")
    pbp_plot_kpis, pbp_plot_df = pbp_transformer(pbp_df)
    return pbp_df, pbp_plot_kpis, pbp_plot_df


def _game_card_specs():
    return build_game_card_specs(get_table("pbp"), get_table("recent_games_teams"))


def _game_options() -> tuple[list[dict], str | None]:
    pbp_df = get_table("pbp")
    yesterdays_games = pbp_df["game_description"].drop_duplicates()
    options = [{"label": game, "value": game} for game in yesterdays_games]
    default_sel = yesterdays_games.iloc[0] if len(yesterdays_games) > 0 else None
    return options, default_sel


def _slate_date_label() -> str:
    pbp_df = get_table("pbp")
    if pbp_df is None or pbp_df.empty or "game_date" not in pbp_df.columns:
        return datetime.now().strftime("%a, %b %d, %Y")
    d = pd.Timestamp(pbp_df["game_date"].max())
    return d.strftime("%a, %b %d, %Y")


def _pbp_chart_subtitle() -> str:
    return "Pick a game below to view play-by-play."


def _slate_summary_bar() -> html.Div:
    """Single compact strip: slate volume without tall KPI cards."""
    pbp_df, _pbp_plot_kpis, pbp_plot_df = _pbp_data()
    yesterdays_games = pbp_df["game_description"].drop_duplicates()
    plays_parsed = len(pbp_plot_df) if pbp_plot_df is not None else 0
    games_last_night = int(yesterdays_games.shape[0])
    return html.Div(
        html.Div(
            [
                html.Span(
                    f"{games_last_night} games on slate",
                    className="recent-games-slate-chip recent-games-slate-chip--accent",
                ),
                html.Span(f"{plays_parsed:,} plays in feed", className="recent-games-slate-chip"),
            ],
            className="recent-games-slate-bar-inner",
        ),
        className="recent-games-slate-bar mb-3",
    )


def _pbp_stat_tile(label: str, value: object) -> html.Div:
    return html.Div(
        [
            html.Div(label, className="recent-games-pbp-stat-lbl"),
            html.Div(str(value), className="recent-games-pbp-stat-val"),
        ],
        className="recent-games-pbp-stat-tile",
    )


def _parse_hex_rgb(hex_s: str) -> tuple[int, int, int] | None:
    h = (hex_s or "").strip().lstrip("#")
    if len(h) != 6 or any(c not in "0123456789abcdefABCDEF" for c in h):
        return None
    try:
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return None


def _hex_tint_rgba(hex_s: str, alpha: float = 0.16) -> str | None:
    rgb = _parse_hex_rgb(hex_s)
    if not rgb:
        return None
    return f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})"


def _pbp_legend_dot(is_home: bool, team_hex: str) -> html.Span:
    """Marker color in the chart follows scoring_team_color; legend dot matches team primary when available."""
    base = "recent-games-legend-dot"
    if _parse_hex_rgb(team_hex):
        return html.Span(className=base, style={"backgroundColor": team_hex})
    suffix = "recent-games-legend-dot--home" if is_home else "recent-games-legend-dot--away"
    return html.Span(className=f"{base} {suffix}")


def _fmt_lead_pct(raw: object) -> str:
    if raw is None:
        return "-"
    try:
        if pd.isna(raw):
            return "-"
        return f"{float(raw):.0%}"
    except TypeError, ValueError:
        return "-"


def _result_line(game_desc: str, home_abbr: str, away_abbr: str) -> tuple[html.Div | str, dict]:
    spec = next((s for s in _game_card_specs() if s.game_description == game_desc), None)
    if spec is None:
        return "", {}

    away_win = spec.winner_abbr == away_abbr
    home_win = spec.winner_abbr == home_abbr
    winner_abbr = spec.winner_abbr or (home_abbr if spec.home_pts > spec.away_pts else away_abbr)
    final_tag = "Final"

    result = html.Div(
        [
            html.Span(
                f"{away_abbr} {spec.away_pts}",
                className="recent-games-pbp-result-team"
                + (" recent-games-pbp-result-team--win" if away_win else ""),
            ),
            html.Span(",", className="recent-games-pbp-result-sep"),
            html.Span(
                f"{home_abbr} {spec.home_pts}",
                className="recent-games-pbp-result-team"
                + (" recent-games-pbp-result-team--win" if home_win else ""),
            ),
            html.Span(f"· {final_tag}", className="recent-games-pbp-result-meta"),
        ],
        className="recent-games-pbp-result-line",
    )
    return result, {
        "winner": winner_abbr,
        "away_pts": spec.away_pts,
        "home_pts": spec.home_pts,
        "final_tag": final_tag,
    }


def _flow_legend_and_stats(game_desc: str | None) -> tuple[html.Div | str, dict]:
    """Centered heading above the margin chart: away @ home title, chart legend, inline stats."""
    pbp_df, pbp_plot_kpis, pbp_plot_df = _pbp_data()
    if not game_desc or pbp_df is None or pbp_df.empty:
        return "", {}
    sub = pbp_df[pbp_df["game_description"] == game_desc]
    if sub.empty:
        return "", {}
    r0 = sub.iloc[0]
    home_fill = str(r0.get("home_fill", "Home"))
    away_fill = str(r0.get("away_fill", "Away"))
    away_abbr = str(r0.get("away_team", ""))
    home_abbr = str(r0.get("home_team", ""))
    home_hex = str(r0.get("home_primary_color") or "").strip()
    away_hex = str(r0.get("away_primary_color") or "").strip()
    away_full = str(r0.get("away_team_full") or "").strip()
    home_full = str(r0.get("home_team_full") or "").strip()
    if away_full and home_full:
        title_line = f"{away_full} @ {home_full}"
    elif away_abbr and home_abbr:
        title_line = f"{away_abbr} @ {home_abbr}"
    else:
        title_line = (
            str(game_desc).replace(" Vs. ", " @ ").replace(" vs. ", " @ ").replace(" vs ", " @ ")
        )

    st = pbp_flow_stats(pbp_plot_df[pbp_plot_df["game_description"] == game_desc])
    kpi_row = pbp_plot_kpis[pbp_plot_kpis["game_description"] == game_desc]
    if kpi_row.empty:
        home_lead_pct = "-"
        away_lead_pct = "-"
        tie_pct = "-"
    else:
        k0 = kpi_row.iloc[0]
        home_lead_pct = _fmt_lead_pct(k0.get("home_pct_leading"))
        away_lead_pct = _fmt_lead_pct(k0.get("away_pct_leading"))
        tie_pct = _fmt_lead_pct(k0.get("tie_pct"))

    stats_bits: list = [
        html.Span(f"Max lead ±{st['max_lead']}", className="recent-games-pbp-heading-kv"),
        html.Span(f"{st['lead_changes']} lead changes", className="recent-games-pbp-heading-kv"),
        html.Span(f"{st['ties']} ties", className="recent-games-pbp-heading-kv"),
        html.Span(f"{st['plays']} plays", className="recent-games-pbp-heading-kv"),
    ]

    home_lbl = f"Home ({home_abbr})" if home_abbr else "Home"
    away_lbl = f"Away ({away_abbr})" if away_abbr else "Away"
    home_bg = _hex_tint_rgba(home_hex)
    away_bg = _hex_tint_rgba(away_hex)
    home_chip_style = {"backgroundColor": home_bg} if home_bg else None
    away_chip_style = {"backgroundColor": away_bg} if away_bg else None
    result_line, result_meta = _result_line(game_desc, home_abbr, away_abbr)
    spec = next((s for s in _game_card_specs() if s.game_description == game_desc), None)
    series_line = (
        _series_chip(spec.series_round, spec.series_status, playoffs_enabled())
        if spec is not None
        else ""
    )

    legend = html.Div(
        [
            html.Div(
                [
                    html.Span(title_line, className="recent-games-pbp-heading-matchup"),
                    series_line,
                    result_line,
                ],
                className="recent-games-pbp-heading-titles",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                [
                                    _pbp_legend_dot(True, home_hex),
                                    html.Span(home_lbl, className="ms-1"),
                                    html.Span(
                                        f"Led {home_lead_pct} of game",
                                        className="recent-games-lead-pct",
                                    ),
                                ],
                                className="recent-games-margin-chip recent-games-margin-chip--home",
                                style=home_chip_style,
                            ),
                            html.Span(
                                [
                                    _pbp_legend_dot(False, away_hex),
                                    html.Span(away_lbl, className="ms-1"),
                                    html.Span(
                                        f"Led {away_lead_pct} of game",
                                        className="recent-games-lead-pct",
                                    ),
                                ],
                                className="recent-games-margin-chip recent-games-margin-chip--away",
                                style=away_chip_style,
                            ),
                        ],
                        className="recent-games-pbp-heading-legend",
                        title=(
                            "Legend for the score chart below: each point is colored by the team that "
                            "scored on that play (home vs away). Lead percentages are clock time spent "
                            f"ahead; tied time was {tie_pct}."
                        ),
                    ),
                    html.Div(stats_bits, className="recent-games-pbp-heading-stats"),
                ],
                className="recent-games-pbp-heading-row",
            ),
        ],
        className="recent-games-pbp-heading",
    )
    return legend, {
        "home": home_fill,
        "away": away_fill,
        "home_pct_leading": home_lead_pct,
        "away_pct_leading": away_lead_pct,
        "tie_pct": tie_pct,
        **result_meta,
        **st,
    }


def _series_chip(
    series_round: str | None, series_status: str | None, playoffs_active: bool
) -> html.Div | str:
    """Playoff series pill, e.g. 'NBA Finals · MIA leads 2-0'.

    Gated on the ``playoffs`` feature flag (authoritative) plus row-level series data,
    so a stale series_status in a mart can't surface during the regular season.
    """
    if not playoffs_active or not series_status:
        return ""
    bits = [series_round, series_status] if series_round else [series_status]
    return html.Div(
        " · ".join(bits),
        className="recent-games-card-series",
    )


def render_game_cards(selected: str | None) -> html.Div:
    game_card_specs = _game_card_specs()
    if not game_card_specs:
        return html.Div("No games in PBP feed.", className="text-muted small")
    playoffs_active = playoffs_enabled()
    n = len(game_card_specs)
    row_cls = "recent-games-card-row recent-games-card-row--scroll"
    if n <= 8:
        row_cls = "recent-games-card-row recent-games-card-row--wrap"
    cells = []
    for spec in game_card_specs:
        sel = spec.game_description == selected
        away_win = spec.winner_abbr == spec.away_abbr
        home_win = spec.winner_abbr == spec.home_abbr
        cells.append(
            html.Div(
                [
                    html.Div(
                        html.Span(
                            f"{spec.away_abbr} @ {spec.home_abbr}",
                            className="recent-games-card-matchup",
                        ),
                        className="recent-games-card-top",
                    ),
                    _series_chip(spec.series_round, spec.series_status, playoffs_active),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(
                                        src=f"assets/{spec.away_logo}",
                                        className="recent-games-card-logo",
                                        alt=spec.away_abbr,
                                    ),
                                    html.Span(spec.away_abbr, className="recent-games-card-abbr"),
                                    html.Span(
                                        str(spec.away_pts),
                                        className="recent-games-card-score"
                                        + (" recent-games-card-score--win" if away_win else ""),
                                    ),
                                ],
                                className="recent-games-card-side",
                            ),
                            html.Div(
                                [
                                    html.Img(
                                        src=f"assets/{spec.home_logo}",
                                        className="recent-games-card-logo",
                                        alt=spec.home_abbr,
                                    ),
                                    html.Span(spec.home_abbr, className="recent-games-card-abbr"),
                                    html.Span(
                                        str(spec.home_pts),
                                        className="recent-games-card-score"
                                        + (" recent-games-card-score--win" if home_win else ""),
                                    ),
                                ],
                                className="recent-games-card-side",
                            ),
                        ],
                        className="recent-games-card-mid",
                    ),
                    html.Div(
                        f"{spec.home_pts - spec.away_pts:+d} margin",
                        className="recent-games-card-margin",
                    ),
                ],
                id={"type": "recent-game-card", "game": spec.game_description},
                n_clicks=0,
                className="recent-games-card" + (" recent-games-card--selected" if sel else ""),
                role="button",
                tabIndex=0,
            )
        )
    return html.Div(html.Div(cells, className=row_cls), className="recent-games-card-strip-inner")


def _pbp_quarter_axis_config(x_min: float) -> tuple[list[float], list[str], list[dict]]:
    """X-axis ticks at mid-quarter (and mid-OT) positions; vertical guides at period boundaries."""
    mids = [42.0, 30.0, 18.0, 6.0]
    labels = ["Q1", "Q2", "Q3", "Q4"]
    boundaries = [48.0, 36.0, 24.0, 12.0, 0.0]
    if x_min < 0:
        span = 5.0
        n_ot = min(12, max(1, math.ceil(-float(x_min) / span - 1e-9)))
        for i in range(n_ot):
            lo = -span * i
            hi = -span * (i + 1)
            mids.append((lo + hi) / 2)
            labels.append(f"OT{i + 1}")
            boundaries.append(hi)
    shapes = [
        {
            "type": "line",
            "xref": "x",
            "yref": "paper",
            "x0": b,
            "x1": b,
            "y0": 0,
            "y1": 1,
            "line": {"color": "rgba(230, 224, 224, 0.14)", "width": 1},
        }
        for b in boundaries
    ]
    return mids, labels, shapes


def create_performance_legend():
    pills = [
        ("Season high", PERFORMANCE_COLORS[1]),
        ("10+ pts above avg", PERFORMANCE_COLORS[2]),
        ("10+ pts below avg", PERFORMANCE_COLORS[3]),
    ]
    return html.Div(
        [
            html.Div("CELL COLORING LEGEND", className="recent-games-panel-eyebrow"),
            html.Div(
                [
                    html.Span(
                        label,
                        className="recent-games-legend-pill",
                        style={"backgroundColor": color},
                    )
                    for label, color in pills
                ],
                className="d-flex flex-wrap gap-2 mt-2",
            ),
        ],
        className="recent-games-legend-card mx-auto",
    )


def create_simple_players_table():
    recent_games_players_df = get_table("recent_games_players")
    if recent_games_players_df is None or recent_games_players_df.empty:
        return dark_datatable(
            table_id="player-recent-games-table",
            columns=RECENT_PLAYERS_SIMPLE_COLUMNS,
            data=[],
            cell_selectable=False,
            sort_action="native",
            page_size=12,
            style_table={"width": "100%", "minWidth": "100%"},
            style_cell={
                "textAlign": "center",
                "fontSize": 13,
                "padding": "6px",
                "height": "auto",
                "minHeight": "2rem",
                "whiteSpace": "normal",
            },
        )
    cols_keep = [
        "team",
        "player",
        "pts",
        "game_ts_percent",
        "plus_minus",
        "outcome",
        "pts_color",
        "ts_color",
    ]
    rows = recent_games_players_df[cols_keep].to_dict("records")
    return dark_datatable(
        table_id="player-recent-games-table",
        columns=RECENT_PLAYERS_SIMPLE_COLUMNS,
        data=rows,
        cell_selectable=False,
        sort_action="native",
        page_size=12,
        style_table={"width": "100%", "minWidth": "100%"},
        style_cell={
            "textAlign": "center",
            "fontSize": 13,
            "padding": "6px",
            "height": "auto",
            "minHeight": "2rem",
            "whiteSpace": "normal",
        },
        style_cell_conditional=[
            {"if": {"column_id": "team"}, "width": "8%"},
            {"if": {"column_id": "player"}, "width": "28%", "textAlign": "left"},
            {"if": {"column_id": "pts"}, "width": "8%"},
            {"if": {"column_id": "game_ts_percent"}, "width": "12%"},
            {"if": {"column_id": "plus_minus"}, "width": "10%"},
            {"if": {"column_id": "outcome"}, "width": "8%"},
        ],
        style_data_conditional=[
            {
                "if": {"filter_query": "{pts_color} = 1", "column_id": "pts"},
                "backgroundColor": PERFORMANCE_COLORS[1],
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {"filter_query": "{pts_color} = 2", "column_id": "pts"},
                "backgroundColor": PERFORMANCE_COLORS[2],
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {"filter_query": "{pts_color} = 3", "column_id": "pts"},
                "backgroundColor": PERFORMANCE_COLORS[3],
                "color": "white",
                "fontWeight": "bold",
            },
            {
                "if": {"filter_query": "{ts_color} = 1", "column_id": "game_ts_percent"},
                "backgroundColor": PERFORMANCE_COLORS[1],
                "color": "white",
                "fontWeight": "bold",
            },
        ],
    )


def _pbp_chart_chrome_above_plot(game_desc: str | None) -> html.Div:
    leg = _flow_legend_and_stats(game_desc)[0] if game_desc else ""
    return html.Div(
        html.Div(id="recent-games-flow-legend-slot", children=leg),
        className="recent-games-pbp-heading-wrap mb-2 w-100",
    )


def recent_games_layout() -> html.Div:
    game_options, default_sel = _game_options()
    return html.Div(
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            f"Recent Games on {_slate_date_label()}",
                            className="recent-games-hero-title recent-games-hero-compact mb-2",
                        ),
                        html.P(
                            _pbp_chart_subtitle(),
                            className="text-muted small mb-2",
                        ),
                        _slate_summary_bar(),
                        html.Div(
                            dcc.Dropdown(
                                id="game-selector",
                                options=game_options,
                                clearable=False,
                                value=default_sel,
                                className="dash-dropdown recent-games-dropdown-sr",
                            ),
                            className="position-relative",
                        ),
                        html.Div(
                            id="recent-games-card-strip",
                            children=render_game_cards(default_sel),
                            className="recent-games-card-strip mb-3 w-100",
                        ),
                    ],
                    className="recent-games-shell text-center w-100 py-3",
                ),
                html.Div(
                    [
                        _pbp_chart_chrome_above_plot(default_sel),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="pbp-analysis-plot",
                                            config={"displayModeBar": False},
                                            style={"height": "560px", "width": "100%"},
                                        ),
                                    ],
                                    width=12,
                                    className="recent-games-minw-0",
                                ),
                            ],
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "TOP PLAYER LINES · FULL SLATE",
                                    className="recent-games-section-eyebrow text-center mb-2",
                                ),
                                html.Div(
                                    create_performance_legend(),
                                    className="d-flex justify-content-center mb-3 w-100",
                                ),
                                html.Div(
                                    create_simple_players_table(),
                                    className="recent-games-players-table-block",
                                ),
                            ],
                            width=12,
                            className="px-0",
                        ),
                    ],
                    className="g-0 mt-2",
                ),
            ],
            className="recent-games-page recent-games-fullbleed",
        ),
        className="custom-padding recent-games-outer",
    )


@callback(
    Output("game-selector", "value"),
    Input({"type": "recent-game-card", "game": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def pick_game_from_card(_clicks):
    if not callback_context.triggered:
        raise PreventUpdate
    raw = callback_context.triggered[0]["prop_id"].rsplit(".", 1)[0]
    picked = json.loads(raw)["game"]
    return picked


@callback(
    Output("recent-games-card-strip", "children"),
    Input("game-selector", "value"),
)
def sync_game_cards(selected):
    return render_game_cards(selected)


@callback(
    Output("recent-games-flow-legend-slot", "children"),
    Input("game-selector", "value"),
)
def sync_chrome(selected):
    if not selected:
        return ""
    legend, _meta = _flow_legend_and_stats(selected)
    return legend


@callback(Output("pbp-analysis-plot", "figure"), Input("game-selector", "value"))
def update_pbp_plot(selected_game):
    """Update play-by-play analysis plot (scatter + line, same data as before)."""
    if not selected_game:
        return {}

    _pbp_df, _pbp_plot_kpis, pbp_plot_df = _pbp_data()
    filtered_pbp = pbp_plot_df.loc[pbp_plot_df["game_description"] == selected_game]

    if filtered_pbp.empty:
        return {}

    fig = px.scatter(
        filtered_pbp,
        x="time_remaining_final",
        y="margin_score",
        labels={
            "margin_score": "Score Differential",
            "time_remaining_final": "Game Time",
        },
        title=None,
        custom_data=[
            "play",
            "time_quarter",
            "quarter",
            "leading_team_text",
            "score",
            "game_plot_team_text",
        ],
    )

    apply_dark_layout(fig, transparent_plot=True)
    x_num = pd.to_numeric(filtered_pbp["time_remaining_final"], errors="coerce")
    x_min = float(x_num.min()) if not x_num.empty else 0.0
    if math.isnan(x_min):
        x_min = 0.0
    tickvals, ticktext, quarter_shapes = _pbp_quarter_axis_config(x_min)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        title=None,
        shapes=quarter_shapes,
        margin=dict(l=48, r=28, t=36, b=48),
    )

    fig.update_traces(
        marker=dict(
            color=filtered_pbp["scoring_team_color"],
            size=8,
            line=dict(width=1, color="rgb(230, 224, 224)"),
        ),
        mode="markers+lines",
        hoverlabel=TRACE_HOVERLABEL,
        hovertemplate=(
            "<b>Time:</b> %{customdata[1]} in %{customdata[2]}<br>"
            "<b>Scoring Team:</b> %{customdata[5]}<br>"
            "<b>Score:</b> %{customdata[4]} (%{customdata[3]})<br>"
            "<b>Play:</b> %{customdata[0]}<br>"
            "<extra></extra>"
        ),
    )

    fig.update_xaxes(
        autorange="reversed",
        tickmode="array",
        tickvals=tickvals,
        ticktext=ticktext,
        showgrid=False,
        showline=True,
        linecolor="rgb(230, 224, 224)",
        linewidth=1,
        mirror=True,
        title="Quarter",
    )

    fig.update_yaxes(
        showline=True,
        linecolor="rgb(230, 224, 224)",
        linewidth=1,
        mirror=True,
        title="Score Differential",
    )

    return fig
