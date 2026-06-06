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
