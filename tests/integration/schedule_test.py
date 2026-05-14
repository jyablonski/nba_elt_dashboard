from dash import dash_table, html

from src.data_cols.future_schedule import future_schedule_columns
from src.pages.schedule import update_schedule_table


def test_schedule_tonights_cards_contract():
    output = update_schedule_table("tonights-games")

    assert isinstance(output, html.Div)
    flat = str(output)
    assert "Detroit Pistons" in flat
    assert "schedule-tonight-grid" in flat


def test_schedule_full_table_contract():
    output = update_schedule_table("full-schedule")

    assert isinstance(output, html.Div)
    table = output.children
    assert isinstance(table, dash_table.DataTable)
    assert table.columns == future_schedule_columns
    assert len(table.data) > 0
    assert table.data[0]["away_team"] == "Boston Celtics"
