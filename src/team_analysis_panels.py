from __future__ import annotations

import math
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


def _to_float(value: Any) -> float | None:
    """Best-effort float coercion (None/NaN/blank -> None)."""
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return None if pd.isna(f) else f


def _fmt_millions(value: Any, *, signed: bool = False) -> str:
    f = _to_float(value)
    if f is None:
        return "-"
    millions = f / 1_000_000
    if signed:
        sign = "+" if millions >= 0 else "-"
        return f"{sign}${abs(millions):.1f}M"
    if millions < 0:
        return f"-${abs(millions):.1f}M"
    return f"${millions:.1f}M"


def _payroll_value_legend() -> html.Div:
    items = [
        ("Salary", "team-panel-payroll-swatch--salary"),
        ("Market value", "team-panel-payroll-swatch--market"),
        ("Surplus", "team-panel-payroll-swatch--surplus"),
        ("Overpay", "team-panel-payroll-swatch--overpay"),
    ]
    return html.Div(
        [
            html.Span(
                [
                    html.Span(className=f"team-panel-payroll-swatch {swatch}"),
                    html.Span(label, className="team-panel-payroll-legend-label"),
                ],
                className="team-panel-payroll-legend-item",
            )
            for label, swatch in items
        ],
        className="team-panel-payroll-legend",
    )


def _payroll_value_stat(label: str, value: str, sub: str, *, accent: str = "") -> html.Div:
    val_cls = "team-panel-payroll-stat-val" + (f" {accent}" if accent else "")
    return html.Div(
        [
            html.Div(label, className="team-panel-payroll-stat-label"),
            html.Div(value, className=val_cls),
            html.Div(sub, className="team-panel-payroll-stat-sub"),
        ],
        className="team-panel-payroll-stat",
    )


def _payroll_status(
    total: float,
    tax: float | None,
    first_apron: float | None,
    second_apron: float | None,
) -> tuple[str, str]:
    """Where the team's payroll sits relative to the cap thresholds (label, modifier)."""
    if second_apron is not None and total >= second_apron:
        return "2nd apron", "apron"
    if first_apron is not None and total >= first_apron:
        return "1st apron", "apron"
    if tax is not None and total >= tax:
        return "Above luxury tax", "tax"
    return "Below luxury tax", "under"


def _payroll_thresholds_bar(payroll: pd.Series) -> html.Div:
    """Horizontal track of payroll vs cap / luxury-tax / apron thresholds."""
    total = _to_float(payroll.get("total_payroll")) or 0.0
    cap = _to_float(payroll.get("salary_cap"))
    tax = _to_float(payroll.get("luxury_tax_threshold"))
    first_apron = _to_float(payroll.get("first_apron"))
    second_apron = _to_float(payroll.get("second_apron"))

    scale_max = second_apron or first_apron or (total * 1.1) or 1.0
    scale_max = max(scale_max, total)

    def _pct(value: float | None) -> float:
        if not value:
            return 0.0
        return max(0.0, min(100.0, value / scale_max * 100.0))

    over_tax = tax is not None and total > tax
    fill_cls = "team-panel-payroll-thresh-fill" + (
        " team-panel-payroll-thresh-fill--over" if over_tax else ""
    )

    markers: list[html.Div] = []
    for value, label in ((cap, "Cap"), (tax, "Tax")):
        if value is None:
            continue
        markers.append(
            html.Div(
                html.Span(
                    f"{label} {_fmt_millions(value)}",
                    className="team-panel-payroll-thresh-tick-label",
                ),
                className="team-panel-payroll-thresh-tick",
                style={"left": f"{_pct(value)}%"},
            )
        )

    status_label, status_mod = _payroll_status(total, tax, first_apron, second_apron)

    return html.Div(
        [
            html.Div(
                [
                    html.Div(className=fill_cls, style={"width": f"{_pct(total)}%"}),
                    *markers,
                ],
                className="team-panel-payroll-thresh-track",
            ),
            html.Div(
                [
                    html.Span(
                        f"scale $0 → {_fmt_millions(scale_max)} (second apron)",
                        className="team-panel-payroll-thresh-scale",
                    ),
                    html.Span(
                        status_label,
                        className=(
                            "team-panel-payroll-status "
                            f"team-panel-payroll-status--{status_mod}"
                        ),
                    ),
                ],
                className="team-panel-payroll-thresh-footer",
            ),
        ],
        className="team-panel-payroll-thresh",
    )


