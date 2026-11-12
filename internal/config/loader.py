"""Configuration loader."""
from __future__ import annotations

import json


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def tenant_schemas(config: dict) -> dict:
    return config.get("tenant_schemas", {})
