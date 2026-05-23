from __future__ import annotations

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import callback, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from src.data_cols.reddit_comments import reddit_comments_slim_columns
from src.data_cols.reddit_recent_keywords import reddit_keyword_columns
from src.database import (
    reddit_comments_df,
    reddit_sentiment_time_series_df,
    reddit_recent_keywords_df,
    social_media_aggs_df,
)
from src.data import team_names_abbreviations
from src.social_media_insights import (
    normalized_daily_volume,
    snapshot_kpis,
    top_flair_share,
    top_flairs,
    top_keywords,
)
from src.social_media_plots import top_threads_engagement_figure
from src.theme.plotly import TRACE_HOVERLABEL, apply_dark_layout
from src.ui.cards import kpi_card as create_kpi_card
from src.ui.sections import page_hero, section_header
from src.ui.tables import dark_datatable

GAME_OUTCOME_COLORS = {
    "W": "#45c2e6",
    "L": "#e85c5c",
    "NO GAME": "#7a8a9c",
}

TEAM_OPTIONS = [{"label": team, "value": team} for team in team_names_abbreviations]

# Default for "Comments vs prior game" team chart (dropdown + initial figure)
_SOCIAL_PRIOR_GAME_DEFAULT_TEAM = "LAL"

COMMENTS_TOOLTIP_CSS = [
    {
        "selector": ".dash-table-tooltip",
        "rule": (
            "background-color: #222222; font-family: Inter, system-ui, sans-serif; "
            "color: rgb(230, 224, 224)"
        ),
    }
]

# Display frame: markdown links + short preview (full text in tooltip)
reddit_display_df = reddit_comments_df.copy()
reddit_display_df["url"] = reddit_display_df["url"].str.replace("^(.*)$", "[Link](\\1)", regex=True)


def _comment_preview(text: object, limit: int = 160) -> str:
    t = str(text).strip()
    if len(t) <= limit:
        return t
    return f"{t[: limit - 1]}…"


reddit_display_df["comment_preview"] = reddit_display_df["comment"].map(_comment_preview)

_KPIS = snapshot_kpis(reddit_comments_df, reddit_recent_keywords_df, social_media_aggs_df)


def _top_flair_share_kpi() -> tuple[str, str, str | None]:
    pct, name = top_flair_share(reddit_comments_df)
    if pct is None or name is None:
        return "-", "Top flair share", None
    headline = f"{pct:.1f}%"
    sub = f"{name} - share of sampled comments"
    return headline, "Top flair share", sub


def create_insight_kpi(*, headline: str, title: str, subtitle: str | None = None) -> html.Div:
    parts = [
        html.Div(headline, className="kpi-card__value"),
        html.Div(title, className="kpi-card__title"),
    ]
    if subtitle:
        parts.append(html.Div(subtitle, className="kpi-card__sub"))
    return create_kpi_card(parts)


def _empty_fig(message: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        annotations=[
            dict(
                text=message,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=14, color="rgb(180, 175, 175)"),
            )
        ],
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    apply_dark_layout(fig, transparent_plot=True)
    return fig


# Volume area: brighter line + airy fill (default px blue is too heavy on dark UI).
_VOLUME_LINE = "rgb(122, 198, 242)"
_VOLUME_FILL = "rgba(122, 198, 242, 0.18)"
# Moving average: amber accent (distinct from blue volume / teal wins).
_MA7_LINE_COLOR = "rgba(255, 159, 67, 0.95)"  # #ff9f43


