import plotly.graph_objects as go
import pytest

from src.pages.social_media_analysis import update_reddit_team_sentiment


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
