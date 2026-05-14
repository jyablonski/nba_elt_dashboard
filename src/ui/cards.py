from __future__ import annotations

from collections.abc import Iterable

from dash import html


def kpi_card(content: Iterable, class_name: str = "kpi-card") -> html.Div:
    return html.Div(list(content), className=class_name)
