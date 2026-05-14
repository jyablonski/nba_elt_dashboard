import pandas as pd

from src.team_analysis_panels import (
    build_injuries_panel,
    build_transactions_panel,
    filter_transactions_last_days,
)


def test_filter_transactions_last_days():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2023-07-20", "2023-01-01"]),
            "transaction": [
                "The Toronto Raptors signed X.",
                "The Toronto Raptors old news.",
            ],
        }
    )
    out = filter_transactions_last_days(df, "Toronto Raptors", days=90)
    assert len(out) == 1
    assert "signed" in out.iloc[0]["transaction"].lower()


def test_build_transactions_panel_renders():
    df = pd.DataFrame(
        [
            {
                "date": pd.Timestamp("2023-07-20"),
                "transaction": "The Toronto Raptors signed Player X.",
            }
        ]
    )
    panel = build_transactions_panel(df)
    s = str(panel)
    assert "TRANSACTIONS" in s
    assert "1 listed" in s
    assert "LAST 90 DAYS" not in s
    assert "stg.transactions_history" not in s
    assert "signed" in s.lower()


def test_build_transactions_panel_empty():
    df = pd.DataFrame(columns=["date", "transaction"])
    panel = build_transactions_panel(df)
    s = str(panel)
    assert "No recent transactions" in s
    assert "0 listed" in s


def test_build_injuries_panel_renders():
    df = pd.DataFrame(
        [
            {
                "team_acronym": "CHA",
                "team": "Charlotte Hornets",
                "player": "Test Player",
                "injury_status": "Out",
                "injury": "Knee",
                "injury_description": "Will be re-evaluated in two weeks.",
                "scrape_date": pd.Timestamp("2023-11-01"),
            }
        ]
    )
    panel = build_injuries_panel(df)
    s = str(panel)
    assert "ACTIVE INJURY REPORT" in s
    assert "1 listed" in s
    assert "Test Player" in s
    assert "team-panel-injury-team" not in s
