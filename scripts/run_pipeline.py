#!/usr/bin/env python3
"""Validate available originals and save EDA summaries; training is never implicit."""
import argparse
import json
from pathlib import Path

from src.data import HISTORICAL_ROWS, load_original_datasets, load_public_datasets
from src.eda import summarize
from src.reporting import save_config, save_csv


def execute(data_dir, output_dir, allow_row_count_mismatch=False, data_format='original'):
    if data_format not in ('original', 'processed'):
        raise ValueError('Unsupported data_format')
    loaded = (load_original_datasets(data_dir) if data_format == 'original'
              else load_public_datasets(data_dir))
    output = Path(output_dir)
    audits = {}
    for regime, (frame, audit) in loaded.items():
        if (audit["row_count_matches"] is False and not allow_row_count_mismatch):
            raise ValueError(f"{regime}: {len(frame)} rows, expected {HISTORICAL_ROWS[regime]}; "
                             "supply --allow-row-count-mismatch only after investigation")
        stats = summarize(frame)
        save_csv(stats["numeric_summary"].reset_index(), output / f"{regime}_numeric_summary.csv")
        audits[regime] = {**audit, "n_duplicates_including_copies": int(stats["duplicates"].sum())}
    manifest = {"data": audits, "data_format": data_format, "training_performed": False,
                "scientific_validation": "PENDING_ROW_LEVEL_SOURCE_AUTHENTICATION"}
    save_config(manifest, output / "dataset_audit.json")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--output-dir", default="build/eda-audit")
    parser.add_argument("--data-format", choices=["original", "processed"], default="original")
    parser.add_argument("--allow-row-count-mismatch", action="store_true")
    args = parser.parse_args(argv)
    print(json.dumps(execute(args.data_dir, args.output_dir,
                             args.allow_row_count_mismatch, args.data_format), indent=2, default=str))


if __name__ == "__main__":
    main()
