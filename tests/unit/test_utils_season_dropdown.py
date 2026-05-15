from datetime import date

from src.utils import create_season_selector_dropdown, scoring_efficiency_season_config


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


def test_scoring_efficiency_season_offseason_not_playoffs_default():
    """Jul–Sep should not default to Playoffs (old bug used Apr 15–Sep 30)."""
    default, opts = scoring_efficiency_season_config(current_date=date(2024, 8, 10))
    assert default == "Regular Season"
    assert len(opts) == 1
    assert opts[0]["value"] == "Regular Season"


def test_scoring_efficiency_playoffs_end_inclusive_june():
    default, opts = scoring_efficiency_season_config(current_date=date(2024, 6, 30))
    assert default == "Playoffs"
    assert len(opts) == 2


def test_scoring_efficiency_july_is_offseason():
    default, opts = scoring_efficiency_season_config(current_date=date(2024, 7, 1))
    assert default == "Regular Season"
    assert len(opts) == 1
