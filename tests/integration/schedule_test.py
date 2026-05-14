import pytest
from dash import dash_table

from src.data_cols.future_schedule import future_schedule_columns
from src.data_cols.tonights_schedule import tonights_schedule_columns
from src.pages.schedule import update_schedule_table


@pytest.mark.parametrize(
    ("tab", "columns", "expected_away"),
    [
        ("tonights-games", tonights_schedule_columns, "Detroit Pistons"),
        ("full-schedule", future_schedule_columns, "Boston Celtics"),
    ],
)
def test_schedule_table_contract(tab, columns, expected_away):
    output = update_schedule_table(tab)

    assert isinstance(output, dash_table.DataTable)
    assert output.columns == columns
    assert len(output.data) > 0
    assert output.data[0]["away_team"] == expected_away
