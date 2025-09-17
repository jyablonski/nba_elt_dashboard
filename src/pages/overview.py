from dash import callback, dash_table, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from src.config import create_kpi_card
from src.data_cols.standings import standings_columns
from src.database import (
    bans_df,
    contract_value_analysis_df,
    injuries_df,
    player_stats_df,
    standings_df,
    team_contracts_analysis_df,
    team_ratings_df,
)
from src.utils import create_season_selector_dropdown, generate_team_ratings_figure

MVP_CANDIDATE_COLORS = {
    "Top 5 MVP Candidate": "#9362DA",
    "Other": "#383b3d",
}

VALUE_ANALYSIS_COLORS = {
    "Superstars": "#9362DA",
    "Great Value": "#3fb7d9",
    "Normal": "#383b3d",
    "Bad Value": "#e04848",
}

COMMON_HOVER_STYLE = dict(
    bgcolor="rgba(255, 255, 255, 0.95)",
    font_size=12,
    font_family="'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
    font_color="#000000",
)

# Data preprocessing
team_contracts_analysis_df = team_contracts_analysis_df.sort_values(
    by="team_pct_salary_earned", ascending=True
)


def create_standings_table(conference_name, data):
    """Create a standardized standings table"""
    return dash_table.DataTable(
        id=f"{conference_name.lower()}-standings-table",
        columns=standings_columns,
        data=data,
        # Styling
        style_cell={
            "background-color": "#383b3d",
            "textAlign": "center",
            "fontSize": 12,
            "color": "rgb(230, 224, 224)",
            "padding": "8px",
        },
        # Hidden columns
        hidden_columns=["active_protocols", "conference", "team"],
        # Table behavior
        cell_selectable=False,
        css=[{"selector": ".show-hide", "rule": "display: none"}],
        sort_action="native",
        page_size=15,
    )


def create_player_value_analysis_chart():
    """Create the player value analysis scatter plot"""
    fig = px.scatter(
        contract_value_analysis_df,
        x="salary",
        y="avg_mvp_score",
        labels={
            "salary": "Annual Salary",
            "avg_mvp_score": "Average MVP Score",
        },
        title="Player Contract Value vs Performance",
        custom_data=[
            "player",
            "team",
            "avg_mvp_score",
            "salary",
            "color_var",
            "games_played",
            "games_missed",
        ],
        color="color_var",
        color_discrete_map=VALUE_ANALYSIS_COLORS,
    )

    # Apply dark theme with transparent plot background
    fig.update_layout(
        paper_bgcolor="#15171a",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "color": "rgb(230, 224, 224)",
            "family": "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
        },
        xaxis={
            "gridcolor": "#383b3d",
            "linecolor": "#383b3d",
            "tickcolor": "#383b3d",
            "zerolinecolor": "#383b3d",
            "tickformat": "$,.0f",
        },
        yaxis={
            "gridcolor": "#383b3d",
            "linecolor": "#383b3d",
            "tickcolor": "#383b3d",
            "zerolinecolor": "#383b3d",
        },
        margin={"l": 80, "r": 40, "t": 80, "b": 60},
        legend_title_text="Player Category",
        title={"x": 0.5, "xanchor": "center"},
    )

    fig.update_traces(
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Team:</b> %{customdata[1]}<br>"
            "<b>Category:</b> %{customdata[4]}<br>"
            "<b>MVP Score:</b> %{customdata[2]:.2f}<br>"
            "<b>Salary:</b> $%{customdata[3]:,}<br>"
            "<b>Games Played:</b> %{customdata[5]}<br>"
            "<b>Games Missed:</b> %{customdata[6]}<br>"
            "<extra></extra>"
        ),
    )

    return fig


