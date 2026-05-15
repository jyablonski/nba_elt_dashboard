import plotly.graph_objects as go


from src.pages.recent_games import update_pbp_plot


# Denver Nuggets Vs. Miami Heat
def test_pbp_plot():
    output = update_pbp_plot("Atlanta Hawks Vs. Brooklyn Nets")
    first_play = "S. Dinwiddie makes 3-pt jump shot from 25 ft (assist by N. Claxton)"
    first_timestamp = "11:33"

    assert isinstance(output, go.Figure)
    assert output.layout.xaxis.title.text == "Quarter"
    tt = output.layout.xaxis.ticktext
    assert tt is not None and "Q1" in tt
    assert output["layout"]["yaxis"]["title"]["text"] == "Score Differential"
    title = output.layout.title
    assert title is None or getattr(title, "text", None) in (None, "")
    assert output["data"][0]["customdata"][0][0] == first_play
    assert output["data"][0]["customdata"][0][1] == first_timestamp


def test_pbp_plot_empty():
    output = update_pbp_plot("boo")

    assert output == {}
