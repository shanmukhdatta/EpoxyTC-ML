#!/usr/bin/env python3
"""Read-only verification of the committed six-column public CSV datasets."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLS = ("base_tc_w_mk", "filler_tc_w_mk", "filler_loading_as_recorded",
        "temperature_k_recorded", "composite_tc_w_mk", "source_ref")
FILES = {
    "cryogenic": ("CRYOGENIC.csv", 54, 5, "29e84afc8e8d9e63bda07b668c423686fa31df3ffc53c02292d2bd76152f680d"),
    "room": ("ROOM.csv", 160, 5, "2143d2b4cc8aa71c7361a4394d0f5f685438a3384481a0a0ed394d12eadfc422"),
    "high": ("HIGH.csv", 42, 1, "be3da1d568c441a42c8b580fa577a07b5c44d613799f5f56e2621e286d8933b6"),
}


def audit(directory: Path, strict_hashes: bool = True) -> dict:
    summary = {}
    for regime, (filename, expected_rows, n_sources, expected_hash) in FILES.items():
        path = Path(directory) / filename
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if strict_hashes and digest != expected_hash:
            raise ValueError(f"{filename}: SHA-256 mismatch; review all data edits")
        with path.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            if tuple(reader.fieldnames or ()) != COLS:
                raise ValueError(f"{filename}: expected exactly {COLS}, got {reader.fieldnames}")
            rows = list(reader)
        if len(rows) != expected_rows:
            raise ValueError(f"{filename}: expected {expected_rows}, got {len(rows)}")
        labels, feature_vectors = Counter(), defaultdict(list)
        missing_t = 0
        for index, rec in enumerate(rows, start=1):
            for key in (COLS[0], COLS[1], COLS[2], COLS[4]):
                try:
                    v = float(rec[key])
                except (ValueError, TypeError) as exc:
                    raise ValueError(f"{filename} row {index}: invalid numeric {key}") from exc
                if not math.isfinite(v) or v < 0 or (key != COLS[2] and v == 0):
                    raise ValueError(f"{filename} row {index}: out-of-domain numeric {key}")
            temperature = rec[COLS[3]]
            if temperature == "":
                missing_t += 1
            else:
                try:
                    v = float(temperature)
                except (ValueError, TypeError) as exc:
                    raise ValueError(f"{filename} row {index}: bad temperature") from exc
                if not math.isfinite(v) or v <= 0:
                    raise ValueError(f"{filename} row {index}: invalid temperature")
            if regime == "room" and temperature != "":
                raise ValueError("ROOM: no observed per-row temperatures were recorded")
            if regime != "room" and temperature == "":
                raise ValueError(f"{filename} row {index}: missing recorded temperature")
            ref = rec["source_ref"]
            if not re.fullmatch(r"\[[0-9]+\]", ref or ""):
                raise ValueError(f"{filename} row {index}: invalid source label")
            labels[ref] += 1
            feature_vectors[tuple(rec[c] for c in COLS[:4])].append(float(rec[COLS[4]]))
        if len(labels) != n_sources:
            raise ValueError(f"{filename}: number of provisional sources changed")
        conflicts = sum(len(set(ys)) > 1 for ys in feature_vectors.values())
        if conflicts != (3 if regime == "room" else 0):
            raise ValueError(f"{filename}: identical-input/different-target grouping changed")
        summary[regime] = {
            "rows": len(rows), "sha256": digest,
            "source_ref_counts_provisional": dict(sorted(labels.items())),
            "missing_actual_temperature_rows": missing_t,
            "same_input_different_target_groups": conflicts,
        }
    return {
        "verification": "PASS_FOR_SIX_COLUMN_SCHEMA_AND_RECORDED_VALUES_ONLY",
        "original_row_count": sum(s["rows"] for s in summary.values()),
        "original_source_authentication": "NOT_VERIFIED",
        "training_performed": False, "regimes": summary,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir", type=Path, default=ROOT / "data" / "processed")
    p.add_argument("--allow-hash-mismatch", action="store_true",
                   help="diagnostic mode only; schema/count checks still run")
    args = p.parse_args()
    print(json.dumps(audit(args.data_dir, strict_hashes=not args.allow_hash_mismatch), indent=2))


if __name__ == "__main__":
    main()
