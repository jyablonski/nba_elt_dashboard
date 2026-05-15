from unittest import mock

import pandas as pd

from src.social_media_insights import (
    _normalize_thread_url,
    _reddit_post_id_from_url,
    daily_weighted_sentiment,
    default_team,
    normalized_daily_volume,
    snapshot_kpis,
    thread_display_label,
    top_flair_share,
    top_flairs,
    top_flairs_over_time_matrix,
    top_keywords,
    top_threads_by_engagement,
)


def test_normalized_daily_volume_prefers_time_series():
    ts = pd.DataFrame(
        {
            "team": ["A", "A", "B"],
            "scrape_date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02"]),
            "num_comments": [10, 5, 7],
        }
    )
    comments = pd.DataFrame()
    out = normalized_daily_volume(ts, comments)
    assert list(out["scrape_date"].dt.date) == [
        pd.Timestamp("2024-01-01").date(),
        pd.Timestamp("2024-01-02").date(),
    ]
    assert out["volume"].tolist() == [15, 7]


def test_normalized_daily_volume_falls_back_to_comments():
    ts = pd.DataFrame()
    comments = pd.DataFrame(
        {
            "scrape_date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
            "compound": [0.1, -0.2],
        }
    )
    out = normalized_daily_volume(ts, comments)
    assert len(out) == 1
    assert int(out["volume"].iloc[0]) == 2


def test_daily_weighted_sentiment_weighted():
    ts = pd.DataFrame(
        {
            "scrape_date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
            "num_comments": [2, 2],
            "avg_compound": [0.0, 1.0],
        }
    )
    out = daily_weighted_sentiment(ts, pd.DataFrame())
    assert len(out) == 1
    assert abs(float(out["sentiment"].iloc[0]) - 0.5) < 1e-9


def test_top_flairs_and_keywords():
    c = pd.DataFrame({"flair": ["A", "A", "", None, "B"]})
    fl = top_flairs(c, n=2)
    assert set(fl["flair"]) == {"A", "B"}

    k = pd.DataFrame(
        {
            "word": ["x", "y"],
            "word_frequency": [5, 9],
            "frequency_rank": [2, 1],
        }
    )
    tk = top_keywords(k, n=1)
    assert tk.iloc[0]["word"] == "y"


def test_top_flair_share():
    c = pd.DataFrame({"flair": ["A", "A", "B", "", None]})
    pct, name = top_flair_share(c)
    assert name == "A"
    assert abs(pct - 40.0) < 1e-9


def test_top_flair_share_empty_paths():
    assert top_flair_share(None) == (None, None)
    assert top_flair_share(pd.DataFrame()) == (None, None)
    assert top_flair_share(pd.DataFrame({"compound": [1]})) == (None, None)
    blank = pd.DataFrame({"flair": ["", "  ", None, pd.NA]})
    assert top_flair_share(blank) == (None, None)

    c = pd.DataFrame(
        {
            "scrape_date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02"]),
            "flair": ["", "  ", None],
        }
    )
    assert top_flairs_over_time_matrix(c).empty


def test_top_flairs_over_time_matrix_all_dates_na():
    c = pd.DataFrame({"scrape_date": [pd.NaT, pd.NaT], "flair": ["A", "B"]})
    assert top_flairs_over_time_matrix(c).empty


def test_top_flairs_over_time_matrix_n_zero():
    c = pd.DataFrame({"scrape_date": pd.to_datetime(["2024-01-01"]), "flair": ["A"]})
    assert top_flairs_over_time_matrix(c, n=0).empty


def test_normalize_thread_url_strips_fragment_query_and_trailing_slash():
    u = "https://www.reddit.com/r/nba/comments/x/y/?ref=1#c"
    assert _normalize_thread_url(u) == "https://www.reddit.com/r/nba/comments/x/y"


def test_normalize_thread_url_empty_and_nan_sentinels():
    assert _normalize_thread_url("") == ""
    assert _normalize_thread_url("   ") == ""
    assert _normalize_thread_url("NaN") == ""
    assert _normalize_thread_url("none") == ""
    assert _normalize_thread_url("NAN") == ""


def test_reddit_post_id_from_url():
    full = "https://www.reddit.com/r/nba/comments/abc123xyz/some_slug/"
    assert _reddit_post_id_from_url(full) == "abc123xyz"
    assert _reddit_post_id_from_url("https://www.reddit.com/r/nba/comments") is None
    assert _reddit_post_id_from_url("https://example.com/no/such/path") is None