def _payroll_value_axis_max(players: pd.DataFrame) -> float:
    """Round the largest of salary / market value up to a clean $10M tick.

    Both the salary bar width and the market-value diamond position are mapped
    through this single $0 -> axis_max domain so the two encodings share one axis.
    """
    largest = 0.0
    for _, r in players.iterrows():
        salary = _to_float(r.get("salary_usd")) or 0.0
        surplus = (_to_float(r.get("production_minus_salary_pct")) or 0.0) * (
            _to_float(r.get("luxury_tax_threshold")) or 0.0
        )
        largest = max(largest, salary, salary + surplus)
    if largest <= 0:
        return 10_000_000.0
    step = 10_000_000.0
    return math.ceil(largest / step) * step


def _payroll_ruler_label(value: float) -> str:
    return "$0" if value <= 0 else f"${int(round(value / 1_000_000))}M"


def build_payroll_value_ruler(axis_max: float) -> html.Div:
    """$0 -> axis_max ruler, aligned to the bar track (same grid as player rows)."""
    step = 10_000_000.0
    n = max(1, int(round(axis_max / step)))
    ticks: list[html.Span] = []
    for i in range(n + 1):
        value = i * step
        pct = value / axis_max * 100.0 if axis_max else 0.0
        cls = "team-panel-payroll-ruler-tick"
        if i == 0:
            cls += " team-panel-payroll-ruler-tick--first"
        elif i == n:
            cls += " team-panel-payroll-ruler-tick--last"
        ticks.append(
            html.Span(_payroll_ruler_label(value), className=cls, style={"left": f"{pct}%"})
        )
    return html.Div(
        [
            html.Div(className="team-panel-payroll-cell-name"),
            html.Div(
                [html.Div(className="team-panel-payroll-ruler-line"), *ticks],
                className="team-panel-payroll-ruler-track",
            ),
            html.Div(className="team-panel-payroll-cell-salary"),
            html.Div(className="team-panel-payroll-cell-surplus"),
        ],
        className="team-panel-payroll-row team-panel-payroll-ruler",
    )


def build_payroll_value_rows(players: pd.DataFrame, axis_max: float) -> list[html.Div]:
    rows: list[html.Div] = []
    for _, r in players.iterrows():
        name = str(r.get("player_name", ""))
        position = str(r.get("position") or "").strip()
        age = _to_float(r.get("age"))
        salary = _to_float(r.get("salary_usd")) or 0.0
        lux = _to_float(r.get("luxury_tax_threshold")) or 0.0
        surplus = (_to_float(r.get("production_minus_salary_pct")) or 0.0) * lux
        market = salary + surplus

        # Both encodings map through the same $0 -> axis_max domain.
        salary_pct = max(0.0, min(100.0, salary / axis_max * 100.0)) if axis_max else 0.0
        market_pct = max(0.0, min(100.0, market / axis_max * 100.0)) if axis_max else 0.0
        is_surplus = surplus >= 0

        track_children: list[html.Div] = [
            html.Div(
                className="team-panel-payroll-bar",
                style={"width": f"{salary_pct}%"},
            )
        ]
        # Always bridge bar-end -> diamond so the gap (surplus or overpay) is visible.
        lo, hi = sorted((salary_pct, market_pct))
        if hi - lo > 0.05:
            connector_cls = "team-panel-payroll-connector " + (
                "team-panel-payroll-connector--surplus"
                if is_surplus
                else "team-panel-payroll-connector--overpay"
            )
            track_children.append(
                html.Div(
                    className=connector_cls,
                    style={"left": f"{lo}%", "width": f"{hi - lo}%"},
                )
            )
        diamond_cls = "team-panel-payroll-diamond " + (
            "team-panel-payroll-diamond--surplus"
            if is_surplus
            else "team-panel-payroll-diamond--overpay"
        )
        track_children.append(
            html.Div(className=diamond_cls, style={"left": f"{market_pct}%"})
        )

        meta_bits = " · ".join(b for b in (position, f"{int(age)}" if age else "") if b)
        surplus_cls = "team-panel-payroll-surplus " + (
            "team-panel-payroll-surplus--pos" if is_surplus else "team-panel-payroll-surplus--neg"
        )
        rows.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(name, className="team-panel-payroll-name"),
                            html.Span(meta_bits, className="team-panel-payroll-meta"),
                        ],
                        className="team-panel-payroll-player",
                    ),
                    html.Div(track_children, className="team-panel-payroll-track"),
                    html.Span(_fmt_millions(salary), className="team-panel-payroll-salary"),
                    html.Span(_fmt_millions(surplus, signed=True), className=surplus_cls),
                ],
                className="team-panel-payroll-row",
            )
        )
    return rows


