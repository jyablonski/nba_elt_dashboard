import dash_bootstrap_components as dbc

from src.ui.badges import tab_count_badge


def test_tab_count_badge_default_class():
    b = tab_count_badge(12)
    assert isinstance(b, dbc.Badge)
    assert b.children == "12"
    assert "app-tab-badge" in (b.className or "")


def test_tab_count_badge_custom_class():
    b = tab_count_badge(0, class_name="custom-badge")
    assert "custom-badge" in (b.className or "")
