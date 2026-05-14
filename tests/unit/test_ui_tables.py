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
