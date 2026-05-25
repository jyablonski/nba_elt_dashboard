import os
from pathlib import Path

from src.data_access.database import load_yaml_with_env


def test_load_yaml_with_env():
    root = Path(__file__).resolve().parents[1]
    cfg = root / "fixtures" / "config_fixture.yaml"
    os.environ.setdefault("RDS_USER", "nba_dashboard_user")
    data = load_yaml_with_env(str(cfg))["docker_dev"]
    assert data == {
        "database": "postgres",
        "host": "postgres",
        "pass": "postgres",
        "schema": "gold",
        "user": "nba_dashboard_user",
    }