def create_team_contract_analysis_chart():
    """Create the team contract value analysis bar chart"""
    fig = px.bar(
        team_contracts_analysis_df,
        x="team_pct_salary_earned",
        y="team",
        color="win_percentage",
        color_continuous_scale=[[0, "#e04848"], [0.5, "#383b3d"], [1, "#3fb7d9"]],
        labels={
            "team_pct_salary_earned": "% Salary Value Earned",
            "team": "Team",
            "win_percentage": "Win %",
        },
        title="Team Contract Efficiency vs Win Percentage",
        custom_data=[
            "team",
            "win_percentage",
            "sum_salary_earned",
            "sum_salary_earned_max",
            "team_pct_salary_earned",
            "value_lost_from_injury",
            "team_pct_salary_lost",
        ],
    )

    # Apply dark theme with transparent plot background
    fig.update_layout(
        paper_bgcolor="#15171a",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "color": "rgb(230, 224, 224)",
            "family": "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
        },
        xaxis={
            "gridcolor": "#383b3d",
            "linecolor": "#383b3d",
            "tickcolor": "#383b3d",
            "zerolinecolor": "#383b3d",
            "tickformat": ".0%",
        },
        yaxis={
            "gridcolor": "#383b3d",
            "linecolor": "#383b3d",
            "tickcolor": "#383b3d",
            "zerolinecolor": "#383b3d",
        },
        margin={"l": 80, "r": 40, "t": 80, "b": 60},
        title={"x": 0.5, "xanchor": "center"},
    )

    fig.update_traces(
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Win Percentage:</b> %{customdata[1]:.1%}<br>"
            "<b>Salary Value Earned:</b> %{customdata[4]:.1%}<br>"
            "<b>Salary Lost to Injury:</b> %{customdata[6]:.1%}<br>"
            "<b>Total Value Earned:</b> $%{customdata[2]:,}<br>"
            "<b>Total Value Lost:</b> $%{customdata[5]:,}<br>"
            "<extra></extra>"
        ),
    )

    return fig


# Layout
overview_layout = html.Div(
    [
        # KPI Section
        html.Div(
            [
                # Home/Road Record KPI
                create_kpi_card(
                    [
                        html.Div(
                            f"{bans_df['tot_wins'][0]} - {bans_df['tot_wins'][1]}",
                            style={"fontSize": 24, "fontWeight": "bold", "margin-bottom": "5px"},
                        ),
                        html.Div(
                            "League Wide Home - Road Win Record", style={"margin-bottom": "5px"}
                        ),
                        html.Div(
                            f"{bans_df['win_pct'][0] * 100:.0f}% - {bans_df['win_pct'][1] * 100:.0f}% Win Percentage Splits",
                            style={"fontSize": 12, "color": "gray"},
                        ),
                    ]
                ),
                # Points Per Game KPI
                create_kpi_card(
                    [
                        html.Div(
                            f"{bans_df['avg_pts'][0]:.1f}",
                            style={"fontSize": 24, "fontWeight": "bold", "margin-bottom": "5px"},
                        ),
                        html.Div("League Average Points Per Game", style={"margin-bottom": "5px"}),
                        html.Div(
                            f"{((bans_df['avg_pts'][0] - bans_df['last_yr_ppg'][0]) / bans_df['avg_pts'][0]) * 100:.2f}% difference vs Last Season",
                            style={"fontSize": 12, "color": "gray"},
                        ),
                    ]
                ),
                # Injury Report KPI
                create_kpi_card(
                    [
                        html.Div(
                            str(len(injuries_df)),
                            style={"fontSize": 24, "fontWeight": "bold", "margin-bottom": "5px"},
                        ),
                        html.Div(
                            "Players Currently on Injury Report", style={"margin-bottom": "5px"}
                        ),
                        html.Div(
                            "Includes all injury designations",
                            style={"fontSize": 12, "color": "gray"},
                        ),
                    ]
                ),
                # Upcoming Games KPI
                create_kpi_card(
                    [
                        html.Div(
                            bans_df["upcoming_game_date"][0].strftime("%B %d"),
                            style={"fontSize": 24, "fontWeight": "bold", "margin-bottom": "5px"},
                        ),
                        html.Div(
                            f"{bans_df['upcoming_games'][0]} Upcoming Games",
                            style={"margin-bottom": "5px"},
                        ),
                        html.Div(
                            bans_df["upcoming_game_date"][0].strftime("%A"),
                            style={"fontSize": 12, "color": "gray"},
                        ),
                    ]
                ),
            ],
            className="kpi-container",
            style={"display": "flex", "justify-content": "space-between", "margin-bottom": "20px"},
        ),
        # Data Update Info
        html.Div(
            [
                html.P(
                    f"Data Last Updated: {(bans_df['scrape_time'][0]).strftime('%A, %B %d at %-I:%M %p UTC')}",
                    style={"text-align": "center", "color": "gray", "margin-bottom": "20px"},
                )
            ]
        ),
        # Standings Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Western Conference", style={"margin-bottom": "15px"}),
                        create_standings_table(
                            "Western",
                            standings_df.query('conference == "Western"').to_dict("records"),
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H3("Eastern Conference", style={"margin-bottom": "15px"}),
                        create_standings_table(
                            "Eastern",
                            standings_df.query('conference == "Eastern"').to_dict("records"),
                        ),
                    ],
                    width=6,
                ),
            ],
            style={"margin-bottom": "30px"},
        ),
        # Season Selector
        create_season_selector_dropdown(),
        # Charts Section 1
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Player Scoring Efficiency", style={"margin-bottom": "15px"}),
                        dcc.Graph(id="player-scoring-efficiency-plot", style={"height": "500px"}),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H3("Team Ratings", style={"margin-bottom": "15px"}),
                        dcc.Graph(
                            id="team-ratings-plot",
                            figure=generate_team_ratings_figure(df=team_ratings_df),
                            style={"height": "500px"},
                        ),
                    ],
                    width=6,
                ),
            ],
            style={"margin-bottom": "30px"},
        ),
        # Charts Section 2
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Player Value Analysis", style={"margin-bottom": "15px"}),
                        dcc.Graph(
                            id="player-value-analysis-plot",
                            figure=create_player_value_analysis_chart(),
                            style={"height": "500px"},
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H3("Team Contract Efficiency", style={"margin-bottom": "15px"}),
                        dcc.Graph(
                            id="contract-bar-plot",
                            figure=create_team_contract_analysis_chart(),
                            style={"height": "500px"},
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
    ],
    className="custom-padding",
)


