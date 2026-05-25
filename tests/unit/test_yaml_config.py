from src.data_access.database import load_yaml_with_env


def test_load_yaml_with_env_substitution(tmp_path, monkeypatch):
    monkeypatch.setenv("NBA_YAML_TESTUSER", "u-from-env")
    p = tmp_path / "cfg.yaml"
    p.write_text(
        "dev:\n  user: ${NBA_YAML_TESTUSER}\n  pass: x\n",
        encoding="utf-8",
    )
    data = load_yaml_with_env(str(p))
    assert data["dev"]["user"] == "u-from-env"
