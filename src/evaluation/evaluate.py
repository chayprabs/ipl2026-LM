"""Evaluation helpers for validating model performance."""

from __future__ import annotations


def evaluate_model(model_artifact: dict, evaluation_data: dict) -> dict:
    """Return placeholder evaluation metrics for a trained model."""

    return {
        "model_type": model_artifact.get("model_type", "unknown"),
        "metrics": {
            "accuracy": None,
            "log_loss": None,
            "roc_auc": None,
        },
        "evaluation_data": evaluation_data,
    }