def test_thread_display_label_blank_base():
    assert thread_display_label("") == "thread"
    assert thread_display_label("   ") == "thread"


def test_thread_display_label_r_nba_post_id_only_path():
    """Slug branch uses post id segment when there is no title slug after it."""
    u = "https://www.reddit.com/r/nba/comments/onlypost12/"
    lab = thread_display_label(u)
    assert "onlypost12" in lab


def test_thread_display_label_r_nba_path_stops_at_comments_uses_base():
    """No segment after ``comments`` — inner if/elif both false, slug stays empty then ``slug or base``."""
    u = "https://www.reddit.com/r/nba/comments"
    lab = thread_display_label(u)
    assert "reddit.com" in lab


def test_thread_display_label_generic_url_last_path_segment():
    lab = thread_display_label("https://news.example.com/item/topic_here")
    assert "topic here" in lab.lower()


def test_thread_display_label_no_path_segments_uses_base():
    lab = thread_display_label("https://reddit.example")
    assert "reddit.example" in lab


def test_thread_display_label_truncates_long_slug():
    long_slug = "a" * 80
    u = f"https://www.reddit.com/r/nba/comments/z/{long_slug}/"
    lab = thread_display_label(u, max_len=20)
    assert len(lab) == 20
    assert lab.endswith("…")


def test_thread_display_label_urlparse_error_falls_back_to_base():
    with mock.patch("src.social_media_insights.urlparse", side_effect=ValueError("bad")):
        lab = thread_display_label("https://fallback.example/z")
    assert "fallback.example" in lab


def test_thread_display_label_r_nba_slug():
    u = "https://www.reddit.com/r/nba/comments/17gkehh/highlight_andre_drummond/"
    lab = thread_display_label(u)
    assert "highlight" in lab.lower()
    assert "drummond" in lab.lower()


def test_top_threads_by_engagement_all_urls_blank():
    df = pd.DataFrame({"url": ["", "  ", "nan", "NaN"], "score": [1, 2, 3, 4]})
    out = top_threads_by_engagement(df, n=10)
    assert out.empty
    assert list(out.columns) == ["thread_url", "label", "n_comments", "avg_score", "avg_compound"]


def test_top_threads_by_engagement_missing_score_and_compound_columns():
    df = pd.DataFrame({"url": ["https://www.reddit.com/r/nba/comments/aa/bb/"]})
    g = top_threads_by_engagement(df, n=5)
    assert len(g) == 1
    assert pd.isna(g.iloc[0]["avg_score"])
    assert pd.isna(g.iloc[0]["avg_compound"])


def test_top_threads_duplicate_label_without_post_id_skips_suffix():
    """Disambiguation loop runs but does not append when Reddit post id is absent."""
    df = pd.DataFrame(
        {
            "url": ["https://a.example/same", "https://b.example/same"],
            "score": [1, 2],
            "compound": [0.0, 0.0],
        }
    )
    g = top_threads_by_engagement(df, n=10)
    assert len(g) == 2
    assert (g["label"] == "same").all()


def test_top_threads_by_engagement_merges_url_variants():
    base = "https://www.reddit.com/r/nba/comments/abc123/my_slug/"
    df = pd.DataFrame(
        {
            "url": [base, base + "#c1", base + "?ref=1"],
            "score": [10, 20, 30],
            "compound": [0.1, 0.2, 0.3],
        }
    )
    g = top_threads_by_engagement(df, n=10)
    assert len(g) == 1
    assert int(g.iloc[0]["n_comments"]) == 3
    assert abs(float(g.iloc[0]["avg_score"]) - 20.0) < 1e-9
    assert abs(float(g.iloc[0]["avg_compound"]) - 0.2) < 1e-9


def test_top_threads_by_engagement_disambiguates_labels():
    u1 = "https://www.reddit.com/r/nba/comments/aaaaaa1/duplicate_title/"
    u2 = "https://www.reddit.com/r/nba/comments/bbbbbb2/duplicate_title/"
    df = pd.DataFrame(
        {
            "url": [u1, u1, u2, u2],
            "score": [1, 2, 3, 4],
            "compound": [0.0, 0.0, 0.0, 0.0],
        }
    )
    g = top_threads_by_engagement(df, n=10)
    assert len(g) == 2
    assert g["label"].nunique() == 2


