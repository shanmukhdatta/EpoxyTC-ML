"""DEEPOXY independent original-CSV integrity and grouped-validation feasibility audit.

This is a NONTRAINING and NONCORRECTIVE audit. It reads three original CSVs,
never modifies their bytes, and writes evidence tables. Source identities,
loading units and constituent properties are not independently validated.

Usage:
    python verify_data_integrity.py --data-dir <directory with 3 original CSVs> --output-dir <dir>
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

FILES = {
    "cryogenic": ("CRYOGENIC_KAGGLE_READY.csv", 54),
    "room": ("ROOM_KAGGLE_READY.csv", 160),
    "high": ("HIGH_KAGGLE_READY.csv", 42),
}
FEATURES = ["base_tc_w_mk", "filler_tc_w_mk", "filler_loading_as_recorded", "temperature_k_recorded"]
TARGET = "composite_tc_w_mk"
REQUIRED = ["orig_id", "publication_id", TARGET, *FEATURES,
            "source_row_evidence", "source_measurement_type", "filler_loading_unit"]


def _jsonable(value):
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return None if not np.isfinite(value) else float(value)
    return value


def audit(data_dir: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    reg, collisions, source_gate, integrity = [], [], [], []
    encountered_ids = set()
    encountered_sha = {}
    total = 0
    for regime, (filename, expected) in FILES.items():
        path = data_dir / filename
        if not path.is_file():
            raise FileNotFoundError(f"Original CSV missing: {path}; no substitute data are acceptable")
        payload = path.read_bytes()
        encountered_sha[filename] = hashlib.sha256(payload).hexdigest()
        df = pd.read_csv(path)
        missing_columns = set(REQUIRED) - set(df.columns)
        if missing_columns:
            raise ValueError(f"{filename}: required columns missing: {sorted(missing_columns)}")
        if len(df) != expected:
            raise ValueError(f"{filename}: {len(df)} rows rather than expected {expected}")
        if df.orig_id.isna().any() or df.orig_id.duplicated().any():
            raise ValueError(f"{filename}: original row IDs are missing or duplicated")
        if set(df.orig_id) & encountered_ids:
            raise ValueError(f"{filename}: original row IDs overlap another dataset")
        encountered_ids.update(df.orig_id)
        if df.publication_id.isna().any():
            raise ValueError(f"{filename}: publication assignment missing")
        if df[FEATURES[:3] + [TARGET]].isna().any().any():
            raise ValueError(f"{filename}: missing numeric material inputs/target")
        total += len(df)

        # All identical numeric feature vectors share one key, including missing temperatures.
        for _, part in df.groupby(FEATURES, dropna=False, sort=False):
            if len(part) <= 1:
                continue
            measured = part[TARGET].astype(float)
            varying = measured.max() - measured.min()
            for _, rec in part.iterrows():
                collisions.append({
                    "regime": regime, "orig_id": rec.orig_id,
                    "publication_id_provisional": rec.publication_id,
                    **{c: _jsonable(rec[c]) for c in FEATURES},
                    TARGET: float(rec[TARGET]),
                    "colliding_row_ids": ";".join(sorted(part.orig_id.astype(str))),
                    "n_same_feature_rows": int(len(part)),
                    "n_provisional_publications": int(part.publication_id.nunique()),
                    "range_target_k_wmk": float(varying),
                    "interpretation": "SAME_RECORDED_FEATURES_DIFFERENT_TARGETS_NOT_PROOF_OF_LAB_ERROR",
                })
        for _, row in df.iterrows():
            source_gate.append({
                "orig_id": row.orig_id, "regime": regime,
                "publication_id_provisional": row.publication_id,
                "has_row_provenance": bool(pd.notna(row.source_row_evidence)),
                "has_loading_unit": bool(pd.notna(row.filler_loading_unit)),
                "has_measurement_type": bool(pd.notna(row.source_measurement_type)),
                "recorded_temperature": bool(pd.notna(row.temperature_k_recorded)),
                "physical_model_verification_gate": "NOT_SOURCE_AUTHENTICATED",
            })
        n_groups = int(df.publication_id.nunique())
        split = {"train": [], "validation": [], "test": []}
        feasibility = "BLOCKED_FEWER_THAN_3_PUBLICATION_GROUPS"
        n_dev = 0
        if n_groups >= 3:
            outer = GroupShuffleSplit(n_splits=1, test_size=1/n_groups, random_state=42)
            development_idx, test_idx = next(outer.split(df, groups=df.publication_id))
            inner = GroupShuffleSplit(n_splits=1, test_size=1/(n_groups-1), random_state=43)
            tr, va = next(inner.split(df.iloc[development_idx], groups=df.iloc[development_idx].publication_id))
            split["train"] = sorted(df.iloc[development_idx].iloc[tr].publication_id.unique())
            split["validation"] = sorted(df.iloc[development_idx].iloc[va].publication_id.unique())
            split["test"] = sorted(df.iloc[test_idx].publication_id.unique())
            unions = [set(split[k]) for k in ("train", "validation", "test")]
            if any(unions[i] & unions[j] for i in range(3) for j in range(i)):
                raise AssertionError("Publication IDs overlap partitions")
            n_dev = len(unions[0] | unions[1])
            feasibility = "CODE_PATH_FEASIBLE_BUT_SOURCE_IDS_PROVISIONAL" if n_dev >= 4 else "CODE_PATH_HAS_TOO_FEW_DEVELOPMENT_GROUPS"
        a = {
            "regime": regime, "original_rows": int(len(df)),
            "provisional_publications": n_groups,
            "recorded_temperature_rows": int(df.temperature_k_recorded.notna().sum()),
            "explicit_filler_loading_unit_rows": int(df.filler_loading_unit.notna().sum()),
            "row_level_source_evidence_rows": int(df.source_row_evidence.notna().sum()),
            "source_measurement_type_rows": int(df.source_measurement_type.notna().sum()),
            "development_publication_count": n_dev,
            "train_publications": ";".join(split["train"]),
            "validation_publications": ";".join(split["validation"]),
            "test_publications": ";".join(split["test"]),
            "grouped_cv_code_feasibility": feasibility,
            "fully_source_authenticated_rows": 0,
            "source_authentication_note": "ASSIGNMENTS_ARE_PROVISIONAL_NOT_VALIDATED_PAPER_SPECIMENS",
        }
        reg.append(a)
        integrity.append({"regime": regime, "filename": filename, "sha256": encountered_sha[filename],
                          "rows": len(df), "distinct_row_ids": df.orig_id.nunique(),
                          "same_recorded_feature_rows": int(df.duplicated(FEATURES, keep=False).sum()),
                          "exact_feature_and_target_duplicates": int(df.duplicated(FEATURES + [TARGET], keep=False).sum())})

    reg_df = pd.DataFrame(reg)
    coll_df = pd.DataFrame(collisions)
    gate_df = pd.DataFrame(source_gate)
    integrity_df = pd.DataFrame(integrity)
    for fname, obj in [
        ("regime_validation_gates.csv", reg_df),
        ("same_input_different_target_rows.csv", coll_df),
        ("source_authentication_gate_256.csv", gate_df),
        ("input_file_hashes.csv", integrity_df),
    ]:
        obj.to_csv(output_dir / fname, index=False)
    assert total == 256 and gate_df.orig_id.nunique() == 256
    assert int(coll_df.n_same_feature_rows.eq(2).sum()) == 6, "Expected three two-row collisions in room data"
    assert len(reg_df) == 3
    assert int(reg_df.row_level_source_evidence_rows.sum()) == 0
    assert int(reg_df.explicit_filler_loading_unit_rows.sum()) == 0
    assert int(reg_df.source_measurement_type_rows.sum()) == 0
    summary = {
        "verification": "PASS_FOR_SCHEMA_COUNTS_GROUP_SPLIT_AND_FEATURE_COLLISION_AUDIT",
        "original_rows": total,
        "original_csv_names": list(encountered_sha),
        "original_input_sha256": encountered_sha,
        "provisional_publications": 11,
        "regimes_group_splittable_by_code": 2,
        "regimes_blocked_by_single_publication": ["high"],
        "rows_with_missing_filler_loading_unit": 256,
        "rows_with_missing_row_level_evidence": 256,
        "rows_with_missing_measurement_type": 256,
        "room_rows_with_missing_actual_temperature": 160,
        "same_feature_vector_conflicting_target_groups": int(coll_df.colliding_row_ids.nunique()),
        "same_feature_vector_conflicting_target_rows": len(coll_df),
        "original_rows_physics_experimentally_authenticated": 0,
        "note": "This is a nontraining verification of recorded data, not validation of source identities, physical models or experimental observations.",
    }
    (output_dir / "verification_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data-dir", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(audit(args.data_dir, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