def build_payroll_value_panel(
    payroll: pd.Series | None,
    players: pd.DataFrame,
    *,
    axis_max: float | None = None,
) -> html.Div:
    """Roster pay-vs-production panel: team payroll header + per-player surplus bars.

    ``axis_max`` lets callers pass a league-wide domain so the salary bars are
    directly comparable across all 30 teams; when omitted it falls back to this
    team's own roster max.
    """
    header = html.Div(
        [
            html.Span(
                "ROSTER · PAY VS. PRODUCTION VALUE", className="team-panel-eyebrow"
            ),
            _payroll_value_legend(),
        ],
        className="team-panel-header team-panel-payroll-header d-flex justify-content-between align-items-center gap-2 flex-wrap",
    )

    if players is None or players.empty:
        return html.Div(
            [
                header,
                html.Div(
                    "No payroll or player value data for this team.",
                    className="team-panel-empty small text-muted",
                ),
            ],
            className="team-panel team-panel--payroll",
        )

    players = players.sort_values("salary_usd", ascending=False, na_position="last")
    if axis_max is None:
        axis_max = _payroll_value_axis_max(players)

    summary: list[html.Div] = []
    if payroll is not None:
        total = _to_float(payroll.get("total_payroll"))
        tax = _to_float(payroll.get("luxury_tax_threshold"))
        roster_count = _to_float(payroll.get("roster_count"))
        vs_tax = (total - tax) if (total is not None and tax is not None) else None
        overpaid = [
            (_to_float(r.get("production_minus_salary_pct")) or 0.0)
            * (_to_float(r.get("luxury_tax_threshold")) or 0.0)
            for _, r in players.iterrows()
        ]
        overpaid_dollars = -sum(s for s in overpaid if s < 0)
        overpaid_count = sum(1 for s in overpaid if s < 0)

        summary = [
            _payroll_value_stat(
                "TEAM PAYROLL",
                _fmt_millions(total),
                f"{int(roster_count)} contracts" if roster_count else "-",
            ),
            _payroll_value_stat(
                "VS LUXURY TAX",
                _fmt_millions(vs_tax, signed=True) if vs_tax is not None else "-",
                f"{'over' if (vs_tax or 0) > 0 else 'under'} the {_fmt_millions(tax)} line"
                if tax is not None
                else "-",
                accent="team-panel-payroll-stat-val--neg"
                if (vs_tax or 0) > 0
                else "team-panel-payroll-stat-val--pos",
            ),
            _payroll_value_stat(
                "ABOVE FAIR VALUE",
                f"{overpaid_count} / {len(players)}",
                f"{_fmt_millions(overpaid_dollars)} committed above market",
                accent="team-panel-payroll-stat-val--neg",
            ),
        ]

    summary_section = html.Div(
        [
            html.Div(summary, className="team-panel-payroll-stats"),
            _payroll_thresholds_bar(payroll) if payroll is not None else html.Div(),
        ],
        className="team-panel-payroll-summary",
    )

    return html.Div(
        [
            header,
            summary_section,
            html.Div(
                [
                    build_payroll_value_ruler(axis_max),
                    *build_payroll_value_rows(players, axis_max),
                ],
                className="team-panel-body team-panel-payroll-body",
            ),
            html.Div(
                "Market value = share of team production × luxury-tax dollars. "
                "Surplus = market value − salary. Source · player_salary_value ⋈ team_payroll_summary.",
                className="team-panel-payroll-footnote small text-muted",
            ),
        ],
        className="team-panel team-panel--payroll",
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
