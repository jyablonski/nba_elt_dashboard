from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
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
                    className="kpi-card",
                ),
                # KPI 2
                html.Div(
                    [
                        html.H4("Select a Social Media Type"),
                        dcc.Dropdown(
                            id="social-media-selector",
                            options=[
                                {"label": "Reddit", "value": "reddit"},
                                {"label": "Twitter", "value": "twitter"},
                            ],
                            value="reddit",
                            clearable=False,
                            className="dash-dropdown",
                        ),
                    ],
                    className="kpi-card",
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
                            f"{social_media_aggs_df['reddit_pct_difference'][0]}% "
                            "difference from average"
                        ),
                    ],
                    className="kpi-card",
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
                            f"{social_media_aggs_df['twitter_pct_difference'][0]}% "
                            "difference from average"
                        ),
                    ],
                    className="kpi-card",
                ),
            ],
            className="kpi-container",
            style={"display": "flex", "justify-content": "space-between"},
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        id="social-media-table",
                        columns=reddit_comments_columns,
                        data=reddit_comments_df.to_dict("records"),
                        css=[
                            {
                                "selector": ".dash-table-tooltip",
                                "rule": "background-color: grey; font-family: \
                                font-family: 'Gill Sans','Gill Sans MT', Calibri, \
                                'Trebuchet MS', sans-serif; color: white",
                            }
                        ],
                        style_cell={
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "maxWidth": 0,
                            "background-color": "#383b3d",
                        },
                        tooltip_data=[
                            {
                                column: {"value": str(value), "type": "markdown"}
                                for column, value in row.items()
                            }
                            for row in reddit_comments_df.to_dict("records")
                        ],
                        tooltip_duration=None,
                        sort_action="native",
                        page_size=15,
                        merge_duplicate_headers=True,
                        style_cell_conditional=[
                            {"if": {"column_id": "scrape_date"}, "width": "8%"},
                            {"if": {"column_id": "author"}, "width": "8%"},
                            {"if": {"column_id": "flair"}, "width": "8%"},
                            {"if": {"column_id": "score"}, "width": "6%"},
                            {"if": {"column_id": "compound"}, "width": "5%"},
                            {"if": {"column_id": "pos"}, "width": "4%"},
                            {"if": {"column_id": "neg"}, "width": "4%"},
                            {"if": {"column_id": "neu"}, "width": "4%"},
                            {"if": {"column_id": "url"}, "width": "8%"},
                            {
                                "if": {"column_id": "comment"},
                                "textAlign": "left",
                                "width": "40%",
                            },
                        ],
                    ),
                    width=12,
                ),
            ],
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H4("Select a Team"),
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
                            ],
                            width=2,
                        )
                    ),
                ),
                dbc.Col(
                    [
                        html.H3("Reddit Sentiment Analysis Plot using Flairs"),
                        dcc.Graph(
                            id="social-media-plot",
                            style={"width": "100%", "display": "inline-block"},
                        ),
                    ],
                    width=12,
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
            "scrape_date": "",
            "num_comments": "Number of Comments",
        },
        custom_data=[
            "scrape_date",
            "num_comments",
            "game_outcome",
        ],
    )

    fig.update_layout(legend_title_text="")

    fig.update_traces(
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        hovertemplate="<b>Scrape Date: </b>%{customdata[0]}<br>"
        "<b>Total Comments:</b> %{customdata[1]}<br>"
        "<b>Previous Day's Game Outcome:</b> %{customdata[2]}<br>",
    )

    return fig
