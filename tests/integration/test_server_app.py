import dash_bootstrap_components as dbc


def test_dash_app_title_and_layout():
    import src.server as server

    assert server.app.title == server.APP_TITLE == "NBA Dashboard"
    assert server.app.layout is not None
    tabs = server._tabs
    assert isinstance(tabs, dbc.Tabs)
    assert tabs.id == "tabs"

    layout_dump = str(server.app.layout.to_plotly_json())
    assert "app-navbar" not in layout_dump
    assert "app-brand" not in layout_dump
    assert "app-season-pill" not in layout_dump
