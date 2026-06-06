from __future__ import annotations

import pandas as pd


def feature_flag_enabled(feature_flags_df: pd.DataFrame | None, flag: str) -> bool:
    """True when ``flag`` is present and enabled in the feature_flags table."""
    if feature_flags_df is None or feature_flags_df.empty:
        return False
    flags = feature_flags_df.set_index("flag")["is_enabled"].to_dict()
    v = flags.get(flag)
    if v is None or pd.isna(v):
        return False
    try:
        return int(v) == 1
    except TypeError, ValueError:
        return bool(v)


def playoffs_enabled() -> bool:
    """Authoritative 'are we in the postseason' switch, read from feature_flags."""
    # Lazy import keeps the cache layer out of shell's import graph.
    from src.data_access.cache import get_table

    try:
        feature_flags_df = get_table("feature_flags")
    except KeyError:
        return False
    return feature_flag_enabled(feature_flags_df, "playoffs")


def season_phase_label(feature_flags_df: pd.DataFrame) -> str:
    if feature_flags_df is None or feature_flags_df.empty:
        return "NBA"
    if feature_flag_enabled(feature_flags_df, "playoffs"):
        return "Playoffs"
    if feature_flag_enabled(feature_flags_df, "season"):
        return "Regular season"
    return "NBA"


def tab_label_with_badge(title: str, count: int | None) -> str:
    """Plain string labels for dbc.Tab (composite Dash components are rejected as label)."""
    if count is None:
        return title
    return f"{title} ({count})"
