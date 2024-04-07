from datetime import datetime

import plotly.graph_objects as go
from src.pages.overview import (
    update_scoring_efficiency_plot,
    create_season_selector_dropdown,
)


def test_graph_regular_season():
    # Mocking the create_season_selector_dropdown function with a specific date
    dropdown = create_season_selector_dropdown(  # noqa
        current_date=datetime(2024, 3, 10).date()
    )

    output = update_scoring_efficiency_plot("Regular Season")

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == "Average PPG"
    assert output["layout"]["yaxis"]["title"]["text"] == "Average TS%"
    assert output["data"][0]["customdata"][0][0] == "Luka Doncic"
    assert output["data"][0]["customdata"][0][2] == 34.1


def test_graph_playoffs():
    # Mocking the create_season_selector_dropdown function with a specific date
    dropdown = create_season_selector_dropdown(  # noqa
        current_date=datetime(2024, 4, 20).date()
    )

    output = update_scoring_efficiency_plot("Playoffs")

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == "Average PPG"
    assert output["layout"]["yaxis"]["title"]["text"] == "Average TS%"
    assert output["data"][0]["customdata"][0][0] == "Joel Embiid"
    assert output["data"][0]["customdata"][0][2] == 27.3
