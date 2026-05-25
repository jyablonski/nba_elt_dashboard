from src.data_access.database import substitute_env_vars


def test_substitute_env_vars_nested(monkeypatch):
    monkeypatch.setenv("OUTER", "outerval")
    nested = {"inner": {"k": "prefix_${OUTER}_suffix"}}
    substitute_env_vars(nested)
    assert nested["inner"]["k"] == "prefix_outerval_suffix"
