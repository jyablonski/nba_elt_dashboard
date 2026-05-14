"""Aggregations for the Social Media Analysis page (no DB changes; derived in-app)."""

from __future__ import annotations

from typing import Any

import pandas as pd


def normalized_daily_volume(
    time_series_df: pd.DataFrame,
    comments_df: pd.DataFrame,
) -> pd.DataFrame:
    """One row per day with column ``volume`` (league-wide from time series when possible)."""
    if time_series_df is not None and not time_series_df.empty:
        cols = {"scrape_date", "num_comments"}
        if cols.issubset(time_series_df.columns):
            out = (
                time_series_df.groupby("scrape_date", as_index=False)["num_comments"]
                .sum()
                .sort_values("scrape_date")
                .rename(columns={"num_comments": "volume"})
            )
            if not out.empty:
                return out
    if comments_df is None or comments_df.empty or "scrape_date" not in comments_df.columns:
        return pd.DataFrame(columns=["scrape_date", "volume"])
    out = (
        comments_df.groupby("scrape_date", as_index=False)
        .size()
        .rename(columns={"size": "volume"})
        .sort_values("scrape_date")
    )
    return out


def daily_weighted_sentiment(
    time_series_df: pd.DataFrame,
    comments_df: pd.DataFrame,
) -> pd.DataFrame:
    """One row per day: volume-weighted avg compound from time series, else mean from comments."""
    if time_series_df is not None and not time_series_df.empty:
        need = {"scrape_date", "num_comments", "avg_compound"}
        if need.issubset(time_series_df.columns):
            ts = time_series_df.copy()
            ts["weighted"] = ts["avg_compound"].astype(float) * ts["num_comments"].astype(float)
            g = ts.groupby("scrape_date", as_index=False).agg(
                w_sum=("weighted", "sum"),
                n=("num_comments", "sum"),
            )
            g["sentiment"] = g.apply(
                lambda r: float(r["w_sum"] / r["n"]) if r["n"] else 0.0,
                axis=1,
            )
            return g[["scrape_date", "sentiment"]].sort_values("scrape_date")
    if comments_df is None or comments_df.empty:
        return pd.DataFrame(columns=["scrape_date", "sentiment"])
    if "compound" not in comments_df.columns:
        return pd.DataFrame(columns=["scrape_date", "sentiment"])
    return (
        comments_df.groupby("scrape_date", as_index=False)["compound"]
        .mean()
        .rename(columns={"compound": "sentiment"})
        .sort_values("scrape_date")
    )


def top_flairs(comments_df: pd.DataFrame, n: int = 12) -> pd.DataFrame:
    if comments_df is None or comments_df.empty or "flair" not in comments_df.columns:
        return pd.DataFrame(columns=["flair", "count"])
    s = comments_df["flair"].fillna("").astype(str).str.strip()
    counts = s[s != ""].value_counts().head(n).reset_index()
    counts.columns = ["flair", "count"]
    return counts


def top_keywords(keywords_df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    if keywords_df is None or keywords_df.empty:
        return pd.DataFrame(columns=["word", "word_frequency"])
    if not {"word", "word_frequency"}.issubset(keywords_df.columns):
        return pd.DataFrame(columns=["word", "word_frequency"])
    return keywords_df.nlargest(n, "word_frequency")[["word", "word_frequency"]].copy()


def default_team(time_series_df: pd.DataFrame, fallback: str = "GSW") -> str:
    if time_series_df is None or time_series_df.empty:
        return fallback
    if "team" not in time_series_df.columns or "num_comments" not in time_series_df.columns:
        return fallback
    s = time_series_df.groupby("team", as_index=False)["num_comments"].sum()
    if s.empty:
        return fallback
    s = s.sort_values("num_comments", ascending=False)
    return str(s.iloc[0]["team"])


def snapshot_kpis(
    comments_df: pd.DataFrame,
    keywords_df: pd.DataFrame,
    aggs_df: pd.DataFrame,
) -> dict[str, Any]:
    """Scalar values for hero / KPI strip."""
    out: dict[str, Any] = {
        "reddit_total": None,
        "reddit_pct_diff": None,
        "avg_compound": None,
        "top_word": None,
        "top_word_freq": None,
        "distinct_flairs": None,
        "keyword_as_of": None,
    }
    if aggs_df is not None and not aggs_df.empty:
        row = aggs_df.iloc[0]
        if "reddit_tot_comments" in row.index:
            out["reddit_total"] = int(row["reddit_tot_comments"])
        if "reddit_pct_difference" in row.index:
            out["reddit_pct_diff"] = float(row["reddit_pct_difference"])
    if comments_df is not None and not comments_df.empty and "compound" in comments_df.columns:
        out["avg_compound"] = float(comments_df["compound"].astype(float).mean())
    if comments_df is not None and not comments_df.empty and "flair" in comments_df.columns:
        s = comments_df["flair"].fillna("").astype(str).str.strip()
        out["distinct_flairs"] = int(s[s != ""].nunique())
    if keywords_df is not None and not keywords_df.empty:
        kw = keywords_df.copy()
        if "frequency_rank" in kw.columns:
            kw["_rank"] = pd.to_numeric(kw["frequency_rank"], errors="coerce")
            kw = kw.sort_values(
                ["_rank", "word_frequency"], ascending=[True, False], na_position="last"
            )
        else:
            kw = kw.sort_values("word_frequency", ascending=False)
        top = kw.iloc[0]
        out["top_word"] = str(top["word"])
        out["top_word_freq"] = int(top["word_frequency"])
        if "analysis_date" in kw.columns and kw["analysis_date"].notna().any():
            out["keyword_as_of"] = kw["analysis_date"].max()
    return out
