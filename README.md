<<<<<<< HEAD
# IPL Prediction System

This repository provides a clean backend skeleton for an IPL match prediction workflow. It is organized so data ingestion, feature filtering, feature building, model training, inference, and evaluation each live in separate modules.

## Project Structure

```text
ipl_prediction_system/
|-- data/
|   |-- raw/
|   |-- interim/
|   `-- processed/
|-- src/
|   |-- data/
|   |-- features/
|   |-- feature_selection/
|   |-- models/
|   |-- inference/
|   |-- evaluation/
|   `-- utils/
|-- configs/
|-- notebooks/
|-- tests/
|-- logs/
|-- scripts/
|-- api/
|-- requirements.txt
|-- README.md
|-- main.py
`-- .gitignore
```

## Pipeline Flow

The training pipeline follows a simple modular sequence:

1. Load raw match and supporting data.
2. Filter candidate features based on data availability and validity.
3. Build the selected feature set.
4. Train a placeholder model artifact.

The API layer is intentionally minimal and currently exposes a dummy `/predict` endpoint.

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the placeholder training pipeline:

```bash
python main.py
```

Run the API locally:

```bash
uvicorn api.app:app --reload
```
=======
# ipl2026-LM
A prediction model based on pre-match data for Indian Premier League 2026.
>>>>>>> db0d7fb5ca66bf72f7100a3e094d8021a0d51ebe