@callback(
    Output("player-scoring-efficiency-plot", "figure"),
    Input("season-selector", "value"),
)
def update_scoring_efficiency_plot(selected_season):
    """Update player scoring efficiency plot based on season selection"""
    if not selected_season:
        selected_season = "Regular Season"

    # Calculate league average
    regular_season_ts_percent_avg = player_stats_df.query("season_type == 'Regular Season'")[
        "avg_ts_percent"
    ].mean()

    # Filter data
    filtered_df = player_stats_df.copy().query(
        f"season_type == '{selected_season}' & avg_ppg >= 20"
    )

    if filtered_df.empty:
        return {}

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x="avg_ppg",
        y="avg_ts_percent",
        labels={
            "avg_ppg": "Average Points Per Game",
            "avg_ts_percent": "True Shooting %",
        },
        title=f"Player Scoring Efficiency - {selected_season}",
        color="is_mvp_candidate",
        color_discrete_map=MVP_CANDIDATE_COLORS,
        custom_data=[
            "player",
            "team",
            "avg_ppg",
            "avg_ts_percent",
            "games_played",
            "is_mvp_candidate",
        ],
    )

    # Apply dark theme with transparent plot background
    fig.update_layout(
        paper_bgcolor="#15171a",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "color": "rgb(230, 224, 224)",
            "family": "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif",
        },
        xaxis={
            "gridcolor": "#383b3d",
            "linecolor": "#383b3d",
            "tickcolor": "#383b3d",
            "zerolinecolor": "#383b3d",
        },
        yaxis={
            "gridcolor": "#383b3d",
            "linecolor": "#383b3d",
            "tickcolor": "#383b3d",
            "zerolinecolor": "#383b3d",
            "tickformat": ".0%",
        },
        margin={"l": 80, "r": 40, "t": 80, "b": 60},
        legend_title_text="Player Type",
        title={"x": 0.5, "xanchor": "center"},
    )

    # Add league average line
    fig.add_hline(
        y=regular_season_ts_percent_avg,
        line_width=2,
        line_dash="dash",
        line_color="rgb(230, 224, 224)",
        opacity=0.7,
    )

    # Add player logos
    player_logos = []
    for i, row in filtered_df.iterrows():
        player_logos.append(
            go.layout.Image(
                source=row["player_logo"],
                x=row["avg_ppg"],
                y=row["avg_ts_percent"],
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                sizex=1.5,
                sizey=1.5,
            )
        )

    fig.update_layout(images=player_logos)

    # Update traces
    fig.update_traces(
        marker=dict(size=16, line=dict(width=1, color="rgb(230, 224, 224)")),
        mode="markers",
        hoverlabel=COMMON_HOVER_STYLE,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Team:</b> %{customdata[1]}<br>"
            "<b>Type:</b> %{customdata[5]}<br>"
            "<b>PPG:</b> %{customdata[2]:.1f}<br>"
            "<b>True Shooting:</b> %{customdata[3]:.1%}<br>"
            "<b>Games Played:</b> %{customdata[4]}<br>"
            "<extra></extra>"
        ),
    )

    # Add annotation for league average
    fig.add_annotation(
        x=filtered_df["avg_ppg"].max() * 0.95,
        y=regular_season_ts_percent_avg + 0.01,
        text="League Average TS%",
        yanchor="bottom",
        showarrow=False,
        font=dict(color="rgb(230, 224, 224)"),
    )

    return fig
