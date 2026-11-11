"""Ensure the DEEPOXY results folder is flat and preserves all curated CSV data."""
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/"results"
FILES=("augmentation_ablation_summary.csv","external_uncertainty_availability.csv","feature_importance_summary.csv","high_temperature_exploratory_models.csv","nine_model_cv_summary.csv","nine_model_oof_bias_summary.csv","nine_model_paired_comparisons.csv","ood_summary.csv","optuna_model_summary.csv","original_five_model_cv_summary.csv","phase7_reference_model_summary.csv","reviewer_status_counts.csv","seven_model_cv_summary.csv","seven_model_pairwise_tests.csv","source_verification_status.csv","source_experiment_model_comparisons.csv","lab_figure3_digitized_approx.csv","lab_fig3_forward_model_scenarios.csv","lab_fig3_maxwell_inverse_checks.csv","lab_fig3_geometry_sensitivity.csv","lab_fig3_group_plausibility.csv","manuscript_physics_300k_matrix_sensitivity.csv","manuscript_tables_2_4_6_recalculated_errors.csv","physical_property_source_register.csv","physics_reviewer_comment_coverage.csv","source_authentication_gate_256.csv","regime_validation_gates.csv","same_input_different_target_rows.csv","input_file_hashes.csv")

def test_recovered_csvs_are_flat_and_readable():
    actual=sorted(p.name for p in RESULTS.iterdir())
    assert actual==sorted([*FILES,"README.md"])
    assert not any(p.is_dir() for p in RESULTS.iterdir())
    for filename in FILES:
        df=pd.read_csv(RESULTS/filename)
        assert len(df)>0, filename
        assert len(df.columns)>1,filename

def test_historical_and_new_evidence_shapes():
    expected={
        "nine_model_cv_summary.csv":18,
        "augmentation_ablation_summary.csv":60,
        "nine_model_paired_comparisons.csv":4,
        "high_temperature_exploratory_models.csv":3,
        "source_experiment_model_comparisons.csv":11,
        "lab_figure3_digitized_approx.csv":30,
        "manuscript_physics_300k_matrix_sensitivity.csv":10,
        "lab_fig3_forward_model_scenarios.csv":15,
        "manuscript_tables_2_4_6_recalculated_errors.csv":16,
        "source_authentication_gate_256.csv":256,
        "same_input_different_target_rows.csv":6,
    }
    for name,n in expected.items():
        assert len(pd.read_csv(RESULTS/name))==n
    assert len(pd.read_csv(ROOT/"docs"/"evidence"/"reviewer_evidence_index.csv"))==40

def test_single_readme_links_every_csv_and_preserves_tools():
    content=(RESULTS/"README.md").read_text(encoding="utf8")
    for name in FILES:
        assert "]("+name+")" in content
    for name in ["physics_ref23_models.svg","physics_lab_figure3_300k.svg"]:
        assert (ROOT/"figures"/name).is_file()
    for name in ["verify_physics_results.py","verify_data_integrity.py"]:
        assert (ROOT/"scripts"/name).is_file()
