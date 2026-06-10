from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class GameCardSpec:
    game_description: str
    away_abbr: str
    home_abbr: str
    away_pts: int
    home_pts: int
    winner_abbr: str
    margin: int
    away_logo: str
    home_logo: str
    series_round: str | None = None
    series_status: str | None = None
    series_game_number: int | None = None


def _clean_str(raw: Any) -> str | None:
    """Normalize an optional text cell to a non-empty string, else None."""
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return None
    s = str(raw).strip()
    return s or None


def _clean_int(raw: Any) -> int | None:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return None
    try:
        return int(float(raw))
    except TypeError, ValueError:
        return None


def _teams_row_for_matchup(teams_df: pd.DataFrame, home: str, away: str) -> pd.Series | None:
    if teams_df is None or teams_df.empty:
        return None
    mask = teams_df.apply(lambda r: {r["team"], r["opponent"]} == {home, away}, axis=1)
    hit = teams_df.loc[mask]
    if hit.empty:
        return None
    return hit.iloc[0]


def build_game_card_specs(pbp_df: pd.DataFrame, teams_df: pd.DataFrame) -> list[GameCardSpec]:
    if pbp_df is None or pbp_df.empty:
        return []
    out: list[GameCardSpec] = []
    for desc in pbp_df["game_description"].drop_duplicates():
        sub = pbp_df[pbp_df["game_description"] == desc]
        row0 = sub.iloc[0]
        home = str(row0["home_team"])
        away = str(row0["away_team"])
        # Final line score: max total points (avoids jump ball / duplicate-clock rows at 0–0).
        sh = pd.to_numeric(sub["score_home"], errors="coerce").fillna(0)
        sa = pd.to_numeric(sub["score_away"], errors="coerce").fillna(0)
        sub = sub.assign(_tot_pts=sh + sa)
        mx = sub["_tot_pts"].max()
        candidates = sub.loc[sub["_tot_pts"] == mx]
        last = candidates.iloc[-1]
        home_pts = int(float(pd.to_numeric(last["score_home"], errors="coerce") or 0))
        away_pts = int(float(pd.to_numeric(last["score_away"], errors="coerce") or 0))
        wn = last.get("winning_team")
        if pd.notna(wn) and str(wn).strip():
            winner_abbr = str(wn).strip()
        else:
            winner_abbr = home if home_pts > away_pts else away
        margin = abs(home_pts - away_pts)
        away_logo = f"logos/{away.lower()}.png"
        home_logo = f"logos/{home.lower()}.png"
        series_round = None
        series_status = None
        series_game_number = None
        tr = _teams_row_for_matchup(teams_df, home, away)
        if tr is not None:
            series_round = _clean_str(tr.get("series_round"))
            series_status = _clean_str(tr.get("series_status"))
            series_game_number = _clean_int(tr.get("series_game_number"))
            margin = abs(int(tr["mov"]))
            hteam = str(tr["home_team"])
            win = str(tr["team"])
            if hteam == home:
                if win == home:
                    away_logo, home_logo = str(tr["opp_logo"]), str(tr["team_logo"])
                else:
                    away_logo, home_logo = str(tr["team_logo"]), str(tr["opp_logo"])
            else:
                away_logo, home_logo = str(tr["team_logo"]), str(tr["opp_logo"])
        out.append(
            GameCardSpec(
                game_description=str(desc),
                away_abbr=away,
                home_abbr=home,
                away_pts=away_pts,
                home_pts=home_pts,
                winner_abbr=winner_abbr,
                margin=margin,
                away_logo=away_logo,
                home_logo=home_logo,
                series_round=series_round,
                series_status=series_status,
                series_game_number=series_game_number,
            )
        )
    return out


