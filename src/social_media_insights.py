"""Aggregations for the Social Media Analysis page (no DB changes; derived in-app)."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse, unquote

import pandas as pd


def _normalize_thread_url(url: object) -> str:
    s = str(url).strip()
    if not s or s.lower() in ("nan", "none"):
        return ""
    s = s.split("#", 1)[0]
    if "?" in s:
        s = s.split("?", 1)[0]
    return s.rstrip("/")


def _reddit_post_id_from_url(url: str) -> str | None:
    parts = [p for p in urlparse(url).path.strip("/").split("/") if p]
    if "comments" in parts:
        i = parts.index("comments")
        if i + 1 < len(parts):
            return parts[i + 1]
    return None


def thread_display_label(url: object, max_len: int = 52) -> str:
    """Human-readable title-ish string from a Reddit thread URL path."""
    base = _normalize_thread_url(url)
    if not base:
        return "thread"
    try:
        parts = [p for p in urlparse(base).path.strip("/").split("/") if p]
        slug = ""
        if len(parts) >= 2 and parts[0] == "r" and parts[1] == "nba" and "comments" in parts:
            i = parts.index("comments")
            if i + 2 < len(parts):
                slug = unquote(parts[i + 2]).replace("_", " ")
            elif i + 1 < len(parts):
                slug = unquote(parts[i + 1])
        elif parts:
            slug = unquote(parts[-1]).replace("_", " ")
        else:
            slug = base
    except TypeError, ValueError, IndexError:
        slug = base
    slug = (slug or base).strip() or "thread"
    return (slug[: max_len - 1] + "…") if len(slug) > max_len else slug


def _disambiguate_thread_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Append short post id when two threads share the same display label."""
    out = df.copy()
    dup = out["label"].duplicated(keep=False)
    if not dup.any():
        return out
    for idx in out.index[dup]:
        pid = _reddit_post_id_from_url(str(out.at[idx, "thread_url"]))
        suffix = (pid or "")[:8]
        if suffix:
            out.at[idx, "label"] = f"{out.at[idx, 'label']} ({suffix})"
    return out


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


def top_flair_share(comments_df: pd.DataFrame | None) -> tuple[float | None, str | None]:
    """Most common non-empty flair: its count divided by total rows (incl. empty flair)."""
    if comments_df is None or comments_df.empty or "flair" not in comments_df.columns:
        return None, None
    s = comments_df["flair"].fillna("").astype(str).str.strip()
    flaired = s[s != ""]
    if flaired.empty:
        return None, None
    vc = flaired.value_counts()
    top_name = str(vc.index[0])
    return float(vc.iloc[0] / len(s) * 100), top_name


def top_flairs_over_time_matrix(comments_df: pd.DataFrame | None, n: int = 8) -> pd.DataFrame:
    """Wide counts: index ``scrape_date``, columns top-``n`` flairs (by total volume), sorted dates."""
    if comments_df is None or comments_df.empty:
        return pd.DataFrame()
    if not {"scrape_date", "flair"}.issubset(comments_df.columns):
        return pd.DataFrame()
    d = comments_df[["scrape_date", "flair"]].copy()
    # One bucket per calendar day - raw values may be datetimes with varying times-of-day,
    # which would create a useless heatmap x-axis (sub-ms zoom) if left unnormalized.
    d["scrape_date"] = pd.to_datetime(d["scrape_date"], errors="coerce").dt.floor("D")
    d = d[d["scrape_date"].notna()]
    d["flair"] = d["flair"].fillna("").astype(str).str.strip()
    d = d[d["flair"] != ""]
    if d.empty:
        return pd.DataFrame()
    top = d["flair"].value_counts().head(n).index.tolist()
    if not top:
        return pd.DataFrame()
    d = d[d["flair"].isin(top)]
    counts = d.groupby(["scrape_date", "flair"], as_index=False).size()
    pivot = counts.pivot(index="scrape_date", columns="flair", values="size").fillna(0)
    pivot = pivot.reindex(columns=top, fill_value=0).sort_index()
    return pivot


def top_threads_by_engagement(comments_df: pd.DataFrame | None, *, n: int = 10) -> pd.DataFrame:
    """One row per thread URL: comment count in sample, mean score, mean compound."""
    cols = ["thread_url", "label", "n_comments", "avg_score", "avg_compound"]
    if comments_df is None or comments_df.empty or "url" not in comments_df.columns:
        return pd.DataFrame(columns=cols)
    d = comments_df.copy()
    d["_tu"] = d["url"].map(_normalize_thread_url)
    d = d[d["_tu"] != ""]
    if d.empty:
        return pd.DataFrame(columns=cols)
    d["_score"] = pd.to_numeric(d["score"], errors="coerce") if "score" in d.columns else pd.NA
    if "compound" in d.columns:
        d["_compound"] = pd.to_numeric(d["compound"], errors="coerce")
    else:
        d["_compound"] = float("nan")
    g = d.groupby("_tu", as_index=False).agg(
        n_comments=("_tu", "size"),
        avg_score=("_score", "mean"),
        avg_compound=("_compound", "mean"),
    )
    g = g.rename(columns={"_tu": "thread_url"}).nlargest(n, "n_comments").reset_index(drop=True)
    g["label"] = g["thread_url"].map(thread_display_label)
    g = _disambiguate_thread_labels(g)
    return g[cols]


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
