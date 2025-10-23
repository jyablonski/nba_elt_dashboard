from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from src.config import create_kpi_card
from src.data_cols.reddit_recent_keywords import reddit_keyword_columns
from src.data_cols.reddit_comments import reddit_comments_columns
from src.database import (
    reddit_comments_df,
    reddit_sentiment_time_series_df,
    reddit_recent_keywords_df,
    social_media_aggs_df,
)
from src.data import team_names_abbreviations
from src.config import DARK_LAYOUT_TEMPLATE

# Constants
GAME_OUTCOME_COLORS = {
    "W": "#3fb7d9",
    "L": "#e04848",
    "NO GAME": "#383b3d",
}

SOCIAL_MEDIA_OPTIONS = [
    {"label": "Reddit", "value": "reddit"},
    {"label": "Twitter (Out of Commission 😢)", "value": "twitter"},
]

TEAM_OPTIONS = [{"label": team, "value": team} for team in team_names_abbreviations]

COMMON_HOVER_STYLE = dict(
    bgcolor="#222222",
    font_size=12,
    font_family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    font_color="rgb(230, 224, 224)",
)

# Data preprocessing
reddit_comments_df["url"] = reddit_comments_df["url"].str.replace(
    "^(.*)$", "[Link](\\1)", regex=True
)


def create_metric_kpi(value, label, difference=None):
    """Create a metric KPI card with value, label, and optional difference"""
    content = [
        html.Div(value, style={"fontSize": 24, "fontWeight": "bold"}),
        html.Div(label, style={"fontSize": 14}),
    ]

    if difference is not None:
        content.append(
            html.Div(
                f"{difference}% difference from average", style={"fontSize": 12, "color": "gray"}
            )
        )

    return create_kpi_card(content)


def create_keywords_table():
    """Create the reddit keywords data table"""
    return dash_table.DataTable(
        id="keywords-table",
        columns=reddit_keyword_columns,
        data=reddit_recent_keywords_df.to_dict("records"),
        css=[{"selector": ".show-hide", "rule": "display: none"}],
        cell_selectable=False,
        filter_action="native",
        sort_action="native",
        page_size=20,
        # Base styling
        style_cell={
            "overflow": "hidden",
            "textOverflow": "ellipsis",
            "maxWidth": 0,
            "background-color": "#383b3d",
            "textAlign": "center",
            "fontSize": 15,
        },
        hidden_columns=[
            "top_nba_team_flair",
            "most_common_sentiment",
            "avg_sentiment_when_used",
            "analysis_date",
        ],
        # Column-specific styling
        style_cell_conditional=[
            {
                "if": {"column_id": "word"},
                "width": "25%",
                "textAlign": "left",
                "fontWeight": "bold",
            },
            {"if": {"column_id": "word_frequency"}, "width": "25%"},
            {"if": {"column_id": "frequency_rank"}, "width": "25%"},
            {"if": {"column_id": "nba_teams_flairs_using_word"}, "width": "25%"},
        ],
        # Conditional formatting for sentiment
        style_data_conditional=[
            {
                "if": {
                    "filter_query": "{avg_sentiment_When_used} > 0.1",
                    "column_id": "avg_sentiment_When_used",
                },
                "backgroundColor": "#4CAF50",
                "color": "white",
            },
            {
                "if": {
                    "filter_query": "{avg_sentiment_When_used} < -0.1",
                    "column_id": "avg_sentiment_When_used",
                },
                "backgroundColor": "#F44336",
                "color": "white",
            },
        ],
    )


def create_data_table():
    """Create the social media data table with consistent styling"""
    return dash_table.DataTable(
        id="social-media-table",
        columns=reddit_comments_columns,
        data=reddit_comments_df.to_dict("records"),
        # Styling
        css=[
            {
                "selector": ".dash-table-tooltip",
                "rule": "background-color: grey; font-family: 'Gill Sans','Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; color: white",
            }
        ],
        # Table behavior
        cell_selectable=False,
        filter_action="native",
        sort_action="native",
        page_size=15,
        merge_duplicate_headers=True,
        # Base styling
        style_cell={
            "overflow": "hidden",
            "textOverflow": "ellipsis",
            "maxWidth": 0,
            "background-color": "#383b3d",
            "textAlign": "center",
            "fontSize": 12,
        },
        # Column-specific styling
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
            {"if": {"column_id": "comment"}, "textAlign": "left", "width": "40%"},
        ],
        # Tooltips
        tooltip_data=[
            {column: {"value": str(value), "type": "markdown"} for column, value in row.items()}
            for row in reddit_comments_df.to_dict("records")
        ],
        tooltip_duration=None,
    )


