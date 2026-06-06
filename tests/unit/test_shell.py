import pandas as pd

from src.shell import (
    feature_flag_enabled,
    playoffs_enabled,
    season_phase_label,
    tab_label_with_badge,
)


def _flags(playoffs: object) -> pd.DataFrame:
    return pd.DataFrame({"flag": ["season", "playoffs"], "is_enabled": [1, playoffs]})


def test_feature_flag_enabled_on():
    assert feature_flag_enabled(_flags(1), "playoffs") is True


def test_feature_flag_enabled_off():
    assert feature_flag_enabled(_flags(0), "playoffs") is False


def test_feature_flag_enabled_missing_flag():
    assert feature_flag_enabled(_flags(1), "nope") is False


def test_feature_flag_enabled_none_and_empty():
    assert feature_flag_enabled(None, "playoffs") is False
    assert feature_flag_enabled(pd.DataFrame(), "playoffs") is False


def test_feature_flag_enabled_na_value():
    assert feature_flag_enabled(_flags(pd.NA), "playoffs") is False


def test_feature_flag_enabled_non_integer_uses_bool_coercion():
    assert feature_flag_enabled(_flags("x"), "playoffs") is True


def test_playoffs_enabled_reads_feature_flags(monkeypatch):
    monkeypatch.setattr("src.data_access.cache.get_table", lambda name: _flags(1), raising=True)
    assert playoffs_enabled() is True

    monkeypatch.setattr("src.data_access.cache.get_table", lambda name: _flags(0), raising=True)
    assert playoffs_enabled() is False


def test_playoffs_enabled_missing_table_is_false(monkeypatch):
    def _raise(name):
        raise KeyError(name)

    monkeypatch.setattr("src.data_access.cache.get_table", _raise, raising=True)
    assert playoffs_enabled() is False


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
