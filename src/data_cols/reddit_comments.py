from dash.dash_table import FormatTemplate

reddit_comments_columns = [
    dict(id="scrape_date", name=["", "Date"]),
    dict(id="author", name=["", "Author"]),
    dict(id="flair", name=["", "Flair"]),
    dict(id="comment", name=["", "Comment"]),
    dict(id="score", name=["", "Upvotes"]),
    dict(
        id="compound",
        name=["Sentiment Scores", "Compound"],
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(
        id="pos",
        name=["Sentiment Scores", "Pos"],
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(
        id="neu",
        name=["Sentiment Scores", "Neu"],
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(
        id="neg",
        name=["Sentiment Scores", "Neg"],
        type="numeric",
        format=FormatTemplate.percentage(1),
    ),
    dict(
        id="url",
        name=["", "URL"],
    ),
]
