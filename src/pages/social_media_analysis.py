from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from src.data_cols.reddit_comments import reddit_comments_columns
from src.data import (
    reddit_comments_df,
    reddit_sentiment_time_series_df,
    social_media_aggs_df,
    team_names_abbreviations,
)

social_media_analysis_layout = html.Div(
    [
        # Single div to contain all four KPIs
        html.Div(
            [
                # KPI 1
                html.Div(
                    [
                        html.Div("Social Media Scraping", style={"fontSize": 24}),
                        # Add images for Reddit and Twitter
                        html.Div(
                            [
                                html.Img(
                                    src="../assets/reddit.png",
                                    style={"height": "75px", "width": "75px"},
                                ),
                                html.Img(
                                    src="../assets/twitter.png",
                                    style={"height": "75px", "width": "120px"},
                                ),
                            ]
                        ),
                    ],
                    className="kpi-box",
                ),
                # KPI 2
                html.Div(
                    [
                        # html.Div("KPI 2 Value", style={"fontSize": 24}),
                        # html.Div("KPI 2 Description"),
                        html.Div(
                            dcc.Dropdown(
                                id="social-media-selector",
                                options=[
                                    {"label": "Reddit", "value": "reddit"},
                                    {"label": "Twitter", "value": "twitter"},
                                ],
                                value="reddit",
                                clearable=False,
                                style={"width": "500px"},
                            ),
                        ),
                    ],
                    className="kpi-box",
                ),
                # KPI 3
                html.Div(
                    [
                        html.Div(
                            social_media_aggs_df["reddit_tot_comments"][0],
                            style={"fontSize": 24},
                        ),
                        html.Div("Total Reddit Comments Scraped"),
                        html.Div(
                            f"{social_media_aggs_df['reddit_pct_difference'][0]}% difference from average"
                        ),
                    ],
                    className="kpi-box",
                ),
                # KPI 4
                html.Div(
                    [
                        html.Div(
                            social_media_aggs_df["twitter_tot_comments"][0],
                            style={"fontSize": 24},
                        ),
                        html.Div("Total Twitter Tweets Scraped"),
                        html.Div(
                            f"{social_media_aggs_df['twitter_pct_difference'][0]}% difference from average"
                        ),
                    ],
                    className="kpi-box",
                ),
            ],
            className="kpi-container",
            style={"display": "flex", "justify-content": "space-between"},
        ),
        html.Div(
            [
                dash_table.DataTable(
                    id="social-media-table",
                    columns=reddit_comments_columns,
                    data=reddit_comments_df.to_dict("records"),
                    css=[{"selector": ".show-hide", "rule": "display: none"}],
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="social-media-team-selector",
                        options=[
                            {"label": team, "value": team}
                            for team in team_names_abbreviations
                        ],
                        value="GSW",
                        clearable=False,
                        style={"width": "250px"},
                    ),
                ),
                dcc.Graph(
                    id="social-media-plot",
                    config={"displayModeBar": False},
                    style={"width": "100%", "display": "inline-block"},
                ),
            ]
        ),
    ],
    className="custom-padding",
)


@callback(
    Output("social-media-plot", "figure"), Input("social-media-team-selector", "value")
)
def update_reddit_team_sentiment(selected_team):
    filtered_team_sentiment = reddit_sentiment_time_series_df.query(
        f"team == '{selected_team}'"
    )

    fig = px.bar(
        filtered_team_sentiment,
        x="scrape_date",
        y="num_comments",
        color="game_outcome",
        color_discrete_map={
            "W": "green",
            "L": "red",
            "NO GAME": "grey",
        },
        labels={
            "scrape_date": "Scrape Date",
            "num_comments": "Number of Comments",
        },
    )

    fig.update_traces(texttemplate="%{text}", textposition="outside")

    return fig
