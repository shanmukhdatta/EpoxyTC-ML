#!/usr/bin/env python3
"""Validate available originals and save EDA summaries; training is never implicit."""
import argparse
import json
from pathlib import Path

from deepoxy.data import HISTORICAL_ROWS, load_original_datasets
from deepoxy.eda import summarize
from deepoxy.reporting import save_config, save_csv


def execute(data_dir, output_dir, allow_row_count_mismatch=False):
    loaded = load_original_datasets(data_dir)
    output = Path(output_dir)
    audits = {}
    for regime, (frame, audit) in loaded.items():
        if (audit["row_count_matches"] is False and not allow_row_count_mismatch):
            raise ValueError(f"{regime}: {len(frame)} rows, expected {HISTORICAL_ROWS[regime]}; "
                             "supply --allow-row-count-mismatch only after investigation")
        stats = summarize(frame)
        save_csv(stats["numeric_summary"].reset_index(), output / f"{regime}_numeric_summary.csv")
        audits[regime] = {**audit, "n_duplicates_including_copies": int(stats["duplicates"].sum())}
    manifest = {"data": audits, "training_performed": False,
                "scientific_validation": "PENDING_ROW_LEVEL_SOURCE_AUTHENTICATION"}
    save_config(manifest, output / "dataset_audit.json")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--allow-row-count-mismatch", action="store_true")
    args = parser.parse_args(argv)
    print(json.dumps(execute(args.data_dir, args.output_dir,
                             args.allow_row_count_mismatch), indent=2, default=str))


if __name__ == "__main__":
    main()
