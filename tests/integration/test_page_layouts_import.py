from src.pages.about import about_layout
from src.pages.overview import overview_layout
from src.pages.recent_games import recent_games_layout
from src.pages.schedule import schedule_layout
from src.pages.social_media_analysis import social_media_analysis_layout
from src.pages.team_analysis import team_analysis_layout


def test_about_layout_importable():
    assert about_layout is not None


def test_overview_layout_importable():
    assert overview_layout() is not None


def test_recent_games_layout_importable():
    layout = recent_games_layout()
    assert layout is not None
    assert "recent-games-slate-bar" in str(layout)


def test_schedule_layout_importable():
    layout = schedule_layout()
    assert layout is not None
    flat = str(layout)
    assert "schedule-page" in flat
    assert "schedule-intel-bar" in flat


def test_social_media_layout_importable():
    assert social_media_analysis_layout() is not None


def test_team_analysis_layout_importable():
    layout = team_analysis_layout()
    assert layout is not None
    assert "team-analysis-page" in str(layout)
