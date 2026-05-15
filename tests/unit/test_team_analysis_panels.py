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


def test_extract_eta_patterns():
    import src.team_analysis_panels as tap

    assert tap._extract_eta("") == "-"
    assert tap._extract_eta("   ") == "-"
    assert tap._extract_eta("Expected back today for practice") == "today"
    assert tap._extract_eta("Listed as day to day") == "day-to-day"
    assert tap._extract_eta("Will be re-evaluated Nov 12") == "re-eval Nov 12"
    assert tap._extract_eta("out 2-4 weeks") == "est. 2–4 wks"
    assert tap._extract_eta("miss 3 weeks") == "est. 3 wks"
    assert tap._extract_eta("return in 5 days") == "est. 5 days"
    assert tap._extract_eta("no timeline given") == "-"


def test_status_badge_classes():
    import src.team_analysis_panels as tap

    assert "out" in tap._status_badge_class("Out")
    assert "out" in tap._status_badge_class("out for season")
    assert "questionable" in tap._status_badge_class("Questionable")
    assert "questionable" in tap._status_badge_class("day to day")
    assert "probable" in tap._status_badge_class("Probable")
    assert "default" in tap._status_badge_class("GTD")


def test_transaction_category_and_highlight_and_date():
    import src.team_analysis_panels as tap
    from dash import html

    assert tap._transaction_category("two-way deal") == "2-WAY"
    assert tap._transaction_category("Player waived") == "WAIVE"
    assert tap._transaction_category("traded to East") == "TRADE"
    assert tap._transaction_category("trade: details") == "TRADE"
    assert tap._transaction_category("converted to standard") == "CONVERT"
    assert tap._transaction_category("signed a contract") == "SIGN"
    assert tap._transaction_category("released yesterday") == "REL"
    assert tap._transaction_category("random note") == "NOTE"

    parts = tap._highlight_transaction_text("The Raptors signed Player X.")
    assert any(isinstance(p, html.Span) and "signed" in str(p) for p in parts)
    plain = tap._highlight_transaction_text("no verb here")
    assert len(plain) == 1 and isinstance(plain[0], html.Span)
    assert plain[0].children == "no verb here" or plain[0].children == ("no verb here",)
    assert len(tap._highlight_transaction_text("signed and waived")) >= 3
    pre = tap._highlight_transaction_text("The club later signed him.")
    assert pre[0].children == "The club later "

    assert tap._format_tx_date(None) == "-"
    assert tap._format_tx_date(float("nan")) == "-"
    assert "Jan" in tap._format_tx_date(pd.Timestamp("2024-01-05"))


def test_filter_transactions_last_days_filters_window():
    import src.team_analysis_panels as tap

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-06-01", "2024-01-01"]),
            "transaction": [
                "The Toronto Raptors signed Player X.",
                "Old Toronto Raptors news from winter.",
            ],
        }
    )
    out = tap.filter_transactions_last_days(df, "Toronto Raptors", days=120)
    assert len(out) == 1
    assert "signed" in out.iloc[0]["transaction"].lower()


def test_filter_transactions_last_days_edge_cases():
    import src.team_analysis_panels as tap

    assert tap.filter_transactions_last_days(None, "Toronto Raptors").empty
    assert tap.filter_transactions_last_days(pd.DataFrame(), "Toronto Raptors").empty
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01"]),
            "transaction": ["Unrelated team note."],
        }
    )
    assert tap.filter_transactions_last_days(df, "Toronto Raptors").empty


def test_build_injury_panel_rows_line2_variants():
    import src.team_analysis_panels as tap

    rows = tap.build_injury_panel_rows(
        pd.DataFrame(
            [
                {
                    "player": "A",
                    "injury_status": "Probable",
                    "injury": "",
                    "injury_description": "Only desc",
                },
                {
                    "player": "B",
                    "injury_status": "Out",
                    "injury": "Knee",
                    "injury_description": "",
                },
            ]
        )
    )
    assert len(rows) == 2