def test_top_threads_by_engagement_respects_n():
    rows = []
    for i, n in enumerate(range(15, 0, -1)):
        u = f"https://www.reddit.com/r/nba/comments/p{i:03d}/title_{i}/"
        for _ in range(n):
            rows.append({"url": u, "score": 1, "compound": 0.0})
    df = pd.DataFrame(rows)
    g = top_threads_by_engagement(df, n=10)
    assert len(g) == 10
    assert int(g.iloc[0]["n_comments"]) == 15


def test_top_threads_by_engagement_empty():
    assert top_threads_by_engagement(None).empty
    assert top_threads_by_engagement(pd.DataFrame()).empty
    assert top_threads_by_engagement(pd.DataFrame({"compound": [1]})).empty


def test_top_flairs_over_time_matrix():
    c = pd.DataFrame(
        {
            "scrape_date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02"]),
            "flair": ["X", "X", "Y"],
        }
    )
    m = top_flairs_over_time_matrix(c, n=2)
    assert list(m.columns) == ["X", "Y"]
    assert int(m.loc[pd.Timestamp("2024-01-01"), "X"]) == 2
    assert int(m.loc[pd.Timestamp("2024-01-02"), "Y"]) == 1
    assert int(m.loc[pd.Timestamp("2024-01-02"), "X"]) == 0


def test_top_flairs_over_time_matrix_floors_to_calendar_day():
    """Same calendar day with different times-of-day must aggregate to one column."""
    c = pd.DataFrame(
        {
            "scrape_date": pd.to_datetime(
                ["2024-06-10 08:00:00", "2024-06-10 23:59:00", "2024-06-10 12:30:00"]
            ),
            "flair": ["Z", "Z", "Z"],
        }
    )
    m = top_flairs_over_time_matrix(c, n=1)
    assert len(m.index) == 1
    assert int(m.iloc[0, 0]) == 3


def test_top_flairs_over_time_matrix_empty():
    assert top_flairs_over_time_matrix(None).empty
    assert top_flairs_over_time_matrix(pd.DataFrame()).empty
    assert top_flairs_over_time_matrix(pd.DataFrame({"flair": ["a"]})).empty


def test_default_team():
    ts = pd.DataFrame({"team": ["X", "Y"], "num_comments": [1, 99]})
    assert default_team(ts, fallback="Z") == "Y"


def test_snapshot_kpis():
    comments = pd.DataFrame({"compound": [0.0, 0.2], "flair": ["A", "B"]})
    keywords = pd.DataFrame(
        {
            "word": ["w1", "w2"],
            "word_frequency": [10, 20],
            "frequency_rank": [2, 1],
            "analysis_date": pd.to_datetime(["2024-01-02", "2024-01-02"]),
        }
    )
    aggs = pd.DataFrame([{"reddit_tot_comments": 100, "reddit_pct_difference": -5.0}])
    s = snapshot_kpis(comments, keywords, aggs)
    assert s["reddit_total"] == 100
    assert s["top_word"] == "w2"
    assert s["distinct_flairs"] == 2


def test_normalized_daily_volume_ts_wrong_columns_falls_back_to_comments():
    ts = pd.DataFrame({"scrape_date": pd.to_datetime(["2024-01-01"])})
    comments = pd.DataFrame(
        {"scrape_date": pd.to_datetime(["2024-01-01", "2024-01-01"]), "compound": [0.0, 0.0]}
    )
    out = normalized_daily_volume(ts, comments)
    assert int(out["volume"].iloc[0]) == 2


def test_normalized_daily_volume_empty_ts_with_columns_uses_comments():
    ts = pd.DataFrame(columns=["scrape_date", "num_comments"])
    comments = pd.DataFrame({"scrape_date": pd.to_datetime(["2024-01-02"]), "compound": [0.1]})
    out = normalized_daily_volume(ts, comments)
    assert len(out) == 1
    assert int(out["volume"].iloc[0]) == 1


def test_normalized_daily_volume_no_usable_comments():
    out = normalized_daily_volume(pd.DataFrame(), None)
    assert list(out.columns) == ["scrape_date", "volume"]
    assert out.empty


