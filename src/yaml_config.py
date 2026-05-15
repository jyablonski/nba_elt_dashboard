from __future__ import annotations

import os
from typing import Any

import yaml


def substitute_env_vars(yaml_content: dict[str, Any]) -> None:
    for key, value in yaml_content.items():
        if isinstance(value, str):
            yaml_content[key] = os.path.expandvars(value)
        elif isinstance(value, dict):
            substitute_env_vars(value)


def load_yaml_with_env(filename: str) -> dict[str, Any]:
    with open(filename) as file:
        yaml_content = yaml.safe_load(file)
        substitute_env_vars(yaml_content)
        return yaml_content
