import plotly.graph_objects as go

from src.utils import generate_team_ratings_figure


def test_generate_team_ratings_figure(team_ratings_fixture):
    figure = generate_team_ratings_figure(df=team_ratings_fixture)

    assert isinstance(figure, go.Figure)
    assert figure["layout"]["xaxis"]["title"]["text"] == "Offensive Rating"
    assert figure["layout"]["yaxis"]["title"]["text"] == "Defensive Rating"
    assert figure["data"][0]["customdata"][0][0] == "Boston Celtics"
    assert figure["data"][0]["customdata"][0][2] == 111.5
