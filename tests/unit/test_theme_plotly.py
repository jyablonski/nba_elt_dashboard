import plotly.graph_objects as go

from src.theme.plotly import apply_dark_layout


def test_apply_dark_layout_hover_and_paper():
    fig = go.Figure(data=go.Scatter(x=[1], y=[2]))
    apply_dark_layout(fig)
    layout = fig.layout
    assert layout.paper_bgcolor == "#15171a"
    assert layout.hoverlabel.bgcolor == "#222222"
    assert "Inter" in layout.hoverlabel.font.family


def test_apply_dark_layout_transparent_plot():
    fig = go.Figure(data=go.Scatter(x=[1], y=[2]))
    apply_dark_layout(fig, transparent_plot=True)
    assert fig.layout.plot_bgcolor == "rgba(0,0,0,0)"


def test_apply_dark_layout_plotly_json_contract():
    """Phase 7b - stable layout keys/colors for dark theme (regression guard)."""
    fig = go.Figure(data=go.Scatter(x=[1, 2], y=[3, 4]))
    apply_dark_layout(fig, transparent_plot=False)
    layout = fig.to_plotly_json()["layout"]
    assert layout["paper_bgcolor"] == "#15171a"
    assert layout["plot_bgcolor"] == "#15171a"
    assert layout["font"]["color"] == "rgb(230, 224, 224)"
    assert layout["hoverlabel"]["bgcolor"] == "#222222"
    assert "Inter" in layout["hoverlabel"]["font"]["family"]

    fig2 = go.Figure(data=go.Scatter(x=[1], y=[2]))
    apply_dark_layout(fig2, transparent_plot=True)
    assert fig2.to_plotly_json()["layout"]["plot_bgcolor"] == "rgba(0,0,0,0)"
