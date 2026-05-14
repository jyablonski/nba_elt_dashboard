def test_about_layout_importable():
    from src.pages.about import about_layout

    assert about_layout is not None


def test_overview_layout_importable():
    from src.pages.overview import overview_layout

    assert overview_layout is not None


def test_recent_games_layout_importable():
    from src.pages.recent_games import recent_games_layout

    assert recent_games_layout is not None


def test_schedule_layout_importable():
    from src.pages.schedule import schedule_layout

    assert schedule_layout is not None


def test_social_media_layout_importable():
    from src.pages.social_media_analysis import social_media_analysis_layout

    assert social_media_analysis_layout is not None


def test_team_analysis_layout_importable():
    from src.pages.team_analysis import team_analysis_layout

    assert team_analysis_layout is not None
