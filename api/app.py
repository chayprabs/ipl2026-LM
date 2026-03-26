"""FastAPI application placeholder for IPL match predictions."""

from __future__ import annotations

from fastapi import FastAPI


app = FastAPI(title="IPL Prediction System API")


@app.get("/predict")
def predict() -> dict:
    """Return a dummy prediction response until the inference layer is implemented."""

    return {
        "predicted_winner": "TBD",
        "confidence": 0.0,
        "status": "placeholder",
    }
