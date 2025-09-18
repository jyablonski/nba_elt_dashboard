from dash import html


def create_kpi_card(content, class_name="kpi-card"):
    """Helper function to create consistent KPI cards"""
    return html.Div(content, className=class_name)


BASE_TABLE_STYLE = {
    "background-color": "#383b3d",
    "textAlign": "center",
    "fontSize": 12,
}

# Dark theme layout template
DARK_LAYOUT_TEMPLATE = {
    "plot_bgcolor": "#15171a",
    "paper_bgcolor": "#15171a",
    "font": {
        "color": "rgb(230, 224, 224)",
        "family": "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    },
    "xaxis": {
        "gridcolor": "#383b3d",
        "linecolor": "#383b3d",
        "tickcolor": "#383b3d",
        "zerolinecolor": "#383b3d",
    },
    "yaxis": {
        "gridcolor": "#383b3d",
        "linecolor": "#383b3d",
        "tickcolor": "#383b3d",
        "zerolinecolor": "#383b3d",
    },
    "margin": {"l": 80, "r": 40, "t": 80, "b": 60},
}

CUSTOM_COLORS = [
    "#3fb7d9",  # the existing ten-above blue
    "#9362DA",  # the existing season-high purple
    "#e04848",  # the existing ten-below red
    "#1EAEDB",  # the accent color
    "#5e6063",  # the hover color
    "#FF4136",  # the selected background
]

# Single bar chart color (matches the theme)
SINGLE_BAR_COLOR = "#3fb7d9"
