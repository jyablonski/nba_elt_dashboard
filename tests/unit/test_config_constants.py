from src.config import CUSTOM_COLORS, SINGLE_BAR_COLOR


def test_custom_colors_nonempty():
    assert len(CUSTOM_COLORS) >= 4
    assert all(isinstance(c, str) and c.startswith("#") for c in CUSTOM_COLORS)


def test_single_bar_color():
    assert SINGLE_BAR_COLOR.startswith("#")
