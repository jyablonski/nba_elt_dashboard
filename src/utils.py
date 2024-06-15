from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


def pbp_transformer(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    *** WARNING ***
    *** DANGER ***

    I ported this 3 yr old R Code via ChatGPT; do not ever fuck with this code.
    if it breaks then rip, just delete the graph and rebuild the dataset
    in dbt which is where this logic should exist.

    Args:
        df (pd.DataFrame): The Pandas DataFrame of pbp Data from dbt

    Returns:
        Pandas DataFrame of pbp Data used for the PBP Chart in Recent Games Tab
    """
    print("Running PBP Transformer")

    def replace_na(series, value):
        return series.fillna(value)

    pbp_events = df.copy().query("scoring_team != 'TIE'")
    pbp_events["prev_time"] = pbp_events["time_remaining_final"].shift()
    pbp_events["prev_time"] = replace_na(pbp_events["prev_time"], 48.0)
    pbp_events["time_difference"] = round(
        60 * (pbp_events["prev_time"] - pbp_events["time_remaining_final"])
    )
    pbp_events["time_difference"] = replace_na(pbp_events["time_difference"], 0)
    last_record_team = pbp_events.tail(1)

    pbp_events = pbp_events._append(
        {
            "scoring_team": last_record_team["scoring_team"].values[0],
            "quarter": last_record_team["quarter"].values[0],
            "time_quarter": "0:00",
            "leading_team_text": last_record_team["leading_team_text"].values[0],
            "time_remaining_final": last_record_team["time_remaining_final"].values[0],
            "prev_time": last_record_team["time_remaining_final"].values[0],
            "time_difference": round(
                60 * (last_record_team["prev_time"].values[0] - 0)
            ),
        },
        ignore_index=True,
    )

    pbp_events["game_plot_team_text"] = pbp_events.apply(
        lambda row: (
            row["home_fill"]
            if row["scoring_team"] == row["home_team"]
            else row["away_fill"]
        ),
        axis=1,
    )

    pbp_kpis = (
        pbp_events.groupby(["scoring_team", "leading_team_text"])["time_difference"]
        .sum()
        .reset_index()
    )
    pbp_kpis = pbp_kpis.pivot_table(
        index="scoring_team",
        columns="leading_team_text",
        values="time_difference",
        fill_value=0,
    ).reset_index()

    # Update "Leading" values by adding "Trailing" to the opponent's "Leading"
    for index, row in pbp_kpis.iterrows():
        opponent_team = "DEN" if row["scoring_team"] == "MIA" else "MIA"
        pbp_kpis.loc[pbp_kpis["scoring_team"] == opponent_team, "Leading"] += row[
            "Trailing"
        ]

    # Check if 'TIE' column exists, if not, add it and initialize to 0
    if "TIE" not in pbp_kpis.columns:
        pbp_kpis["TIE"] = 0

    tot = sum(pbp_kpis["Leading"] + pbp_kpis["TIE"])
    pbp_kpis["pct_leading"] = round(pbp_kpis["Leading"] / tot, 3)
    pbp_kpis.drop(columns=["Trailing"], inplace=True)

    return pbp_kpis, pbp_events


def generate_team_ratings_figure(df: pd.DataFrame) -> go.Figure:
    ortg_avg = df["ortg"].mean()
    drtg_avg = df["drtg"].mean()

    team_ratings_fig = px.scatter(
        df,
        x="ortg",
        y="drtg",
        labels={
            "ortg": "Offensive Rating",
            "drtg": "Defensive Rating",
        },
        custom_data=[
            "team",
            "ortg",
            "drtg",
            "nrtg",
            "ortg_rank",
            "drtg_rank",
            "nrtg_rank",
        ],
    )

    team_ratings_fig.add_hline(
        y=ortg_avg, line_width=3, line_dash="dash", line_color="black", opacity=0.5
    )
    team_ratings_fig.add_vline(
        x=drtg_avg, line_width=3, line_dash="dash", line_color="black", opacity=0.5
    )

    team_logos = []
    for i, row in df.iterrows():
        team_logos.append(
            go.layout.Image(
                source=f"../assets/{row['team_logo']}",
                x=row["ortg"],
                y=row["drtg"],
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                sizex=2.5,
                sizey=2.5,
            )
        )

    layout = go.Layout(images=team_logos)
    team_ratings_fig.update_layout(layout)

    team_ratings_fig.update_yaxes(
        autorange="reversed",
    )
    team_ratings_fig.update_traces(
        mode="markers",
        marker=dict(
            size=25,
            opacity=0,
        ),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        hovertemplate="<b>%{customdata[0]}</b><br>"
        "<b>Offensive Rating:</b> %{customdata[1]} (%{customdata[4]})<br>"
        "<b>Defensive Rating:</b> %{customdata[2]} (%{customdata[5]})<br>"
        "<b>Net Rating:</b> %{customdata[3]} (%{customdata[6]})<br>",
    )

    return team_ratings_fig


def create_season_selector_dropdown(
    current_date: datetime.date = datetime.now().date(),
) -> dbc.Row:
    """
    Function to conditionally create the Regular Season / Playoffs
    Dropdown Selector for the Scoring Efficiency Plot.

    It will only show Regular Season until the Playoffs, and will
    default to showing Playoffs first once the Postseason begins.

    Args:
        current_date (date): Current Date to check various conditions for

    Returns:
        dbc.Row Object for the Dropdown Selector.
    """
    playoff_start = datetime(current_date.year, 4, 15).date()
    season_start = datetime(current_date.year, 10, 1).date()

    if playoff_start < current_date < season_start:
        default_season = "Playoffs"
        options = [
            {"label": "Regular Season", "value": "Regular Season"},
            {"label": "Playoffs", "value": "Playoffs"},
        ]
    else:
        default_season = "Regular Season"
        options = [{"label": "Regular Season", "value": "Regular Season"}]

    dropdown = dbc.Row(
        [
            html.H4("Select a Season Type"),
            dbc.Col(
                dcc.Dropdown(
                    id="season-selector",
                    options=options,
                    clearable=False,
                    value=default_season,
                ),
                width={"size": 2},
            ),
        ]
    )

    return dropdown
