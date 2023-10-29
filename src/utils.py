from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def pbp_transformer(df: pd.DataFrame):
    """
    *** WARNING ***
    *** DANGER ***

    I ported this 3 yr old R Code via ChatGPT; do not ever fuck with this code.
    if it breaks then rip, just delete the graph and rebuild the dataset
    needed in dbt

    Args:
        df (pd.DataFrame): The Pandas DataFrame of pbp Data from dbt

    Returns:
        Pandas DataFrame of pbp Data for the Line Chart in Recent Games Tab
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
        lambda row: row["home_fill"]
        if row["scoring_team"] == row["home_team"]
        else row["away_fill"],
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

    tot = sum(pbp_kpis["Leading"] + pbp_kpis["TIE"])
    pbp_kpis["pct_leading"] = round(pbp_kpis["Leading"] / tot, 3)
    pbp_kpis.drop(columns=["Trailing"], inplace=True)

    return pbp_kpis, pbp_events


def generate_card(name: str, description: str, kpi_value: str, color: str):
    """
    Function to generate cards for KPIs

    Args:
        name (str):

        description (str):

        kpi_value: The KPI Value or BAN to put in the Card

        color: Color of the top bar

    Returns
        HTML Card
    """

    return dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(name, className="card-title"),
                        html.P(description, className="card-desc"),
                        html.P(f"{kpi_value:,}", className="card-text"),
                        html.P("Key Metric", className="card-kpi"),
                    ],
                    className="text-center mx-auto",
                )
            ],
            style={
                "background": f"linear-gradient(to bottom, {color} 100%, #FFFFFF 0%)"
            },
        ),
        className="col-auto mb-3",
    )


def generate_team_ratings_figure(df):
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
            "drtg_rank",
            "ortg_rank",
            "nrtg_rank",
        ],
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
                sizex=2.0,
                sizey=2.0,
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
            size=18,
            opacity=0,
        ),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        hovertemplate="<b>%{customdata[0]}</b><br>"
        "<b>Offensive Rating:</b> %{customdata[1]} (%{customdata[4]})<br>"
        "<b>Defensive Rating:</b> %{customdata[2]} (%{customdata[5]})<br>"
        "<b>Net Rating:</b> %{customdata[3]} (%{customdata[6]})<br>",
    )

    return team_ratings_fig
