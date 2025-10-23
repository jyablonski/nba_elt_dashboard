import plotly.graph_objects as go
from dash import dash_table

from src.pages.team_analysis import (
    update_mov,
    update_injuries,
    update_team_player_efficiency,
    update_transactions,
)


def test_mov():
    output = update_mov("Charlotte Hornets")

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == "Date"
    assert output["layout"]["yaxis"]["title"]["text"] == "Margin of Victory"

    if "data" in output and len(output["data"]) > 0:
        assert output["data"][0]["customdata"] is not None


def test_injuries():
    output = update_injuries("Charlotte Hornets")

    assert isinstance(output, dash_table.DataTable)

    if output.data and len(output.data) > 0:
        assert "player" in output.data[0]
        assert output.data[0]["player"] == "Frank Ntilikina"


def test_team_player_efficiency():
    output = update_team_player_efficiency("Los Angeles Clippers")

    assert isinstance(output, go.Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == "Average Points Per Game"
    assert output["layout"]["yaxis"]["title"]["text"] == "True Shooting %"

    if "data" in output and len(output["data"]) > 0:
        assert output["data"][0]["customdata"].all() is not None


def test_transactions():
    output = update_transactions("Toronto Raptors")

    assert isinstance(output, dash_table.DataTable)

    if output.data and len(output.data) > 0:
        assert "transaction" in output.data[0]
        assert output.data[0]["transaction"] == "The Toronto Raptors waived Joe Wieskamp."
