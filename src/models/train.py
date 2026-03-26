"""Training entrypoints for IPL prediction models."""

from __future__ import annotations


def train_model(feature_bundle: dict, config: dict) -> dict:
    """Train the model defined in configuration.

    This placeholder does not fit a real estimator yet. It only returns
    metadata showing what would be passed into training.
    """

    model_config = config.get("model", {})

    return {
        "model_type": model_config.get("name", "xgboost_placeholder"),
        "feature_count": feature_bundle.get("feature_count", 0),
        "artifact_path": model_config.get("artifact_path", "models/latest.pkl"),
        "status": "placeholder",
    }
