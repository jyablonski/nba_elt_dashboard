def test_load_yaml_with_env(config_fixture):
    assert config_fixture == {
        "database": "postgres",
        "host": "postgres",
        "pass": "postgres",
        "schema": "marts",
        "user": "nba_dashboard_user",
    }
