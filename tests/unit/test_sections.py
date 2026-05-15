from dash import html

from src.ui.sections import page_hero, section_header


def test_page_hero_minimal():
    h = page_hero("T")
    assert "T" in str(h)
    assert "text-center" in h.className


def test_page_hero_with_meta():
    h = page_hero(
        "T",
        kicker="K",
        subtitle="S",
        meta=[html.Span("meta")],
    )
    assert "K" in str(h) and "meta" in str(h)


def test_page_hero_with_title_meta():
    h = page_hero(
        "T",
        title_meta=[html.Span("logo", id="hero-logo")],
    )
    s = str(h)
    assert "T" in s and "hero-logo" in s


def test_section_header_with_aside():
    s = section_header("Main", aside="note")
    assert "Main" in str(s) and "note" in str(s)
