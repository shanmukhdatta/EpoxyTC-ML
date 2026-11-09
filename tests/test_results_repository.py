"""The curated results are real recovered historical CSVs, not fabricated model runs."""
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FILES = (
    "augmentation_ablation_summary.csv",
    "external_uncertainty_availability.csv",
    "feature_importance_summary.csv",
    "high_temperature_exploratory_models.csv",
    "nine_model_cv_summary.csv",
    "nine_model_oof_bias_summary.csv",
    "nine_model_paired_comparisons.csv",
    "ood_summary.csv",
    "optuna_model_summary.csv",
    "original_five_model_cv_summary.csv",
    "phase7_reference_model_summary.csv",
    "reviewer_status_counts.csv",
    "seven_model_cv_summary.csv",
    "seven_model_pairwise_tests.csv",
    "source_verification_status.csv",
)


def test_recovered_csvs_are_at_results_root_and_readable():
    actual = sorted(p.name for p in RESULTS.glob("*.csv"))
    assert actual == sorted(FILES)
    for filename in FILES:
        frame = pd.read_csv(RESULTS / filename)
        assert len(frame) > 0, filename
        assert len(frame.columns) > 1, filename
    assert not (RESULTS / "notebook_recovered").exists()


def test_recorded_scientific_structure_and_reviewer_metadata_location():
    assert len(pd.read_csv(RESULTS / "nine_model_cv_summary.csv")) == 18
    assert len(pd.read_csv(RESULTS / "augmentation_ablation_summary.csv")) == 60
    assert len(pd.read_csv(RESULTS / "nine_model_paired_comparisons.csv")) == 4
    assert len(pd.read_csv(RESULTS / "high_temperature_exploratory_models.csv")) == 3
    assert len(pd.read_csv(ROOT / "docs" / "evidence" / "reviewer_evidence_index.csv")) == 40

    for name in ("manifest.json", "metrics_snapshot.json", "reviewer_evidence_index.csv"):
        assert not (RESULTS / name).exists()
        assert (ROOT / "docs" / "evidence" / name).exists()


def test_readme_links_point_to_existing_local_files():
    content = (RESULTS / "README.md").read_text(encoding="utf8")
    for filename in FILES:
        assert f"]({filename})" in content
