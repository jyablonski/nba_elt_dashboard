import pandas as pd

from src.social_media_insights import (
    daily_weighted_sentiment,
    default_team,
    normalized_daily_volume,
    snapshot_kpis,
    top_flairs,
    top_keywords,
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
    assert list(out["scrape_date"].dt.date) == [pd.Timestamp("2024-01-01").date(), pd.Timestamp("2024-01-02").date()]
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
    comments = pd.DataFrame(
        {"scrape_date": pd.to_datetime(["2024-01-01"]), "compound": [0.0]}
    )
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
