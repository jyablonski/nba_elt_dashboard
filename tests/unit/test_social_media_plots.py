import pandas as pd

from src.social_media_plots import top_threads_engagement_figure


def test_top_threads_engagement_figure():
    base = "https://www.reddit.com/r/nba/comments/abc123/thread_slug_here/"
    df = pd.DataFrame(
        {
            "url": [base, base + "?ref=share", base + "#comment-xyz"],
            "score": [10, 20, 30],
            "compound": [0.1, 0.2, 0.3],
        }
    )
    fig = top_threads_engagement_figure(df, n_threads=5)
    assert fig.data
    assert all(tr.type == "bar" for tr in fig.data)


def test_top_threads_engagement_empty():
    fig = top_threads_engagement_figure(pd.DataFrame())
    assert not fig.data


def test_top_threads_engagement_none():
    fig = top_threads_engagement_figure(None)
    assert not fig.data


def test_top_threads_engagement_missing_columns():
    fig = top_threads_engagement_figure(pd.DataFrame({"x": [1]}))
    assert not fig.data
