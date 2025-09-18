from dash import dash_table

from src.pages.schedule import update_schedule_table
from src.data_cols.future_schedule import future_schedule_columns
from src.data_cols.tonights_schedule import tonights_schedule_columns


def test_schedule_tonight():
    output = update_schedule_table("tonights-games")

    assert isinstance(output, dash_table.DataTable)
    assert output.columns == tonights_schedule_columns
    assert len(output.data) > 0  # Has some data
    assert output.data[0]["away_team"] == "Detroit Pistons"

def test_schedule_full():
    output = update_schedule_table("full-schedule")

    assert isinstance(output, dash_table.DataTable)
    assert output.columns == future_schedule_columns
    assert len(output.data) > 0
    assert output.data[0]["away_team"] == "Boston Celtics"
