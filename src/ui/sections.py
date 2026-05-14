from __future__ import annotations

from collections.abc import Sequence

from dash import html
from dash.development.base_component import Component


def page_hero(
    title: str,
    *,
    kicker: str | None = None,
    subtitle: str | None = None,
    meta: Sequence | None = None,
) -> html.Div:
    children: list = []
    if kicker:
        children.append(
            html.Div(kicker, className="text-uppercase small app-hero-kicker mb-1"),
        )
    children.append(html.H1(title, className="app-hero-title mb-2"))
    if subtitle:
        children.append(html.P(subtitle, className="text-muted small mb-0"))
    if meta:
        children.append(html.Div(list(meta), className="mt-3"))
    return html.Div(children, className="app-page-hero py-3 text-center")


def section_header(title: str, aside: str | None = None) -> html.Div:
    row: list[Component] = [html.H4(title, className="mb-0")]
    if aside:
        row.append(html.Span(aside, className="text-muted small ms-2"))
    return html.Div(
        row,
        className="app-section-header d-flex flex-wrap align-items-baseline justify-content-center mb-3",
    )
