import pandas as pd

from src.shell import season_phase_label, tab_label_with_badge


def test_season_phase_playoffs():
    df = pd.DataFrame({"flag": ["playoffs", "season"], "is_enabled": [1, 1]})
    assert season_phase_label(df) == "Playoffs"


def test_season_phase_regular():
    df = pd.DataFrame({"flag": ["playoffs", "season"], "is_enabled": [0, 1]})
    assert season_phase_label(df) == "Regular season"


def test_season_phase_fallback():
    df = pd.DataFrame({"flag": ["playoffs", "season"], "is_enabled": [0, 0]})
    assert season_phase_label(df) == "NBA"


def test_season_phase_empty():
    assert season_phase_label(pd.DataFrame()) == "NBA"


def test_season_phase_flag_value_is_na():
    df = pd.DataFrame({"flag": ["playoffs", "season"], "is_enabled": [pd.NA, 1]})
    assert season_phase_label(df) == "Regular season"


def test_season_phase_flag_non_integer_uses_bool_coercion():
    df = pd.DataFrame({"flag": ["playoffs", "season"], "is_enabled": ["x", 0]})
    assert season_phase_label(df) == "Playoffs"


def test_tab_label_no_badge():
    assert tab_label_with_badge("Overview", None) == "Overview"


def test_tab_label_with_badge():
    assert tab_label_with_badge("Schedule", 3) == "Schedule (3)"
