"""Shared utility functions used across the project."""

from __future__ import annotations

from pathlib import Path

import yaml


def get_project_root() -> Path:
    """Return the repository root for the IPL prediction system package."""

    return Path(__file__).resolve().parents[2]


def load_yaml_config(config_path: str | Path) -> dict:
    """Load a YAML configuration file into a plain dictionary."""

    path = Path(config_path)
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}
