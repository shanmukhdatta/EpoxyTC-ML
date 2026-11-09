#!/usr/bin/env python3
"""Run explicit grouped nested CV or reuse saved row-level predictions."""
import argparse
import json
from pathlib import Path
import pandas as pd

from src.training import core_nested_cv
from src.evaluation import evaluate_prediction_table
from src.reporting import load_verified_predictions, save_csv, save_config


def execute(data_path=None, output_dir="results", models=("ExtraTrees",),
            n_search=8, reuse_predictions=None):
    out = Path(output_dir)
    if reuse_predictions is not None:
        predictions = load_verified_predictions(reuse_predictions)
        metrics = evaluate_prediction_table(predictions)
        mode = "REUSED_VERIFIED_SCHEMA_ONLY"
        save_csv(metrics, out / "recomputed_metrics.csv")
        source = str(reuse_predictions)
    else:
        if data_path is None:
            raise ValueError("--data is required for training; use --reuse-predictions otherwise")
        frame = pd.read_csv(data_path)
        needed = {"split", "publication_id", "composite_tc_w_mk"}
        if not needed.issubset(frame):
            raise ValueError("Training requires authentic frozen split assignments; missing: "
                             + str(sorted(needed - set(frame))))
        metrics, predictions, tuning = core_nested_cv(frame, model_names=models,
                                                       n_search=n_search, n_jobs=1)
        save_csv(predictions, out / "new_cv_predictions.csv")
        save_csv(metrics, out / "new_cv_fold_metrics.csv")
        save_csv(tuning, out / "new_cv_tuning.csv")
        mode = "NEW_GROUPED_NESTED_CV"
        source = str(data_path)
    save_config({"mode": mode, "source": source, "models_requested": list(models),
                 "no_final_test_scored": mode == "NEW_GROUPED_NESTED_CV",
                 "historical_parity": "NOT_ESTABLISHED"}, out / "experiment_manifest.json")
    return metrics


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data")
    parser.add_argument("--reuse-predictions")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--models", nargs="+", default=["ExtraTrees"])
    parser.add_argument("--n-search", type=int, default=8)
    args = parser.parse_args(argv)
    table = execute(args.data, args.output_dir, args.models,
                    args.n_search, args.reuse_predictions)
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
