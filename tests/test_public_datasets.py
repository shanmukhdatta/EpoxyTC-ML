"""Checks for the tracked public data and revised 300 K conditional calculations."""
import csv
from pathlib import Path
from scripts.verify_public_datasets import audit
from src.physics import maxwell_eucken, bruggeman_symmetric

ROOT = Path(__file__).resolve().parents[1]


def test_public_tables_have_expected_rows_and_missingness():
    result = audit(ROOT / "data" / "processed")
    assert result["original_row_count"] == 256
    assert [result["regimes"][name]["rows"] for name in ("cryogenic", "room", "high")] == [54,160,42]
    assert result["regimes"]["room"]["missing_actual_temperature_rows"] == 160
    assert result["regimes"]["room"]["same_input_different_target_groups"] == 3
    assert len(result["regimes"]["high"]["source_ref_counts_provisional"]) == 1


def test_revised_manuscript_physics_table_matches_equations():
    with (ROOT / "results" / "manuscript_physics_300k_matrix_sensitivity.csv").open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 10
    for row in rows:
        km_lo, km_hi = float(row["km_low_proxy_w_mk"]), float(row["km_cross_study_w_mk"])
        kf, phi = float(row["kf_proxy_w_mk"]), float(row["volume_fraction"])
        for calc, col in (
            (maxwell_eucken(km_lo,kf,phi), "maxwell_low_w_mk"),
            (maxwell_eucken(km_hi,kf,phi), "maxwell_cross_study_w_mk"),
            (bruggeman_symmetric(km_hi,kf,phi), "bruggeman_cross_study_w_mk"),
        ):
            assert abs(calc - float(row[col])) < 0.00061
