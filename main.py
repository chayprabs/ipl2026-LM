"""Main entrypoint for the IPL prediction system."""

from __future__ import annotations

from scripts.run_pipeline import run_pipeline


def main() -> None:
    """Execute the placeholder training pipeline."""

    result = run_pipeline()
    print("IPL prediction system initialized.")
    print(f"Filtered features: {len(result['selected_features'])}")


if __name__ == "__main__":
    main()