def _add_7day_moving_avg(
    fig: go.Figure,
    *,
    x: pd.Series,
    y: pd.Series,
    hover_y_fmt: str,
    name: str = "7-day moving avg",
) -> None:
    """Overlay a 7-day rolling mean (min_periods=1 so early dates still show partial windows)."""
    ys = pd.to_numeric(y, errors="coerce")
    ma = ys.rolling(window=7, min_periods=1).mean()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=ma,
            mode="lines",
            name=name,
            line=dict(width=2.75, color=_MA7_LINE_COLOR),
            hoverlabel=TRACE_HOVERLABEL,
            hovertemplate=f"%{{x}}<br>{name}: %{{y:{hover_y_fmt}}}<extra></extra>",
            showlegend=False,
        )
    )
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=1,
        y=1,
        text=f"<span style='font-size:18px;line-height:0'>━</span>&nbsp;{name}",
        xanchor="right",
        yanchor="top",
        showarrow=False,
        font=dict(size=12, color=_MA7_LINE_COLOR),
        bgcolor="rgba(21, 23, 26, 0.72)",
        bordercolor="rgba(255, 159, 67, 0.35)",
        borderwidth=1,
        borderpad=4,
    )


def build_league_volume_figure() -> go.Figure:
    d = normalized_daily_volume(reddit_sentiment_time_series_df, reddit_comments_df)
    if d.empty:
        return _empty_fig("No daily volume to plot")
    d = d.sort_values("scrape_date")
    fig = px.area(
        d,
        x="scrape_date",
        y="volume",
        title="League-wide comment volume",
    )
    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
        hovertemplate="%{x}<br>%{y:,} comments<extra></extra>",
        line=dict(color=_VOLUME_LINE, width=2),
        fillcolor=_VOLUME_FILL,
    )
    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Comments",
        title={"x": 0.5, "xanchor": "center"},
        margin=dict(l=48, r=24, t=48, b=48),
        showlegend=False,
    )
    _add_7day_moving_avg(fig, x=d["scrape_date"], y=d["volume"], hover_y_fmt=",.0f")
    return fig


def build_top_threads_engagement_figure() -> go.Figure:
    return top_threads_engagement_figure(reddit_comments_df)


def build_top_keywords_figure() -> go.Figure:
    kwd = top_keywords(reddit_recent_keywords_df, 14)
    if kwd.empty:
        return _empty_fig("No keyword rankings")
    kwd = kwd.sort_values("word_frequency", ascending=True)
    fig = px.bar(
        kwd,
        x="word_frequency",
        y="word",
        orientation="h",
        title="Top keywords in recent threads",
    )
    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL, hovertemplate="%{y}<br>%{x} mentions<extra></extra>"
    )
    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(
        xaxis_title="Mentions",
        yaxis_title="",
        title={"x": 0.5, "xanchor": "center"},
        margin=dict(l=120, r=24, t=48, b=48),
    )
    return fig


def build_top_flairs_figure() -> go.Figure:
    fl = top_flairs(reddit_display_df, 12)
    if fl.empty:
        return _empty_fig("No flair counts")
    fl = fl.sort_values("count", ascending=True)
    fig = px.bar(
        fl,
        x="count",
        y="flair",
        orientation="h",
        title="Most common user flairs (sample)",
    )
    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL, hovertemplate="%{y}<br>%{x} comments<extra></extra>"
    )
    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(
        xaxis_title="Comments",
        yaxis_title="",
        title={"x": 0.5, "xanchor": "center"},
        margin=dict(l=140, r=24, t=48, b=48),
    )
    return fig


def create_keywords_table():
    return dark_datatable(
        table_id="keywords-table",
        columns=reddit_keyword_columns,
        data=reddit_recent_keywords_df.to_dict("records"),
        cell_selectable=False,
        filter_action="native",
        sort_action="native",
        page_size=20,
        style_cell={
            "whiteSpace": "normal",
            "height": "auto",
            "minHeight": "2.5rem",
            "lineHeight": "1.35",
            "textAlign": "center",
            "fontSize": 15,
            "color": "rgb(230, 224, 224)",
        },
        hidden_columns=[
            "top_nba_team_flair",
            "most_common_sentiment",
            "avg_sentiment_when_used",
            "analysis_date",
        ],
        style_cell_conditional=[
            {
                "if": {"column_id": "word"},
                "width": "25%",
                "textAlign": "left",
                "fontWeight": "bold",
            },
            {"if": {"column_id": "word_frequency"}, "width": "25%"},
            {"if": {"column_id": "frequency_rank"}, "width": "25%"},
            {"if": {"column_id": "nba_team_flairs_using_word"}, "width": "25%"},
        ],
        style_data_conditional=[
            {
                "if": {
                    "filter_query": "{avg_sentiment_when_used} > 0.1",
                    "column_id": "avg_sentiment_when_used",
                },
                "backgroundColor": "#4CAF50",
                "color": "white",
            },
            {
                "if": {
                    "filter_query": "{avg_sentiment_when_used} < -0.1",
                    "column_id": "avg_sentiment_when_used",
                },
                "backgroundColor": "#F44336",
                "color": "white",
            },
        ],
    )


