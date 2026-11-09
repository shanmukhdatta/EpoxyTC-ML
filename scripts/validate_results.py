#!/usr/bin/env python3
"""Validate saved predictions and recompute metrics without fitting models."""
import argparse
import json
from pathlib import Path

from src.data import sha256_file
from src.evaluation import evaluate_prediction_table
from src.reporting import load_verified_predictions, save_csv, save_config


def execute(predictions_path, output_dir):
    records = load_verified_predictions(predictions_path)
    metrics = evaluate_prediction_table(records)
    output = Path(output_dir)
    save_csv(metrics, output / "validated_recomputed_metrics.csv")
    manifest = {
        "predictions_path": str(predictions_path),
        "predictions_sha256": sha256_file(predictions_path),
        "rows": len(records),
        "status": "SCHEMA_AND_NUMERICAL_METRICS_VALIDATED",
        "scientific_provenance_verified": False,
        "notebook_numerical_parity_verified": False,
    }
    save_config(manifest, output / "validation_manifest.json")
    return manifest


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--predictions", required=True)
    p.add_argument("--output-dir", default="results")
    args = p.parse_args(argv)
    print(json.dumps(execute(args.predictions, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
