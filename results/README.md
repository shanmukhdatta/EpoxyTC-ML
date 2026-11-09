# DEEPOXY — Flat results directory

**One directory, CSV files only (plus this README).** The former `results/physics/` and `results/verification/` subdirectories have been removed; their useful CSV evidence is directly here. The original 15 notebook CSVs are preserved byte-for-byte. **Total: 28 CSV tables**.

## A. Original Kaggle notebook results — 15 CSV files

These are historical saved notebook output tables; they were not retrained during this cleanup. Publication/material identity is still provisional.

| CSV file | Description |
|---|---|
| [`augmentation_ablation_summary.csv`](augmentation_ablation_summary.csv) | Saved exploratory augmentation comparisons |
| [`external_uncertainty_availability.csv`](external_uncertainty_availability.csv) | Availability of retrospective uncertainty exports; not raw laboratory data |
| [`feature_importance_summary.csv`](feature_importance_summary.csv) | Saved permutation feature importance |
| [`high_temperature_exploratory_models.csv`](high_temperature_exploratory_models.csv) | Within-single-publication high-temperature model metrics |
| [`nine_model_cv_summary.csv`](nine_model_cv_summary.csv) | Nine-model grouped-development summaries (18 rows) |
| [`nine_model_oof_bias_summary.csv`](nine_model_oof_bias_summary.csv) | Pooled OOF/bias summaries, not row-level predictions |
| [`nine_model_paired_comparisons.csv`](nine_model_paired_comparisons.csv) | Four exploratory matched-fold comparisons |
| [`ood_summary.csv`](ood_summary.csv) | Feature-range OOD diagnostics |
| [`optuna_model_summary.csv`](optuna_model_summary.csv) | Tuning summaries, not full trial logs |
| [`original_five_model_cv_summary.csv`](original_five_model_cv_summary.csv) | Original five-model benchmark |
| [`phase7_reference_model_summary.csv`](phase7_reference_model_summary.csv) | Later reference-model summary |
| [`reviewer_status_counts.csv`](reviewer_status_counts.csv) | Historical reviewer-progress counts |
| [`seven_model_cv_summary.csv`](seven_model_cv_summary.csv) | Seven-model benchmark |
| [`seven_model_pairwise_tests.csv`](seven_model_pairwise_tests.csv) | Exploratory paired statistical tests |
| [`source_verification_status.csv`](source_verification_status.csv) | Original source-count and provenance gaps |

## B. Physical equations and experimental comparisons — 9 CSV files

These are limited, **conditional** model comparisons using reported experiments, approximate graph readings and/or literature-supported constituent properties. Maxwell–Eucken, Bruggeman, Hamilton–Crosser, Lewis–Nielsen and Hashin–Shtrikman are implemented in [`src/physics.py`](../src/physics.py).

| CSV file | Description |
|---|---|
| [`source_experiment_model_comparisons.csv`](source_experiment_model_comparisons.csv) | 11 conditional source-reconstructed physical-model cases |
| [`lab_figure3_digitized_approx.csv`](lab_figure3_digitized_approx.csv) | 30 approximate manuscript Figure 3 plot readings |
| [`lab_fig3_forward_model_scenarios.csv`](lab_fig3_forward_model_scenarios.csv) | 15 literature-proxy forward-model scenarios |
| [`lab_fig3_maxwell_inverse_checks.csv`](lab_fig3_maxwell_inverse_checks.csv) | 30 inverse/high-filler-conductivity Maxwell checks |
| [`lab_fig3_geometry_sensitivity.csv`](lab_fig3_geometry_sensitivity.csv) | Geometry and packing sensitivity scenarios |
| [`lab_fig3_group_plausibility.csv`](lab_fig3_group_plausibility.csv) | Six filler × temperature plausibility summaries |
| [`manuscript_tables_2_4_6_recalculated_errors.csv`](manuscript_tables_2_4_6_recalculated_errors.csv) | 16 manuscript numerical error comparisons; some references provisional |
| [`physical_property_source_register.csv`](physical_property_source_register.csv) | Literature property inputs, sources and temperature limits |
| [`physics_reviewer_comment_coverage.csv`](physics_reviewer_comment_coverage.csv) | 17 physics-related reviewer question statuses |

Recorded computation scope: **11** source-reconstructed comparison cases, **30** approximately digitized manuscript Figure 3 observations, **15** forward-model scenarios, and **16** manuscript-table error comparisons. The 158 arithmetic replay checks confirm computational consistency, **not** exact-specimen experimental validity.

Plots are kept in the existing [`figures/`](../figures/README.md): [REF_23 physics comparison](../figures/physics_ref23_models.svg), [digitized lab Figure 3](../figures/physics_lab_figure3_300k.svg).

## C. Dataset source integrity — 4 CSV files

| CSV file | Description |
|---|---|
| [`source_authentication_gate_256.csv`](source_authentication_gate_256.csv) | All 256 original observations and their source-evidence gate |
| [`regime_validation_gates.csv`](regime_validation_gates.csv) | Three-regime counts, publication-group split feasibility |
| [`same_input_different_target_rows.csv`](same_input_different_target_rows.csv) | Six room observations with identical recorded inputs but different targets |
| [`input_file_hashes.csv`](input_file_hashes.csv) | SHA256 digests of the unmodified original raw datasets |

The cryogenic, room and high datasets comprise **54, 160 and 42 rows** (256 total), associated with 5, 5 and 1 **provisional** source groups. **0/256 rows** have fully authenticated original specimen and loading-unit evidence. Therefore no universal physical verification or publication-held-out validation of the single-source high-temperature set can be claimed.

Three pairs (six rows) in the room dataset have identical recorded four-feature input vectors but differing target conductivity values. Their implied full-recorded-data deterministic-fit error floor is **MAE 0.0081875** and **RMSE 0.0528471 W/(m·K)**. These are mathematical lower bounds, **not held-out model scores**.

## Reproduce the checks

```bash
python -m pytest -q
python scripts/verify_physics_results.py
python scripts/verify_data_integrity.py --data-dir /path/to/original/CSVs --output-dir /path/to/new/audit
```

The original input CSVs are not committed. The second script requires them; use an output directory **outside `results/`** to preserve these curated tables. The physics script replays the saved results using the actual `src/physics.py` equations.

Related context is in [`docs/evidence/`](../docs/evidence/), including [conditional paper-ready physics text](../docs/evidence/physics_paper_ready.md), [collision details](../docs/evidence/room_feature_collision_finding.md), [blank raw-lab input template](../docs/evidence/lab_measurement_input_template.csv) and the [40-question reviewer index](../docs/evidence/reviewer_evidence_index.csv).

## Scientific limitations

- Graph digitization tolerance is **not** experimental uncertainty or a GUM calibration budget.
- External epoxy/filler conductivity, density, shape and packing assumptions are **not automatically valid for the exact specimens**.
- Original row source assignments and filler-loading units need independent authentication.
- The notebook's stated 259 observations versus the available 256 original CSV rows remain unresolved.
- No new model training, original-row replacement or data correction was performed by this directory reorganization.
