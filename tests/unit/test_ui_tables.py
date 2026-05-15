from src.ui.tables import dark_datatable


def test_dark_datatable_merges_style_cell():
    t = dark_datatable(
        table_id="t1",
        columns=[{"name": "a", "id": "a"}],
        data=[{"a": 1}],
        style_cell={"padding": "4px"},
    )
    assert t.id == "t1"
    assert t.style_cell["padding"] == "4px"
    assert "background-color" in t.style_cell
    assert t.css and t.css[0]["selector"] == ".show-hide"


def test_dark_datatable_prepends_hide_toggle_to_custom_css():
    custom = [{"selector": ".dash-table-tooltip", "rule": "color: red;"}]
    t = dark_datatable(
        table_id="t2",
        columns=[{"name": "a", "id": "a"}],
        data=[{"a": 1}],
        css=custom,
    )
    assert t.css[0]["selector"] == ".show-hide"
    assert t.css[1] == custom[0]


def test_dark_datatable_prepends_hide_toggle_when_css_is_single_dict():
    user_css = {"selector": ".custom", "rule": "color: blue;"}
    t = dark_datatable(
        table_id="t3",
        columns=[{"name": "a", "id": "a"}],
        data=[{"a": 1}],
        css=user_css,
    )
    assert t.css[0]["selector"] == ".show-hide"
    assert t.css[1] == user_css
