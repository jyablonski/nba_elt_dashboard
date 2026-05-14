from datetime import date

from src.utils import create_season_selector_dropdown


def test_season_selector_playoffs_window():
    row = create_season_selector_dropdown(current_date=date(2024, 5, 1))
    dd = row.children[0].children[1]
    assert dd.value == "Playoffs"
    assert len(dd.options) == 2


def test_season_selector_regular_season_outside_playoffs():
    row = create_season_selector_dropdown(current_date=date(2024, 1, 15))
    dd = row.children[0].children[1]
    assert dd.value == "Regular Season"
    assert len(dd.options) == 1
