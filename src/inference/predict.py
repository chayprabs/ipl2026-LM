"""Inference helpers for serving match predictions."""

from __future__ import annotations


def predict_match(model_artifact: dict, feature_row: dict) -> dict:
    """Generate a placeholder prediction response for a single match payload."""

    return {
        "model_type": model_artifact.get("model_type", "unknown"),
        "predicted_winner": "TBD",
        "confidence": 0.0,
        "input_features": feature_row,
    }
