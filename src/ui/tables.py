from __future__ import annotations

from typing import Any

from dash import dash_table

from src.config import BASE_TABLE_STYLE

# Dash shows a "Toggle columns" control when hidden_columns is set; we hide it for dark tables.
_HIDE_COLUMN_TOGGLE_CSS: dict[str, Any] = {"selector": ".show-hide", "rule": "display: none"}


def dark_datatable(
    *,
    columns: list[dict[str, Any]],
    data: list[dict[str, Any]],
    table_id: str,
    page_size: int = 15,
    **kwargs: Any,
) -> dash_table.DataTable:
    style_cell = {**BASE_TABLE_STYLE, **kwargs.pop("style_cell", {})}
    user_css = kwargs.pop("css", None)
    if user_css is None:
        css: list[dict[str, Any]] = [_HIDE_COLUMN_TOGGLE_CSS]
    elif isinstance(user_css, list):
        css = [_HIDE_COLUMN_TOGGLE_CSS, *user_css]
    else:
        css = [_HIDE_COLUMN_TOGGLE_CSS, user_css]
    return dash_table.DataTable(
        id=table_id,
        columns=columns,
        data=data,
        style_cell=style_cell,
        page_size=page_size,
        css=css,
        **kwargs,
    )
