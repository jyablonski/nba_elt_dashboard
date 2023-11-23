def test_load_yaml_with_env(config_fixture):
    assert config_fixture == {
        "database": "postgres",
        "host": "postgres",
        "pass": "postgres",
        "schema": "nba_prod",
        "user": "nba_dashboard_user",
    }
