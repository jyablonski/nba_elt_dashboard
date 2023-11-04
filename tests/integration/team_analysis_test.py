from datetime import date
import pytest

from src.pages.team_analysis import (
    update_mov,
    update_injuries,
    update_team_player_efficiency,
    update_transactions,
)


@pytest.mark.parametrize(
    "test_input,expected_output",
    [("Charlotte Hornets", date(2023, 4, 9)), ("Milwaukee Bucks", date(2023, 4, 26))],
)
def test_mov(test_input, expected_output):
    output = update_mov(test_input)

    assert output["layout"]["xaxis"]["title"]["text"] == "Date"
    assert output["layout"]["yaxis"]["title"]["text"] == "Margin of Victory"
    assert output["data"][0]["customdata"][0][0] == expected_output


@pytest.mark.parametrize(
    "test_input,expected_output",
    [
        ("Charlotte Hornets", "Frank Ntilikina"),
        ("Phoenix Suns", "Bradley Beal"),
    ],
)
def test_injuries(test_input, expected_output):
    output = update_injuries(test_input)

    assert output[0].data[0]["player"] == expected_output


@pytest.mark.parametrize(
    "test_input,expected_output",
    [
        ("Los Angeles Clippers", "Paul George"),
        ("Dallas Mavericks", "Luka Doncic"),
    ],
)
def test_team_player_efficiency(test_input, expected_output):
    output = update_team_player_efficiency(test_input)

    assert output["layout"]["xaxis"]["title"]["text"] == "Average PPG"
    assert output["layout"]["yaxis"]["title"]["text"] == "Average TS%"
    assert output["data"][0]["customdata"][0][0] == expected_output


@pytest.mark.parametrize(
    "test_input,expected_output",
    [
        (
            "Toronto Raptors",
            "The Toronto Raptors signed Gradey Dick to a multi-year contract.",
        ),
        (
            "Golden State Warriors",
            "The Golden State Warriors signed Brandin Podziemski to a multi-year contract.",
        ),
    ],
)
def test_transactions(test_input, expected_output):
    output = update_transactions(test_input)

    assert output[0].data[0]["transaction"] == expected_output
