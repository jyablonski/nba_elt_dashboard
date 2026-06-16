import pandas as pd
from dash import html

import src.team_analysis_panels as tap
from src.team_analysis_panels import (
    build_injuries_panel,
    build_payroll_value_panel,
    build_transactions_panel,
    filter_transactions_last_days,
)


def _payroll_players_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "player_name": "Star Guard",
                "position": "PG",
                "age": 24,
                "salary_usd": 45_900_000,
                "luxury_tax_threshold": 187_895_000,
                "production_minus_salary_pct": -0.0743,
            },
            {
                "player_name": "Value Wing",
                "position": "SF",
                "age": 23,
                "salary_usd": 12_600_000,
                "luxury_tax_threshold": 187_895_000,
                "production_minus_salary_pct": 0.0829,
            },
        ]
    )


def _payroll_row() -> pd.Series:
    return pd.Series(
        {
            "team": "CHA",
            "total_payroll": 171_100_000,
            "roster_count": 15,
            "salary_cap": 154_647_000,
            "luxury_tax_threshold": 187_895_000,
            "first_apron": 195_945_000,
            "second_apron": 207_824_000,
        }
    )


def test_fmt_millions_variants():
    assert tap._fmt_millions(45_900_000) == "$45.9M"
    assert tap._fmt_millions(-16_800_000) == "-$16.8M"
    assert tap._fmt_millions(13_100_000, signed=True) == "+$13.1M"
    assert tap._fmt_millions(-1_000_000, signed=True) == "-$1.0M"
    assert tap._fmt_millions(None) == "-"


def test_build_payroll_value_panel_renders():
    panel = build_payroll_value_panel(_payroll_row(), _payroll_players_df())
    s = str(panel)
    assert "PAY VS. PRODUCTION VALUE" in s
    assert "TEAM PAYROLL" in s
    assert "$171.1M" in s
    assert "VS LUXURY TAX" in s
    assert "Star Guard" in s
    assert "Value Wing" in s
    # one overpaid, one surplus player
    assert "team-panel-payroll-diamond--overpay" in s
    assert "team-panel-payroll-diamond--surplus" in s
    # ruler with a $0 origin
    assert "team-panel-payroll-ruler" in s
    assert "$0" in s
    # both surplus and overpay players get a connector to their diamond
    assert "team-panel-payroll-connector--surplus" in s
    assert "team-panel-payroll-connector--overpay" in s


def test_payroll_value_shared_axis_widths():
    """Bar width and diamond left both map through the same axis_max domain."""
    players = _payroll_players_df()
    axis_max = tap._payroll_value_axis_max(players)
    # $45.9M salary on a $50M axis (rounded up to $10M step) -> 91.8%
    assert axis_max == 50_000_000
    rows = tap.build_payroll_value_rows(players, axis_max)
    star_track = rows[0].children[1].children
    bar_style = star_track[0].style
    assert bar_style["width"] == f"{45_900_000 / axis_max * 100}%"


def test_payroll_value_panel_uses_supplied_axis_max():
    """A league-wide axis_max overrides this team's own roster max for comparability."""
    panel = build_payroll_value_panel(_payroll_row(), _payroll_players_df(), axis_max=60_000_000)
    s = str(panel)
    # ruler reflects the supplied $60M domain, not the team's $50M roster max
    assert "$60M" in s
    # $45.9M salary bar mapped through the $60M domain
    assert f"{45_900_000 / 60_000_000 * 100}%" in s


def test_payroll_status_tiers():
    cap, tax, a1, a2 = 154_647_000, 187_895_000, 195_945_000, 207_824_000
    assert tap._payroll_status(150_000_000, tax, a1, a2) == ("Below luxury tax", "under")
    assert tap._payroll_status(190_000_000, tax, a1, a2) == ("Above luxury tax", "tax")
    assert tap._payroll_status(196_000_000, tax, a1, a2) == ("1st apron", "apron")
    assert tap._payroll_status(245_600_000, tax, a1, a2) == ("2nd apron", "apron")
    # missing thresholds fall through to the safe default
    assert tap._payroll_status(150_000_000, None, None, None) == ("Below luxury tax", "under")


def test_payroll_value_panel_shows_status_pill():
    panel = build_payroll_value_panel(_payroll_row(), _payroll_players_df())
    s = str(panel)
    # _payroll_row() total $171.1M is under the $187.9M tax line
    assert "Below luxury tax" in s
    assert "team-panel-payroll-status--under" in s


def test_payroll_ruler_ticks_origin_and_max():
    ruler = tap.build_payroll_value_ruler(50_000_000)
    track = ruler.children[1]
    ticks = track.children[1:]  # first child is the baseline line
    assert ticks[0].children == "$0"
    assert ticks[0].style["left"] == "0.0%"
    assert ticks[-1].children == "$50M"
    assert ticks[-1].style["left"] == "100.0%"


def test_build_payroll_value_panel_empty():
    panel = build_payroll_value_panel(None, pd.DataFrame())
    s = str(panel)
    assert "PAY VS. PRODUCTION VALUE" in s
    assert "No payroll or player value data" in s


def test_build_payroll_value_panel_players_without_payroll_header():
    """Missing team_payroll_summary row still renders the per-player bars."""
    panel = build_payroll_value_panel(None, _payroll_players_df())
    s = str(panel)
    assert "Star Guard" in s
    assert "TEAM PAYROLL" not in s


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
    assert "out" in tap._status_badge_class("Out")
    assert "out" in tap._status_badge_class("out for season")
    assert "questionable" in tap._status_badge_class("Questionable")
    assert "questionable" in tap._status_badge_class("day to day")
    assert "probable" in tap._status_badge_class("Probable")
    assert "default" in tap._status_badge_class("GTD")


def test_transaction_category_and_highlight_and_date():
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
