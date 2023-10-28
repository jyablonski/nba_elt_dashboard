from dash import html
import dash_bootstrap_components as dbc

import pandas as pd


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

    # Define a function for handling missing values
    def replace_na(series, value):
        return series.fillna(value)

    # Equivalent of R's dplyr functions in Python using pandas and numpy
    team_colors = df[["scoring_team", "leading_team_text"]].copy().drop_duplicates()
    try_df = df.copy().query("scoring_team != 'TIE'")
    try_df["prev_time"] = try_df["time_remaining_final"].shift()
    try_df["prev_time"] = replace_na(try_df["prev_time"], 48.0)
    try_df["time_difference"] = round(
        60 * (try_df["prev_time"] - try_df["time_remaining_final"])
    )
    try_df["time_difference"] = replace_na(try_df["time_difference"], 0)
    last_record_team = try_df.tail(1)

    # Create an empty DataFrame
    mydf = pd.DataFrame(
        columns=["scoring_team", "Trailing_time", "Leading_time", "Tied_time"]
    )

    # Group and summarize the try_df DataFrame
    try_df = try_df._append(
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

    summarized_df = (
        try_df.groupby(["scoring_team", "leading_team_text"])["time_difference"]
        .sum()
        .reset_index()
    )
    summarized_df = summarized_df.pivot_table(
        index="scoring_team",
        columns="leading_team_text",
        values="time_difference",
        fill_value=0,
    ).reset_index()

    # Create a copy of the original DataFrame
    result_df = summarized_df.copy()

    # Update "Leading" values by adding "Trailing" to the opponent's "Leading"
    for index, row in result_df.iterrows():
        opponent_team = "DEN" if row["scoring_team"] == "MIA" else "MIA"
        result_df.loc[result_df["scoring_team"] == opponent_team, "Leading"] += row[
            "Trailing"
        ]

    tot = sum(result_df["Leading"] + result_df["TIE"])
    result_df["pct_leading"] = round(result_df["Leading"] / tot, 3)

    # Drop the "Trailing" column
    result_df.drop(columns=["Trailing"], inplace=True)
    # # Simulating team_colors DataFrame (you can populate it with actual data)
    # team_colors = df.drop_duplicates(subset=["scoring_team", "scoring_team_color"])[["scoring_team", "scoring_team_color"]]

    # # Join the DataFrames
    # mydf = mydf.merge(team_colors, on="scoring_team", how="left")
    # mydf["text"] = (
    #     "<span style='color:"
    #     + mydf["scoring_team_color"]
    #     + ";'>"
    #     + mydf["scoring_team"]
    #     + "</span> led for "
    #     + (mydf["pct_leadtime"] * 100).astype(str)
    #     + " % of the Game"
    # )
    # mydf["tied_text"] = (
    #     "The teams were tied for "
    #     + (mydf["pct_tiedtime"] * 100).astype(str)
    #     + " % of the Game"
    # )

    # # Select the desired columns for the final DataFrame
    # final_df = mydf[["text", "tied_text"]]

    return result_df, try_df


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
