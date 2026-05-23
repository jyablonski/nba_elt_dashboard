from __future__ import annotations

from datetime import date, datetime

from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.theme.plotly import TRACE_HOVERLABEL, apply_dark_layout
from src.ui.sections import section_header


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

    # Handle empty dataframe
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    def replace_na(series, value):
        return series.fillna(value)

    pbp_events = df.copy().sort_values(
        ["game_description", "time_remaining_final"],
        ascending=[True, False],
    )
    pbp_events["prev_time"] = pbp_events.groupby("game_description")[
        "time_remaining_final"
    ].shift()
    pbp_events["prev_time"] = replace_na(pbp_events["prev_time"], 48.0)
    pbp_events["next_time"] = pbp_events.groupby("game_description")[
        "time_remaining_final"
    ].shift(-1)
    pbp_events["next_time"] = replace_na(pbp_events["next_time"], 0)
    pbp_events["time_difference"] = round(
        60 * (pbp_events["time_remaining_final"] - pbp_events["next_time"])
    )
    pbp_events["time_difference"] = replace_na(pbp_events["time_difference"], 0)
    plot_events = pbp_events.query("scoring_team != 'TIE'").copy()
    last_records = plot_events.groupby("game_description", as_index=False).tail(1)

    end_rows = []
    for _, row in last_records.iterrows():
        end_rows.append(
            {
                **row.to_dict(),
                "time_quarter": "0:00",
                "time_remaining_final": 0,
                "prev_time": row["time_remaining_final"],
                "next_time": 0,
                "time_difference": 0,
            }
        )
    if end_rows:
        plot_events = pd.concat([plot_events, pd.DataFrame(end_rows)], ignore_index=True)

    plot_events["game_plot_team_text"] = plot_events.apply(
        lambda row: (
            row["home_fill"] if row["scoring_team"] == row["home_team"] else row["away_fill"]
        ),
        axis=1,
    )

    pbp_kpis = (
        pbp_events.groupby(["game_description", "leading_team"])["time_difference"]
        .sum()
        .reset_index()
    )
    pbp_kpis = pbp_kpis.pivot_table(
        index="game_description",
        columns="leading_team",
        values="time_difference",
        fill_value=0,
    ).reset_index()

    if "TIE" not in pbp_kpis.columns:
        pbp_kpis["TIE"] = 0

    teams_by_game = (
        pbp_events.groupby("game_description")[["home_team", "away_team"]].first().reset_index()
    )
    pbp_kpis = pbp_kpis.merge(teams_by_game, on="game_description", how="left")

    leading_cols = [
        col for col in pbp_kpis.columns if col not in {"game_description", "home_team", "away_team"}
    ]
    total_time = pbp_kpis[leading_cols].sum(axis=1).replace(0, pd.NA)
    pbp_kpis["home_pct_leading"] = round(
        pbp_kpis.apply(lambda row: row.get(row["home_team"], 0), axis=1) / total_time,
        3,
    )
    pbp_kpis["away_pct_leading"] = round(
        pbp_kpis.apply(lambda row: row.get(row["away_team"], 0), axis=1) / total_time,
        3,
    )
    pbp_kpis["tie_pct"] = round(pbp_kpis["TIE"] / total_time, 3)

    plot_events.drop(columns=["next_time"], inplace=True)

    return pbp_kpis, plot_events


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
        title="Team Offensive vs Defensive Ratings",
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

    apply_dark_layout(team_ratings_fig, transparent_plot=True)
    team_ratings_fig.update_yaxes(autorange="reversed")
    team_ratings_fig.update_layout(title={"x": 0.5, "xanchor": "center"})

    team_ratings_fig.add_hline(
        y=drtg_avg, line_width=2, line_dash="dash", line_color="rgb(230, 224, 224)", opacity=0.7
    )
    team_ratings_fig.add_vline(
        x=ortg_avg, line_width=2, line_dash="dash", line_color="rgb(230, 224, 224)", opacity=0.7
    )

    team_logos = []
    for _i, row in df.iterrows():
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

    team_ratings_fig.update_layout(go.Layout(images=team_logos))

    team_ratings_fig.update_traces(
        mode="markers",
        marker=dict(size=25, opacity=0),
        hoverlabel=TRACE_HOVERLABEL,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<b>Offensive Rating:</b> %{customdata[1]} (Rank: %{customdata[4]})<br>"
            "<b>Defensive Rating:</b> %{customdata[2]} (Rank: %{customdata[5]})<br>"
            "<b>Net Rating:</b> %{customdata[3]} (Rank: %{customdata[6]})<br>"
            "<extra></extra>"
        ),
    )

    return team_ratings_fig


def scoring_efficiency_season_config(
    current_date: date | None = None,
) -> tuple[str, list[dict[str, str]]]:
    """Default value and dropdown options for the Overview scoring-efficiency filter.

    Playoffs appears only during a bounded postseason window (not all of Jul–Sep).
    """
    if current_date is None:
        current_date = datetime.now().date()
    year = current_date.year
    playoff_start = datetime(year, 4, 15).date()
    playoff_end = datetime(year, 6, 30).date()
    opt_rs: dict[str, str] = {"label": "Regular Season", "value": "Regular Season"}
    opt_po: dict[str, str] = {"label": "Playoffs", "value": "Playoffs"}
    if playoff_start <= current_date <= playoff_end:
        return "Playoffs", [opt_rs, opt_po]
    return "Regular Season", [opt_rs]


def create_season_selector_dropdown(
    current_date: date | None = None,
) -> dbc.Row:
    """
    Row with "Season type" header + dropdown (legacy layout helper; tests only).

    Overview embeds the dropdown next to the scoring-efficiency table instead.
    """
    default_season, options = scoring_efficiency_season_config(current_date)

    dropdown = dbc.Row(
        [
            dbc.Col(
                [
                    section_header("Season type"),
                    dcc.Dropdown(
                        id="scoring-efficiency-season",
                        options=options,
                        clearable=False,
                        value=default_season,
                        className="dash-dropdown",
                    ),
                ],
                width={"size": 12, "md": 4},
            ),
        ],
        className="mb-3",
    )

    return dropdown
