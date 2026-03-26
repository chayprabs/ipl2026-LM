"""Feature-building entrypoints for model training and inference."""

from __future__ import annotations


def _feature_name(feature: object) -> str:
    """Extract a feature name from either a mapping-like or object-like feature."""

    if hasattr(feature, "name"):
        return str(getattr(feature, "name"))
    if isinstance(feature, dict):
        return str(feature["name"])
    return str(feature)


def build_training_features(raw_datasets: dict, selected_features: list[object], config: dict) -> dict:
    """Transform filtered feature definitions into a model-ready placeholder bundle.

    The real implementation should map raw datasets to a training matrix and target.
    """

    return {
        "feature_names": [_feature_name(feature) for feature in selected_features],
        "feature_count": len(selected_features),
        "raw_datasets": raw_datasets,
        "X": None,
        "y": None,
        "config_snapshot": config.get("features", {}),
    }