def _team_outcome_figure(selected_team: str | None) -> go.Figure:
    if not selected_team:
        return _empty_fig("Pick a team")

    filtered_data = reddit_sentiment_time_series_df[
        reddit_sentiment_time_series_df["team"] == selected_team
    ]

    if filtered_data.empty:
        return _empty_fig(f"No flair timeline rows for {selected_team}")

    fd = filtered_data.copy()
    fd["scrape_date"] = pd.to_datetime(fd["scrape_date"])
    daily_total = (
        fd.groupby("scrape_date", as_index=False)["num_comments"].sum().sort_values("scrape_date")
    )

    fig = px.bar(
        fd,
        x="scrape_date",
        y="num_comments",
        color="game_outcome",
        color_discrete_map=GAME_OUTCOME_COLORS,
        labels={
            "scrape_date": "Date",
            "num_comments": "Number of Comments",
            "game_outcome": "Previous Day's Game Outcome",
        },
        title=f"{selected_team} - comments by prior game outcome",
    )

    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(
        legend_title_text="Game Outcome",
        showlegend=True,
        title={"x": 0.5, "xanchor": "center"},
    )

    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
        hovertemplate=(
            "<b>Date:</b> %{x}<br>"
            "<b>Comments:</b> %{y}<br>"
            "<b>Game Outcome:</b> %{fullData.name}<br>"
            "<extra></extra>"
        ),
    )

    _add_7day_moving_avg(
        fig,
        x=daily_total["scrape_date"],
        y=daily_total["num_comments"],
        hover_y_fmt=",.0f",
        name="7-day avg (daily total)",
    )

    return fig


_TEAM_CHART_INIT = _team_outcome_figure(_SOCIAL_PRIOR_GAME_DEFAULT_TEAM)


def create_slim_comments_table():
    sub = reddit_display_df[["scrape_date", "flair", "score", "compound", "comment_preview", "url"]]
    rows = sub.to_dict("records")
    tooltip_data = [
        {"comment_preview": {"value": str(c)[:4000], "type": "markdown"}}
        for c in reddit_display_df["comment"].tolist()
    ]
    return dark_datatable(
        table_id="social-media-slim-table",
        columns=reddit_comments_slim_columns,
        data=rows,
        css=COMMENTS_TOOLTIP_CSS,
        cell_selectable=False,
        filter_action="native",
        sort_action="native",
        page_size=12,
        style_cell={
            "whiteSpace": "normal",
            "height": "auto",
            "minHeight": "2.25rem",
            "lineHeight": "1.35",
            "textAlign": "center",
            "fontSize": 13,
            "color": "rgb(230, 224, 224)",
        },
        style_cell_conditional=[
            {"if": {"column_id": "scrape_date"}, "width": "10%"},
            {"if": {"column_id": "flair"}, "width": "10%"},
            {"if": {"column_id": "score"}, "width": "8%"},
            {"if": {"column_id": "compound"}, "width": "10%"},
            {"if": {"column_id": "url"}, "width": "8%"},
            {"if": {"column_id": "comment_preview"}, "textAlign": "left", "width": "54%"},
        ],
        tooltip_data=tooltip_data,
        tooltip_duration=None,
    )


