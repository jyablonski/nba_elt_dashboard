import plotly.graph_objects as go
from dash import dash_table, html

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

    assert len(output.data) > 0
    assert output.data[0].type == "bar"
    assert output["data"][0]["customdata"] is not None


def test_mov_empty_team_dark_placeholder():
    """Teams with no MOV rows get a dark placeholder, not `{}` white canvas."""
    output = update_mov("Oklahoma City Thunder")

    assert isinstance(output, go.Figure)
    assert len(output.data) == 0
    assert output.layout.annotations
    assert "No margin-of-victory" in output.layout.annotations[0].text


def test_injuries():
    output = update_injuries("Charlotte Hornets")

    assert isinstance(output, html.Div)
    flat = str(output)
    assert "ACTIVE INJURY REPORT" in flat
    if "0 listed" not in flat:
        assert "Frank Ntilikina" in flat


def test_team_player_efficiency():
    output = update_team_player_efficiency("Los Angeles Clippers")

    assert isinstance(output, dash_table.DataTable)
    assert output.columns[0]["id"] == "player"
    assert len(output.data) > 0


def test_transactions():
    output = update_transactions("Toronto Raptors")

    assert isinstance(output, html.Div)
    flat = str(output)
    assert "TRANSACTIONS" in flat
    assert "LAST 90 DAYS" not in flat
    assert "stg.transactions_history" not in flat
    if "No recent" not in flat.lower():
        assert "waived" in flat.lower() or "Joe Wieskamp" in flat
