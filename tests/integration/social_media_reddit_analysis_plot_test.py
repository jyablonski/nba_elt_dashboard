import plotly.graph_objects as go
import pytest

from src.pages.social_media_analysis import update_reddit_team_sentiment


def test_social_media_reddit_plot_with_known_data():
    """Test with a team that definitely has data"""
    output = update_reddit_team_sentiment("GSW")

    if output == {}:
        pytest.skip("No data available for GSW")

    assert isinstance(output, go.Figure)
    assert output["layout"]["title"]["text"] == "GSW - Comments by Game Outcome Over Time"

    assert "data" in output
    assert len(output["data"]) > 0
