from src.pages.overview import update_scoring_efficiency_table


def test_scoring_efficiency_table_regular_season():
    rows = update_scoring_efficiency_table("Regular Season")

    assert isinstance(rows, list)
    assert rows[0]["player"] == "Joel Embiid"
    assert rows[0]["avg_ppg"] == 35.3
    luka = next(r for r in rows if r["player"] == "Luka Doncic")
    assert luka["avg_ppg"] == 34.1
    assert "avg_ts_percent" in luka
    assert "ts_vs_reg_pp" in luka


def test_scoring_efficiency_table_playoffs():
    rows = update_scoring_efficiency_table("Playoffs")

    assert isinstance(rows, list)
    assert rows[0]["player"] == "Joel Embiid"
    assert rows[0]["avg_ppg"] == 27.3
