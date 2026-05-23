import plotly.graph_objects as go
import pytest

from src.pages.social_media_analysis import build_league_volume_figure, update_reddit_team_sentiment


def test_social_media_reddit_plot_with_known_data():
    """Test with a team that definitely has data"""
    output = update_reddit_team_sentiment("GSW")
    assert isinstance(output, go.Figure)
    if not output.data:
        pytest.skip("No data available for GSW")
    title = output["layout"]["title"]["text"]
    assert "GSW" in title and "prior game outcome" in title

    assert "data" in output
    assert len(output["data"]) > 0


def test_league_volume_moving_average_is_direct_labeled():
    output = build_league_volume_figure()
    if not output.data:
        pytest.skip("No league volume data available")

    assert output["layout"]["showlegend"] is False
    annotations = output["layout"]["annotations"]
    assert any("7-day moving avg" in a["text"] for a in annotations)
    label = next(a for a in annotations if "7-day moving avg" in a["text"])
    assert "━" in label["text"]
    assert label["xref"] == "paper"
    assert label["yref"] == "paper"
    assert label["x"] == 1
    assert label["y"] == 1
    assert output["layout"]["margin"]["r"] == 24
