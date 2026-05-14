from __future__ import annotations

from typing import Any

from dash import dash_table

from src.config import BASE_TABLE_STYLE


def dark_datatable(
    *,
    columns: list[dict[str, Any]],
    data: list[dict[str, Any]],
    table_id: str,
    page_size: int = 15,
    **kwargs: Any,
) -> dash_table.DataTable:
    style_cell = {**BASE_TABLE_STYLE, **kwargs.pop("style_cell", {})}
    return dash_table.DataTable(
        id=table_id,
        columns=columns,
        data=data,
        style_cell=style_cell,
        page_size=page_size,
        **kwargs,
    )
