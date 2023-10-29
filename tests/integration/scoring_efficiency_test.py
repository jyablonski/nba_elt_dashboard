import plotly.graph_objects as go


from src.pages.overview import update_graph

def test_graph_regular_season():
    output = update_graph("Regular Season")

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == "Average PPG"
    assert output["layout"]["yaxis"]["title"]["text"] == "Average TS%"
    assert output["data"][0]["customdata"][0][0] == "Nikola Jokic"
    assert output["data"][0]["customdata"][0][2] == 24.5

def test_graph_playoffs():
    output = update_graph("Playoffs")

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == "Average PPG"
    assert output["layout"]["yaxis"]["title"]["text"] == "Average TS%"
    assert output["data"][0]["customdata"][0][0] == 'Nikola Jokic'
    assert output["data"][0]["customdata"][0][2] == 30.0