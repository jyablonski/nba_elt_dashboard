from dash.dash_table import FormatTemplate

reddit_comments_columns = [
    dict(id="scrape date", name="Date"),
    dict(id="author", name="User"),
    dict(id="flair", name="Flair"),
    dict(id="comment", name="Comment"),
    dict(id="score", name="Upvotes"),
    dict(
        id="compound",
        name="Compound Sentiment Score",
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(
        id="pos", name="Positive", type="numeric", format=FormatTemplate.percentage(1)
    ),
    dict(id="neu", name="Neutral", type="numeric", format=FormatTemplate.percentage(1)),
    dict(
        id="neg", name="Negative", type="numeric", format=FormatTemplate.percentage(1)
    ),
    dict(id="url", name="URL"),
]
