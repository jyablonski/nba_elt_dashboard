import plotly.graph_objects as go


from src.pages.recent_games import update_data_table


# Denver Nuggets Vs. Miami Heat
def test_pbp_plot():
    output = update_data_table("Denver Nuggets Vs. Miami Heat")
    first_play = "B. Adebayo makes 2-pt dunk from 2 ft"
    first_timestamp = "11:39"

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == ""
    assert output["layout"]["yaxis"]["title"]["text"] == "Score Differential"
    assert output["data"][0]["customdata"][0][0] == first_play
    assert output["data"][0]["customdata"][0][1] == first_timestamp


def test_pbp_plot_empty():
    output = update_data_table("boo")

    assert list(output["data"][0]["customdata"]) == []
