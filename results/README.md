# Results archive: exact file index and interpretation

This directory contains **26 currently tracked CSV tables**, all directly inside `results/` (no nested result folders). Saved historical model results have **not been retrained** by reorganizing or documenting this archive. Figures are indexed in [figures/](../figures/README.md).

## A. Historical saved machine-learning summaries (14 CSVs)

These are inspectable **archived notebook summaries**, not a release of per-row predictions, the original frozen split assignments, full Optuna trial histories, or pretrained checkpoints.

| CSV | Interpretation |
| --- | --- |
| [augmentation_ablation_summary.csv](augmentation_ablation_summary.csv) | Saved exploratory augmentation/control comparisons |
| [external_uncertainty_availability.csv](external_uncertainty_availability.csv) | Availability of historical uncertainty exports; not raw instrument uncertainties |
| [feature_importance_summary.csv](feature_importance_summary.csv) | Reported feature-importance diagnostics |
| [high_temperature_exploratory_models.csv](high_temperature_exploratory_models.csv) | Exploratory models in a single-source high-temperature regime |
| [nine_model_cv_summary.csv](nine_model_cv_summary.csv) | Nine-model, four-provisional-development-fold summaries for cryogenic and room data |
| [nine_model_oof_bias_summary.csv](nine_model_oof_bias_summary.csv) | Pooled out-of-fold errors and bias summaries, not row-level predictions |
| [nine_model_paired_comparisons.csv](nine_model_paired_comparisons.csv) | Four paired model comparisons with adjusted p-values |
| [ood_summary.csv](ood_summary.csv) | Recorded outside-training-range diagnostics |
| [optuna_model_summary.csv](optuna_model_summary.csv) | Tuning result summaries, not all trial records |
| [original_five_model_cv_summary.csv](original_five_model_cv_summary.csv) | Original five-model comparison |
| [phase7_reference_model_summary.csv](phase7_reference_model_summary.csv) | Later reference-model summary |
| [reviewer_status_counts.csv](reviewer_status_counts.csv) | Historical reviewer-evidence status counts |
| [seven_model_cv_summary.csv](seven_model_cv_summary.csv) | Seven-model comparison |
| [seven_model_pairwise_tests.csv](seven_model_pairwise_tests.csv) | Saved exploratory paired tests |

**Interpretation:** The lowest saved mean-fold MAEs in the nine-model table are 0.06264 W/(m·K) (cryogenic) and 0.18339 W/(m·K) (room) for TabICLv2. Four recorded comparisons have Holm-adjusted `p = 0.50`: descriptive rankings are **not demonstrations of significant superiority**. The high-temperature table comes from one provisional publication; no publication-held-out generalization is established.

## B. Conditional physical-model and manuscript-number analyses (10 CSVs)

| CSV | Interpretation |
| --- | --- |
| [source_experiment_model_comparisons.csv](source_experiment_model_comparisons.csv) | 11 conditional source-reconstructed cases |
| [lab_figure3_digitized_approx.csv](lab_figure3_digitized_approx.csv) | 30 approximately digitized manuscript plot readings |
| [lab_fig3_forward_model_scenarios.csv](lab_fig3_forward_model_scenarios.csv) | 15 proxy-property forward-model scenarios |
| [lab_fig3_maxwell_inverse_checks.csv](lab_fig3_maxwell_inverse_checks.csv) | Inverse Maxwell checks for the graph readings |
| [lab_fig3_geometry_sensitivity.csv](lab_fig3_geometry_sensitivity.csv) | Filler geometry/packing sensitivity |
| [lab_fig3_group_plausibility.csv](lab_fig3_group_plausibility.csv) | Filler/temperature-group plausibility checks |
| [manuscript_tables_2_4_6_recalculated_errors.csv](manuscript_tables_2_4_6_recalculated_errors.csv) | 16 saved manuscript-table error comparisons |
| [physical_property_source_register.csv](physical_property_source_register.csv) | Literature-supported constituent-property register |
| [physics_reviewer_comment_coverage.csv](physics_reviewer_comment_coverage.csv) | Physics-related reviewer evidence status |
| [manuscript_physics_300k_matrix_sensitivity.csv](manuscript_physics_300k_matrix_sensitivity.csv) | Ten revised 300 K cases under two matrix-property assumptions |

The computations can be replayed **arithmetically** with `src/physics.py`. Approximate graph reading, external epoxy/filler property values, filler volume/shape assumptions, and sample identity are **not independent laboratory verification**. In particular, the 1.064 W/(m·K) epoxy assumption in the revised sensitivity table comes from a **different published material batch** ([Cryogenics 2024](https://doi.org/10.1016/j.cryogenics.2024.103973)); favorable conditional model error under that assumption is not verified specimen-specific predictive accuracy.

See [physics comparison figure](../figures/physics_ref23_models.svg), [approximate Figure 3 reconstruction](../figures/physics_lab_figure3_300k.svg), and [updated matrix sensitivity plot](../figures/physics_matrix_sensitivity_300k.svg).

## C. Saved input-integrity evidence (2 CSVs)

| CSV | Interpretation |
| --- | --- |
| [input_file_hashes.csv](input_file_hashes.csv) | Previously recorded hashes/counts of the **full original** CSV files |
| [same_input_different_target_rows.csv](same_input_different_target_rows.csv) | Six room records from three equal-input/different-target pairs |

The 256-row source authentication and regime validation tables named in **older documentation are not present in the current repository**. Do not follow or cite dead links to `source_authentication_gate_256.csv`, `regime_validation_gates.csv`, or `source_verification_status.csv`. The recorded earlier verification summary survives as [dataset_verification_summary.json](../docs/evidence/dataset_verification_summary.json), but that JSON is **not equivalent to those missing row-level CSVs**.

The three room collision pairs imply a theoretical **full-dataset deterministic-fit** error floor of MAE 0.0081875 and RMSE 0.0528471 W/(m·K), for regressors restricted to exactly four recorded features. These are not held-out scores; read the [collision audit](../docs/evidence/room_feature_collision_finding.md).

## Verify without changing results

Run from repository root:

```bash
python -m pytest -q
python scripts/verify_public_datasets.py
python scripts/verify_physics_results.py
```

These checks use present public assets. For a **fresh** original 24-column data/provenance audit, separately provide the original three CSVs and run:

```bash
python scripts/verify_data_integrity.py --data-dir /path/to/full-originals --output-dir build/original-audit
```

This last command **cannot** be performed with the public six-column exports. Use `build/` or another new output folder rather than overwriting archived results. [Full reproducibility protocol](../docs/reproducibility.md) · [Reviewer evidence index](../docs/evidence/reviewer_evidence_index.csv) · [Dataset index](../data/README.md).
