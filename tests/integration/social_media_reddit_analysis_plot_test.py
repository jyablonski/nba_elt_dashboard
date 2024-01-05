from datetime import datetime

import plotly.graph_objects as go
import pytest

from src.pages.social_media_analysis import update_reddit_team_sentiment


@pytest.mark.parametrize(
    "test_input,expected_output",
    [
        ("BKN", "W"),
        ("GSW", "NO GAME"),
        ("OKC", "NO GAME"),
    ],
)
def test_social_media_reddit_plot2(test_input, expected_output):
    current_date = datetime.now().date()
    output = update_reddit_team_sentiment(test_input)

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == ""
    assert output["layout"]["yaxis"]["title"]["text"] == "Number of Comments"
    assert output["data"][0]["customdata"][0][0] == current_date
    assert output["data"][0]["customdata"][0][2] == expected_output
