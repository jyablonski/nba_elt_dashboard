from __future__ import annotations

import pandas as pd


def season_phase_label(feature_flags_df: pd.DataFrame) -> str:
    if feature_flags_df is None or feature_flags_df.empty:
        return "NBA"

    flags = feature_flags_df.set_index("flag")["is_enabled"].to_dict()

    def _on(name: str) -> bool:
        v = flags.get(name)
        if v is None or pd.isna(v):
            return False
        try:
            return int(v) == 1
        except TypeError, ValueError:
            return bool(v)

    if _on("playoffs"):
        return "Playoffs"
    if _on("season"):
        return "Regular season"
    return "NBA"


def tab_label_with_badge(title: str, count: int | None) -> str:
    """Plain string labels for dbc.Tab (composite Dash components are rejected as label)."""
    if count is None:
        return title
    return f"{title} ({count})"
