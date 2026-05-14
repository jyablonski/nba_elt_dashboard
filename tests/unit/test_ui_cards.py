from dash import html

from src.ui.cards import kpi_card


def test_kpi_card_wraps_children():
    inner = html.Span("x")
    card = kpi_card([inner], class_name="kpi-card")
    assert card.className == "kpi-card"
    assert len(card.children) == 1
