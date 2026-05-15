"""Plotly figures for social media pages (no database import)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.social_media_insights import top_threads_by_engagement
from src.theme.plotly import TRACE_HOVERLABEL, apply_dark_layout

_TOP_THREADS_BAR = "rgb(122, 198, 242)"


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


def top_threads_engagement_figure(
    comments_df: pd.DataFrame | None, *, n_threads: int = 10
) -> go.Figure:
    """Horizontal bars: threads with the most sampled comments (URL-aggregated)."""
    g = top_threads_by_engagement(comments_df, n=n_threads)
    if g.empty:
        return _empty_fig("Not enough thread URLs in this sample to rank by engagement")
    plot = g.sort_values("n_comments", ascending=True)
    k = len(plot)
    fig = px.bar(
        plot,
        x="n_comments",
        y="label",
        orientation="h",
        title=f"Top {k} threads by comments in sample",
        color_discrete_sequence=[_TOP_THREADS_BAR],
    )
    cd = plot[["thread_url", "avg_score", "avg_compound"]].to_numpy()
    fig.update_traces(
        hoverlabel=TRACE_HOVERLABEL,
        customdata=cd,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Comments in sample: %{x:,}<br>"
            "Avg upvotes: %{customdata[1]:.1f}<br>"
            "Avg compound: %{customdata[2]:.3f}<br>"
            "<span style='font-size:11px;opacity:0.85'>%{customdata[0]}</span><br>"
            "<span style='font-size:11px;opacity:0.75'>Click near the title or bar to open thread</span>"
            "<extra></extra>"
        ),
    )
    # Narrow invisible bars on the left so clicks beside the y labels still hit a trace with URL.
    nc = plot["n_comments"].to_numpy(dtype=float)
    pad_vals = np.maximum(nc * 0.15, 3.0)
    pad_vals = np.minimum(pad_vals, nc * 0.48)
    fig.add_trace(
        go.Bar(
            y=plot["label"],
            x=pad_vals,
            orientation="h",
            marker=dict(color="rgba(0,0,0,0)", line=dict(width=0)),
            customdata=cd,
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.update_layout(barmode="overlay")
    apply_dark_layout(fig, transparent_plot=True)
    fig.update_layout(
        title={"x": 0.5, "xanchor": "center"},
        xaxis_title="Comment rows (sample)",
        yaxis_title="",
        showlegend=False,
        margin=dict(l=280, r=24, t=48, b=48),
    )
    return fig
