"""Run the end-to-end IPL training pipeline."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.load_data import load_match_data
from src.feature_selection.filter_features import build_feature_registry, filter_features
from src.features.build_features import build_training_features
from src.models.train import train_model
from src.utils.helpers import load_yaml_config


def run_pipeline() -> dict:
    """Execute the high-level training flow with placeholder components."""

    config = load_yaml_config(PROJECT_ROOT / "configs" / "config.yaml")
    raw_datasets = load_match_data(config)
    candidate_features = build_feature_registry().all()
    selected_features = filter_features(
        candidate_features,
        config.get("data", {}).get("available_sources", []),
    )
    training_bundle = build_training_features(raw_datasets, selected_features, config)
    trained_model = train_model(training_bundle, config)

    return {
        "config": config,
        "raw_datasets": raw_datasets,
        "selected_features": selected_features,
        "training_bundle": training_bundle,
        "trained_model": trained_model,
    }


if __name__ == "__main__":
    result = run_pipeline()
    print("Pipeline executed successfully.")
    print(f"Selected features: {len(result['selected_features'])}")
    print(f"Model status: {result['trained_model']['status']}")
