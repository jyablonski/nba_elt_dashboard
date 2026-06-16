from __future__ import annotations

import plotly.graph_objects as go

from src.config import DARK_LAYOUT_TEMPLATE

# Keep Plotly hover tooltips visually consistent with the team dropdowns
# (.Select-control / .Select-menu-outer in static/styles.css): same
# surface-header background and --text foreground tokens. This keeps the dark
# theme coherent under dark-mode reader extensions.
HOVERLABEL_BG = "#222222"  # --surface-header
HOVERLABEL_TEXT = "#e8e6e3"  # --text

TRACE_HOVERLABEL = dict(
    bgcolor=HOVERLABEL_BG,
    bordercolor=HOVERLABEL_BG,
    font=dict(
        size=12,
        family="Inter, system-ui, sans-serif",
        color=HOVERLABEL_TEXT,
    ),
)


def apply_dark_layout(fig: go.Figure, *, transparent_plot: bool = False) -> go.Figure:
    layout = dict(DARK_LAYOUT_TEMPLATE)
    if transparent_plot:
        layout["plot_bgcolor"] = "rgba(0,0,0,0)"
    fig.update_layout(
        **layout,
        hoverlabel=dict(TRACE_HOVERLABEL),
    )
    return fig