def test_daily_weighted_sentiment_comments_mean_path():
    comments = pd.DataFrame(
        {"scrape_date": pd.to_datetime(["2024-01-01", "2024-01-01"]), "compound": [0.0, 0.4]}
    )
    out = daily_weighted_sentiment(pd.DataFrame(), comments)
    assert abs(float(out["sentiment"].iloc[0]) - 0.2) < 1e-9


def test_normalized_daily_volume_ts_groupby_empty_drops_to_comments():
    ts = pd.DataFrame({"scrape_date": [pd.NaT, pd.NaT], "num_comments": [1, 2]})
    comments = pd.DataFrame({"scrape_date": pd.to_datetime(["2024-01-01"]), "compound": [0.0]})
    out = normalized_daily_volume(ts, comments)
    assert len(out) == 1
    assert int(out["volume"].iloc[0]) == 1


def test_daily_weighted_sentiment_empty_comments_dataframe():
    ts = pd.DataFrame({"scrape_date": pd.to_datetime(["2024-01-01"]), "x": [1]})
    out = daily_weighted_sentiment(ts, pd.DataFrame())
    assert out.empty


def test_daily_weighted_sentiment_comments_missing_compound():
    comments = pd.DataFrame({"scrape_date": pd.to_datetime(["2024-01-01"])})
    out = daily_weighted_sentiment(pd.DataFrame(), comments)
    assert out.empty


def test_daily_weighted_sentiment_zero_weight_row():
    ts = pd.DataFrame(
        {
            "scrape_date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
            "num_comments": [0, 0],
            "avg_compound": [0.25, 0.75],
        }
    )
    out = daily_weighted_sentiment(ts, pd.DataFrame())
    assert float(out["sentiment"].iloc[0]) == 0.0


def test_daily_weighted_sentiment_ts_missing_weight_columns():
    ts = pd.DataFrame({"scrape_date": pd.to_datetime(["2024-01-01"]), "num_comments": [3]})
    comments = pd.DataFrame(
        {"scrape_date": pd.to_datetime(["2024-01-01", "2024-01-01"]), "compound": [-1.0, 1.0]}
    )
    out = daily_weighted_sentiment(ts, comments)
    assert float(out["sentiment"].iloc[0]) == 0.0


def test_top_flairs_empty_and_missing_column():
    assert top_flairs(None, n=5).empty
    assert top_flairs(pd.DataFrame(), n=5).empty
    assert top_flairs(pd.DataFrame({"compound": [1]}), n=5).empty


def test_top_keywords_empty_and_bad_columns():
    assert top_keywords(None, n=3).empty
    assert top_keywords(pd.DataFrame(), n=3).empty
    bad = pd.DataFrame({"word": ["a"], "nope": [1]})
    assert top_keywords(bad, n=3).empty


def test_default_team_fallback_paths():
    assert default_team(None, fallback="Z") == "Z"
    assert default_team(pd.DataFrame(), fallback="Z") == "Z"
    ts = pd.DataFrame({"team": ["A"], "wrong": [1]})
    assert default_team(ts, fallback="Z") == "Z"
    ts_empty = pd.DataFrame({"team": pd.Series(dtype=str), "num_comments": pd.Series(dtype=int)})
    assert default_team(ts_empty, fallback="Z") == "Z"
    ts_nan_team = pd.DataFrame({"team": [float("nan"), float("nan")], "num_comments": [1, 2]})
    assert default_team(ts_nan_team, fallback="Z") == "Z"


def test_snapshot_kpis_partial_inputs():
    s = snapshot_kpis(
        pd.DataFrame({"compound": [0.5]}),
        pd.DataFrame({"word": ["hi"], "word_frequency": [3]}),
        pd.DataFrame([{"other": 1}]),
    )
    assert s["reddit_total"] is None
    assert s["avg_compound"] == 0.5
    assert s["top_word"] == "hi"
    assert s["keyword_as_of"] is None

    s2 = snapshot_kpis(
        pd.DataFrame(),
        pd.DataFrame(
            {
                "word": ["a", "b"],
                "word_frequency": [1, 9],
                "analysis_date": pd.to_datetime(["2024-01-01", pd.NaT]),
            }
        ),
        pd.DataFrame(),
    )
    assert s2["top_word"] == "b"
    assert pd.notna(s2["keyword_as_of"])


def test_snapshot_kpis_no_flair_column():
    s = snapshot_kpis(pd.DataFrame({"compound": [0.1]}), pd.DataFrame(), pd.DataFrame())
    assert s["distinct_flairs"] is None