# Layout
social_media_analysis_layout = html.Div(
    [
        # KPI Section
        html.Div(
            [
                # Reddit Logo
                create_kpi_card(
                    [
                        html.Img(
                            src="../assets/reddit.png", style={"height": "75px", "width": "75px"}
                        )
                    ]
                ),
                # Social Media Selector
                create_kpi_card(
                    [
                        html.H4("Select Social Media Type", style={"margin-bottom": "10px"}),
                        dcc.Dropdown(
                            id="social-media-selector",
                            options=SOCIAL_MEDIA_OPTIONS,
                            value="reddit",
                            clearable=False,
                            className="dash-dropdown",
                        ),
                    ]
                ),
                # Reddit Metrics
                create_metric_kpi(
                    value=social_media_aggs_df["reddit_tot_comments"][0],
                    label="Total Reddit Comments Scraped",
                    difference=social_media_aggs_df["reddit_pct_difference"][0],
                ),
                # Twitter Metrics
                create_metric_kpi(
                    value=social_media_aggs_df["twitter_tot_comments"][0],
                    label="Total Twitter Tweets Scraped",
                    difference=social_media_aggs_df["twitter_pct_difference"][0],
                ),
            ],
            className="kpi-container",
            style={"display": "flex", "justify-content": "space-between", "margin-bottom": "20px"},
        ),
        # Data Tables Section
        dbc.Row(
            [
                # Comments Table
                dbc.Col(
                    [
                        html.H3("Recent Comments", style={"margin-bottom": "15px"}),
                        create_data_table(),
                    ],
                    width=8,
                ),
                # Keywords Table
                dbc.Col(
                    [
                        html.H3("Trending Keywords", style={"margin-bottom": "15px"}),
                        create_keywords_table(),
                    ],
                    width=4,
                ),
            ]
        ),
        html.Br(),
        # Sentiment Analysis Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Comments by Team Flair", style={"margin-bottom": "15px"}),
                        # Team Selector
                        html.Div(
                            [
                                html.Label(
                                    "Select Team:",
                                    style={"margin-right": "10px", "fontWeight": "bold"},
                                ),
                                dcc.Dropdown(
                                    id="social-media-team-selector",
                                    options=TEAM_OPTIONS,
                                    value="GSW",
                                    clearable=False,
                                    style={"width": "250px", "display": "inline-block"},
                                ),
                            ],
                            style={"margin-bottom": "20px"},
                        ),
                        # Chart
                        dcc.Graph(
                            id="social-media-plot", style={"width": "100%", "height": "500px"}
                        ),
                    ],
                    width=12,
                )
            ]
        ),
    ],
    className="custom-padding",
)


@callback(Output("social-media-plot", "figure"), Input("social-media-team-selector", "value"))
def update_reddit_team_sentiment(selected_team):
    """Update sentiment plot based on selected team"""
    if not selected_team:
        return {}

    # Filter data
    filtered_data = reddit_sentiment_time_series_df.query(f"team == '{selected_team}'")

    if filtered_data.empty:
        return {}

    # Create plot
    fig = px.bar(
        filtered_data,
        x="scrape_date",
        y="num_comments",
        color="game_outcome",
        color_discrete_map=GAME_OUTCOME_COLORS,
        labels={
            "scrape_date": "Date",
            "num_comments": "Number of Comments",
            "game_outcome": "Previous Day's Game Outcome",
        },
        title=f"{selected_team} - Comments by Game Outcome Over Time",
    )

    # Update layout with dark theme
    fig.update_layout(
        **DARK_LAYOUT_TEMPLATE,
        legend_title_text="Game Outcome",
        showlegend=True,
        title={"x": 0.5, "xanchor": "center"},
    )

    # Update hover template
    fig.update_traces(
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>Date:</b> %{x}<br>"
            "<b>Comments:</b> %{y}<br>"
            "<b>Game Outcome:</b> %{fullData.name}<br>"
            "<extra></extra>"
        ),
    )

    return fig