def _kpi_row() -> list:
    rt = _KPIS["reddit_total"]
    pdiff = _KPIS["reddit_pct_diff"]
    diff_txt = None
    if pdiff is not None:
        diff_txt = f"{pdiff:+.1f}% vs rolling average snapshot"

    share_h, share_title, share_sub = _top_flair_share_kpi()
    cards = [
        create_insight_kpi(
            headline=f"{rt:,}" if rt is not None else "-",
            title="Reddit comments in latest scrape",
            subtitle=diff_txt,
        ),
        create_insight_kpi(
            headline=share_h,
            title=share_title,
            subtitle=share_sub,
        ),
    ]
    tw = _KPIS["top_word"]
    twf = _KPIS["top_word_freq"]
    if tw is not None and twf is not None:
        cards.append(
            create_insight_kpi(
                headline=tw,
                title="Top trending token",
                subtitle=f"{twf:,} mentions in ranked window",
            )
        )
    else:
        cards.append(
            create_insight_kpi(
                headline="-", title="Top trending token", subtitle="No keyword table rows"
            )
        )
    n_flairs = _KPIS["distinct_flairs"]
    cards.append(
        create_insight_kpi(
            headline=f"{n_flairs:,}" if n_flairs is not None else "-",
            title="Distinct flairs in sample",
            subtitle="Fan identity diversity in this pull",
        )
    )
    return cards


social_media_analysis_layout = html.Div(
    [
        page_hero(
            title="r/NBA Social Pulse",
            title_meta=[
                html.Img(
                    src="../assets/reddit.png",
                    alt="Reddit",
                    style={"height": "48px", "width": "48px"},
                ),
            ],
        ),
        html.Div(_kpi_row(), className="kpi-container"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        figure=build_league_volume_figure(), config={"displayModeBar": False}
                    ),
                    xs=12,
                    lg=6,
                    className="mb-3",
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="social-media-top-threads-graph",
                            figure=build_top_threads_engagement_figure(),
                            config={"displayModeBar": False},
                        ),
                        html.Div(id="social-media-top-threads-dummy", style={"display": "none"}),
                    ],
                    xs=12,
                    lg=6,
                    className="mb-3",
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=build_top_keywords_figure(), config={"displayModeBar": False}),
                    xs=12,
                    lg=6,
                    className="mb-3",
                ),
                dbc.Col(
                    dcc.Graph(figure=build_top_flairs_figure(), config={"displayModeBar": False}),
                    xs=12,
                    lg=6,
                    className="mb-3",
                ),
            ],
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "Comments vs prior game result", className="mb-0 align-self-center"
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Team",
                                    className="form-label fw-bold mb-0 me-2",
                                    htmlFor="social-media-team-selector",
                                ),
                                dcc.Dropdown(
                                    id="social-media-team-selector",
                                    options=TEAM_OPTIONS,
                                    value=_SOCIAL_PRIOR_GAME_DEFAULT_TEAM,
                                    clearable=False,
                                    className="dash-dropdown",
                                    style={"minWidth": "220px", "maxWidth": "320px"},
                                ),
                            ],
                            className="d-flex flex-wrap align-items-center",
                        ),
                    ],
                    className="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-3",
                ),
                html.Div(
                    dcc.Graph(
                        id="social-media-plot",
                        figure=_TEAM_CHART_INIT,
                        style={"width": "100%", "height": "460px"},
                    ),
                    className="social-media-flair-chart-wrap",
                ),
            ],
            className="mb-2",
        ),
        html.Details(
            [
                html.Summary("Detailed tables (full keyword stats & comment preview)"),
                html.Div(
                    [
                        section_header("Recent comments"),
                        create_slim_comments_table(),
                        section_header("Trending keywords"),
                        create_keywords_table(),
                    ],
                    className="mt-3",
                ),
            ],
            className="social-media-details mb-4",
            open=False,
        ),
    ],
    className="custom-padding",
)


@callback(Output("social-media-plot", "figure"), Input("social-media-team-selector", "value"))
def update_reddit_team_sentiment(selected_team):
    """Update sentiment plot based on selected team"""
    return _team_outcome_figure(selected_team)
