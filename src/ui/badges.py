from __future__ import annotations

import dash_bootstrap_components as dbc


def tab_count_badge(count: int, *, class_name: str = "app-tab-badge") -> dbc.Badge:
    return dbc.Badge(str(count), pill=True, className=class_name, color="secondary")
