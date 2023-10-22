import pandas as pd


def pbp_transformer(df: pd.DataFrame):
    """
    *** WARNING ***
    *** DANGER ***

    I Ported this 3 yr old R Code via ChatGPT; do not ever fuck with this code.
    if it breaks then rip, just delete the graph and rebuild the dataset
    needed in dbt

    Args:
        df (pd.DataFrame): The Pandas DataFrame of pbp Data from dbt

    Returns:
        Pandas DataFrame of pbp Data for the Line Chart in Recent Games Tab
    """
    # Define a function for handling missing values
    def replace_na(series, value):
        return series.fillna(value)

    # Equivalent of R's dplyr functions in Python using pandas and numpy
    team_colors = df[["scoring_team", "leading_team_text"]].drop_duplicates()
    try_df = df[df["scoring_team"] != "TIE"]
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
    )
    summarized_df["TIE_time"] = summarized_df.get("TIE_time", 0)

    # Create mydf DataFrame with the same structure as in R
    mydf["scoring_team"] = summarized_df.index
    mydf["Leading_time"] = summarized_df["TeamA"]
    mydf["Trailing_time"] = -summarized_df["TeamB"]
    mydf["Tied_time"] = summarized_df["TIE_time"]

    # Additional operations
    mydf["opp_leadtime"] = mydf["Trailing_time"][::-1]
    mydf["opp_tiedtime"] = mydf["Tied_time"][::-1]
    mydf["tot_leadtime"] = mydf["Leading_time"] + mydf["opp_leadtime"]
    mydf["tot_trailtime"] = mydf["tot_leadtime"][::-1]
    mydf["tot_tiedtime"] = mydf["Tied_time"] + mydf["opp_tiedtime"]
    mydf["tot_time"] = (
        mydf["tot_leadtime"] + mydf["tot_trailtime"] + mydf["tot_tiedtime"]
    )
    mydf["pct_leadtime"] = round(mydf["tot_leadtime"] / mydf["tot_time"], 3)
    mydf["pct_tiedtime"] = round(mydf["tot_tiedtime"] / mydf["tot_time"], 3)

    # Simulating team_colors DataFrame (you can populate it with actual data)
    team_colors = pd.DataFrame(
        {
            "scoring_team": ["TeamA", "TeamB"],
            "scoring_team_color": ["#FF0000", "#0000FF"],
        }
    )

    # Join the DataFrames
    mydf = mydf.merge(team_colors, on="scoring_team", how="left")
    mydf["text"] = (
        "<span style='color:"
        + mydf["scoring_team_color"]
        + ";'>"
        + mydf["scoring_team"]
        + "</span> led for "
        + (mydf["pct_leadtime"] * 100).astype(str)
        + " % of the Game"
    )
    mydf["tied_text"] = (
        "The teams were tied for "
        + (mydf["pct_tiedtime"] * 100).astype(str)
        + " % of the Game"
    )

    # Select the desired columns for the final DataFrame
    final_df = mydf[["text", "tied_text"]]

    return mydf, final_df