def biggest_scoring_run(
    pbp_events: pd.DataFrame,
    *,
    min_net: int = 8,
    max_side: int = 30,
    max_span_minutes: float = 6.0,
    max_loser_ratio: float = 0.40,
) -> dict[str, Any] | None:
    """Find the winning team's most impactful concentrated scoring run.

    Scans the game's scoring events and returns the contiguous stretch that
    maximizes the winner's net advantage (e.g. a 16-3 run), bounded so it reads
    as a *clean run* rather than "outscored over a half":

    - ``min_net``: lower bound on (winner_pts - loser_pts). Surfaces an 8-0 in a
      close game while rejecting a 17-14 (net 3).
    - ``max_side``: cap on points per side, so neither number balloons past ~30.
    - ``max_span_minutes``: cap on the run's game-clock duration, keeping it a
      concentrated burst instead of a slow grind across two quarters.
    - ``max_loser_ratio``: cap on loser_pts / winner_pts. Without it, maximizing
      net surfaces choppy "24-13" stretches (opponent share 0.54) that are really
      just trading baskets. At 0.40 a 22-8 (0.36) survives but a 24-13 does not.

    The optimal window always starts and ends on a winner basket (a trailing
    opponent score only drags net down), so the opponent's points sit *inside*
    the run -- exactly how a "16-3" is described colloquially.

    A run is **always** returned for any game the winner actually scored in: when
    no stretch clears every bound (e.g. a low-scoring defensive game with no real
    run), the best concentrated net window is returned with ``qualified=False``
    so callers can still label it. ``None`` only comes back for empty/invalid data
    or a tie/unknown winner.

    Returns a dict describing the run (winner-first label, team color, the
    ``time_remaining_final`` span so the caller can band/annotate the plot, and a
    ``qualified`` flag), or ``None``.
    """
    needed = {
        "time_remaining_final",
        "score_home",
        "score_away",
        "home_team",
        "away_team",
        "winning_team",
    }
    if pbp_events is None or pbp_events.empty or not needed <= set(pbp_events.columns):
        return None

    g = pbp_events.sort_values("time_remaining_final", ascending=False).reset_index(drop=True)

    winners = g["winning_team"].dropna().astype(str)
    winners = winners[winners.str.upper() != "TIE"]
    if winners.empty:
        return None
    winner = winners.iloc[0]
    home = str(g["home_team"].iloc[0])
    winner_is_home = winner == home

    sh = pd.to_numeric(g["score_home"], errors="coerce").ffill().fillna(0)
    sa = pd.to_numeric(g["score_away"], errors="coerce").ffill().fillna(0)
    dh = sh.diff().fillna(sh).clip(lower=0)
    da = sa.diff().fillna(sa).clip(lower=0)
    win_pts = (dh if winner_is_home else da).to_numpy()
    los_pts = (da if winner_is_home else dh).to_numpy()

    scoring = (win_pts > 0) | (los_pts > 0)
    if not scoring.any():
        return None
    wp = win_pts[scoring]
    lp = los_pts[scoring]
    ev = g.loc[scoring].reset_index(drop=True)
    tr = pd.to_numeric(ev["time_remaining_final"], errors="coerce").to_numpy()

    n = len(ev)
    # Two candidates, both bounded by side/span and bookended by a winner basket:
    #   strict  -> also clears min_net and the loser-ratio cap (a "clean" run)
    #   fallback -> best net window regardless, so we always have something to show
    best_strict: tuple[float, ...] | None = None
    best_strict_ij: tuple[int, int] | None = None
    best_fallback: tuple[float, ...] | None = None
    best_fallback_ij: tuple[int, int] | None = None
    for i in range(n):
        if wp[i] == 0:
            continue
        w = 0.0
        loss = 0.0
        for j in range(i, n):
            w += wp[j]
            loss += lp[j]
            if w > max_side or loss > max_side:
                break
            span = tr[i] - tr[j]
            if span > max_span_minutes:
                break
            if wp[j] == 0:
                continue
            net = w - loss
            # Max net, then bigger winner number, then fewer opponent points,
            # then the tighter (shorter) burst.
            key = (net, w, -loss, -span)
            if best_fallback is None or key > best_fallback:
                best_fallback = key
                best_fallback_ij = (i, j)
            if net < min_net or loss > max_loser_ratio * w:
                continue
            if best_strict is None or key > best_strict:
                best_strict = key
                best_strict_ij = (i, j)

    qualified = best_strict_ij is not None
    best_ij = best_strict_ij if qualified else best_fallback_ij
    if best_ij is None:
        return None

    i, j = best_ij
    win_total = int(wp[i : j + 1].sum())
    los_total = int(lp[i : j + 1].sum())
    color_col = "home_primary_color" if winner_is_home else "away_primary_color"
    win_color = str(ev[color_col].iloc[i]) if color_col in ev.columns else None

    return {
        "winner": winner,
        "win_pts": win_total,
        "los_pts": los_total,
        "label": f"{win_total}-{los_total}",
        "qualified": qualified,
        "win_color": win_color,
        # x-axis (time_remaining_final) bounds of the run; x is reversed on the plot.
        "x_start": float(tr[i]),
        "x_end": float(tr[j]),
        "quarter_start": str(ev["quarter"].iloc[i]) if "quarter" in ev.columns else None,
        "quarter_end": str(ev["quarter"].iloc[j]) if "quarter" in ev.columns else None,
        "clock_start": str(ev["time_quarter"].iloc[i]) if "time_quarter" in ev.columns else None,
        "clock_end": str(ev["time_quarter"].iloc[j]) if "time_quarter" in ev.columns else None,
    }


def pbp_flow_stats(pbp_events: pd.DataFrame) -> dict[str, Any]:
    """Stats for the selected game's PBP event frame (transformed)."""
    empty: dict[str, Any] = {
        "max_lead": "-",
        "lead_changes": "-",
        "ties": "-",
        "swing": "-",
        "plays": "-",
    }
    if pbp_events is None or pbp_events.empty or "margin_score" not in pbp_events.columns:
        return empty
    sub = pbp_events.sort_values("time_remaining_final", ascending=False)
    m = sub["margin_score"].astype(float).to_numpy()
    max_lead = int(np.nanmax(np.abs(m)))
    sign = np.sign(m)
    changes = int((sign[1:] != sign[:-1]).sum()) if len(sign) > 1 else 0
    ties = int(np.sum(m == 0))
    m_time = sub.sort_values("time_remaining_final")["margin_score"].astype(float)
    dm = m_time.diff().abs().dropna()
    swing = int(dm.max()) if not dm.empty else "-"
    return {
        "max_lead": max_lead,
        "lead_changes": changes,
        "ties": ties,
        "swing": swing,
        "plays": len(sub),
    }
