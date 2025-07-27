import plotly.graph_objects as go


from src.pages.schedule import update_schedule_plot


def test_schedule_analysis_sos():
    output = update_schedule_plot("strength-of-schedule")

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == "% Games Below .500 Teams"
    assert output["layout"]["yaxis"]["title"]["text"] == "Team"
    assert output["data"][0]["customdata"][0][0] == "HOU"
    assert output["data"][0]["customdata"][0][1] == 0.268


def test_schedule_analysis_preseason_over_unders():
    output = update_schedule_plot("vegas-preseason-odds")

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == "Wins Differential"
    assert output["layout"]["yaxis"]["title"]["text"] == "Team"
    assert output["data"][0]["customdata"][0][0] == "UTA"
    assert output["data"][0]["customdata"][0][1] == -15.5


def test_schedule_analysis_team_comebacks():
    output = update_schedule_plot("team-comebacks")

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == "Net Comebacks"
    assert output["layout"]["yaxis"]["title"]["text"] == "Team"
    assert output["data"][0]["customdata"][0][0] == "WAS"
    assert output["data"][0]["customdata"][0][1] == 15
