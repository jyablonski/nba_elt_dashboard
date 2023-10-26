from dash import callback, dash_table, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

from src.data_cols.reddit_comments import reddit_comments_columns
from src.data import (
    reddit_comments_df,
    reddit_sentiment_time_series_df,
    social_media_aggs_df,
    team_names_abbreviations,
)
from src.utils import generate_card


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
                    style_cell={
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                        "maxWidth": 0,
                    },
                    sort_action="native",
                    page_size=15,
                    merge_duplicate_headers=True,
                    style_cell_conditional=[
                        {"if": {"column_id": "scrape_date"}, "width": "8%"},
                        {"if": {"column_id": "flair"}, "width": "8%"},
                        {"if": {"column_id": "comment"}, "width": "40%"},
                        {"if": {"column_id": "score"}, "width": "6%"},
                        {"if": {"column_id": "compound"}, "width": "5%"},
                        {"if": {"column_id": "pos"}, "width": "4%"},
                        {"if": {"column_id": "neg"}, "width": "4%"},
                        {"if": {"column_id": "neu"}, "width": "4%"},
                        {"if": {"column_id": "url"}, "width": "8%"},
                    ],
                ),
            ],
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
                    style={"width": "100%", "display": "inline-block"},
                ),
            ]
        ),
        html.Div(
            [
                html.H1("Card Component", className="text-center"),
                dbc.Row(
                    [
                        generate_card(
                            name="John Doe",
                            description="Business Owner",
                            kpi_value=2,
                            color="green",
                        ),
                        generate_card(
                            name="John Doe2",
                            description="Business Owner2",
                            kpi_value=3,
                            color="green",
                        ),
                        generate_card(
                            name="John Doe3",
                            description="Business Owner3",
                            kpi_value=1123 - 1414,
                            color="green",
                        ),
                    ],
                    className="cards justify-content-center",
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