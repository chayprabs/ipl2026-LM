"""Data-loading utilities for the IPL prediction pipeline."""

from __future__ import annotations

from pathlib import Path


def load_match_data(config: dict) -> dict:
    """Load raw datasets required by the training pipeline.

    This placeholder only returns the configured paths and source names.
    Replace it later with actual readers for CSV, parquet, APIs, or databases.
    """

    data_config = config.get("data", {})
    raw_dir = Path(data_config.get("raw_dir", "data/raw"))

    return {
        "raw_data_dir": raw_dir,
        "available_sources": data_config.get("available_sources", []),
        "matches": None,
        "players": None,
        "venues": None,
    }
