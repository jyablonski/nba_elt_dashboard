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
