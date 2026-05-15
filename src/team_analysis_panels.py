"""Custom HTML panels for Team Analysis (injuries + transactions)."""

from __future__ import annotations

import re
from datetime import timedelta
from typing import Any

import pandas as pd
from dash import html


def _norm_status(raw: str) -> str:
    s = str(raw).strip().upper().replace(" ", " ")
    s = s.replace("DAY TO DAY", "DAY-TO-DAY")
    return s


def _status_badge_class(status: str) -> str:
    u = _norm_status(status)
    if "OUT FOR SEASON" in u or u == "OUT":
        return "team-panel-injury-badge team-panel-injury-badge--out"
    if "QUESTIONABLE" in u or "DAY-TO-DAY" in u or "DAY TO DAY" in u:
        return "team-panel-injury-badge team-panel-injury-badge--questionable"
    if "PROBABLE" in u:
        return "team-panel-injury-badge team-panel-injury-badge--probable"
    return "team-panel-injury-badge team-panel-injury-badge--default"


def _extract_eta(description: str) -> str:
    """Best-effort timeline from free-text injury blurbs."""
    if not description or not str(description).strip():
        return "-"
    t = str(description)
    if re.search(r"\btoday\b", t, re.I):
        return "today"
    if re.search(r"\bday[- ]to[- ]day\b", t, re.I):
        return "day-to-day"
    m = re.search(
        r"re-?evaluat[^.]*?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.,]*\s+\d{1,2}|\d{1,2}/\d{1,2})",
        t,
        re.I,
    )
    if m:
        return f"re-eval {m.group(1).strip()}"
    m = re.search(r"(\d+)\s*[-–]\s*(\d+)\s*weeks?", t, re.I)
    if m:
        return f"est. {m.group(1)}–{m.group(2)} wks"
    m = re.search(r"(\d+)\s*weeks?", t, re.I)
    if m:
        return f"est. {m.group(1)} wks"
    m = re.search(r"(\d+)\s*days?", t, re.I)
    if m:
        return f"est. {m.group(1)} days"
    return "-"


def build_injury_panel_rows(df: pd.DataFrame) -> list[html.Div]:
    rows: list[html.Div] = []
    for _, r in df.iterrows():
        player = str(r.get("player", ""))
        status = str(r.get("injury_status", ""))
        injury = str(r.get("injury", ""))
        desc = str(r.get("injury_description", ""))
        line2 = f"{injury} · {desc}" if injury and desc else (injury or desc)
        eta = _extract_eta(desc)
        rows.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(player, className="team-panel-injury-name"),
                                    html.Span(
                                        _norm_status(status), className=_status_badge_class(status)
                                    ),
                                ],
                                className="team-panel-injury-line1",
                            ),
                            html.Span(eta, className="team-panel-injury-eta small text-muted"),
                        ],
                        className="team-panel-injury-top d-flex justify-content-between align-items-start gap-2",
                    ),
                    html.Div(line2, className="team-panel-injury-line2 small text-muted"),
                ],
                className="team-panel-injury-row",
            )
        )
    return rows


def build_injuries_panel(df: pd.DataFrame) -> html.Div:
    n = len(df)
    body = (
        build_injury_panel_rows(df)
        if n
        else [html.Div("No injuries reported.", className="team-panel-empty small text-muted")]
    )
    return html.Div(
        [
            html.Div(
                [
                    html.Span("ACTIVE INJURY REPORT", className="team-panel-eyebrow"),
                    html.Span(f"{n} listed", className="team-panel-count small text-muted"),
                ],
                className="team-panel-header d-flex justify-content-between align-items-baseline",
            ),
            html.Div(body, className="team-panel-body"),
        ],
        className="team-panel team-panel--injuries",
    )


_VERB_PAT = re.compile(
    r"\b(signed|waived|traded|acquired|released|converted|exercised|declined|fired|hired)\b",
    re.IGNORECASE,
)


def _highlight_transaction_text(text: str) -> list[Any]:
    parts: list[Any] = []
    last = 0
    for m in _VERB_PAT.finditer(text):
        if m.start() > last:
            parts.append(html.Span(text[last : m.start()]))
        parts.append(html.Span(m.group(1), className="team-panel-tx-verb"))
        last = m.end()
    if last < len(text):
        parts.append(html.Span(text[last:]))
    return parts if parts else [html.Span(text)]


def _transaction_category(tx: str) -> str:
    t = tx.lower()
    if "two-way" in t or "two way" in t:
        return "2-WAY"
    if "waived" in t:
        return "WAIVE"
    if "traded" in t or "trade:" in t:
        return "TRADE"
    if "converted" in t:
        return "CONVERT"
    if "signed" in t:
        return "SIGN"
    if "released" in t:
        return "REL"
    return "NOTE"


def _format_tx_date(d: Any) -> str:
    if d is None or (isinstance(d, float) and pd.isna(d)):
        return "-"
    ts = pd.Timestamp(d)
    return ts.strftime("%b %d").replace(" 0", " ")


def build_transaction_rows(df: pd.DataFrame) -> list[html.Div]:
    rows: list[html.Div] = []
    for _, r in df.iterrows():
        tx = str(r.get("transaction", ""))
        d = r.get("date")
        rows.append(
            html.Div(
                [
                    html.Span(_format_tx_date(d), className="team-panel-tx-date"),
                    html.Div(
                        _highlight_transaction_text(tx),
                        className="team-panel-tx-desc flex-grow-1",
                    ),
                    html.Span(_transaction_category(tx), className="team-panel-tx-tag"),
                ],
                className="team-panel-tx-row d-flex align-items-baseline gap-2",
            )
        )
    return rows


def build_transactions_panel(df: pd.DataFrame) -> html.Div:
    n = len(df)
    body = (
        build_transaction_rows(df)
        if n
        else [html.Div("No recent transactions.", className="team-panel-empty small text-muted")]
    )
    return html.Div(
        [
            html.Div(
                [
                    html.Span("TRANSACTIONS", className="team-panel-eyebrow"),
                    html.Span(f"{n} listed", className="team-panel-count small text-muted"),
                ],
                className="team-panel-header d-flex justify-content-between align-items-baseline",
            ),
            html.Div(body, className="team-panel-body"),
        ],
        className="team-panel team-panel--transactions",
    )


def filter_transactions_last_days(
    transactions_df: pd.DataFrame,
    team_name: str,
    *,
    days: int = 90,
) -> pd.DataFrame:
    cols = ["date", "transaction"]
    if transactions_df is None or transactions_df.empty:
        return pd.DataFrame(columns=cols)
    sub = transactions_df.loc[
        transactions_df["transaction"]
        .astype(str)
        .str.contains(re.escape(team_name), case=False, na=False)
    ].copy()
    if sub.empty:
        return sub
    sub["date"] = pd.to_datetime(sub["date"], errors="coerce")
    sub = sub.dropna(subset=["date"])
    end = sub["date"].max()
    start = end - timedelta(days=days)
    return sub.loc[sub["date"] >= start].sort_values("date", ascending=False)
