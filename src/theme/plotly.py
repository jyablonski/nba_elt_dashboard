from __future__ import annotations

import plotly.graph_objects as go

from src.config import DARK_LAYOUT_TEMPLATE

TRACE_HOVERLABEL = dict(
    bgcolor="#222222",
    font=dict(
        size=12,
        family="Inter, system-ui, sans-serif",
        color="rgb(230, 224, 224)",
    ),
)


def apply_dark_layout(fig: go.Figure, *, transparent_plot: bool = False) -> go.Figure:
    layout = dict(DARK_LAYOUT_TEMPLATE)
    if transparent_plot:
        layout["plot_bgcolor"] = "rgba(0,0,0,0)"
    fig.update_layout(
        **layout,
        hoverlabel=dict(
            bgcolor="#222222",
            font=dict(
                size=12,
                family="Inter, system-ui, sans-serif",
                color="rgb(230, 224, 224)",
            ),
        ),
    )
    return fig
