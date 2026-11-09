# DEEPOXY — Recovered historical notebook results

**Status: HISTORICAL NOTEBOOK OUTPUTS / PROVISIONAL RESEARCH EVIDENCE.**
These files are recovered from saved displays of the manually executed `epoxty-checking.ipynb` (SHA-256 recorded in `manifest.json`). The original Kaggle results ZIP and full row-level experiment files were **not** available. Do not describe these outputs as externally validated or numerically reproduced.

## What you can inspect now

| Workstream | Result file | Notebook cells (1-based) | Key evidence |
|---|---|---|---|
| Original five-model baseline | [original_five_model_cv_summary.csv](notebook_recovered/original_five_model_cv_summary.csv) | 49, 51 | 5 models × 2 regimes, 4 folds |
| Expanded seven-model benchmark | [seven_model_cv_summary.csv](notebook_recovered/seven_model_cv_summary.csv) | 51 | Includes GPR and MLP |
| Nine-model benchmark | [nine_model_cv_summary.csv](notebook_recovered/nine_model_cv_summary.csv) | 69, 96 | TabICLv2 lowest displayed mean MAE in cryogenic and room |
| Prediction bias/residual summaries | [nine_model_oof_bias_summary.csv](notebook_recovered/nine_model_oof_bias_summary.csv) | 76 | Pooled OOF summaries, **not** the individual prediction rows |
| Exact paired tests | [nine_model_paired_comparisons.csv](notebook_recovered/nine_model_paired_comparisons.csv) | 69, 97 | Holm-adjusted p=0.5 for 4 comparisons |
| Seven-model paired tests | [seven_model_pairwise_tests.csv](notebook_recovered/seven_model_pairwise_tests.csv) | 51 | Multiple tests, limited source groups |
| Optuna tuning | [optuna_model_summary.csv](notebook_recovered/optuna_model_summary.csv) | 54 | Summary metrics, raw trials not recovered |
| Train-only augmentation sensitivity | [augmentation_ablation_summary.csv](notebook_recovered/augmentation_ablation_summary.csv) | 72, 98 | 60 summarized combinations; mixed performance |
| High-temperature exploratory | [high_temperature_exploratory_models.csv](notebook_recovered/high_temperature_exploratory_models.csv) | 94–95 | 42 rows, one source; **not external validation** |
| Held-out permutation importance | [feature_importance_summary.csv](notebook_recovered/feature_importance_summary.csv) | 82 | Association only; **not SHAP or causal proof** |
| OOD diagnostics | [ood_summary.csv](notebook_recovered/ood_summary.csv) | 86, 93 | Small number of out-of-range observations |
| Source evidence status | [source_verification_status.csv](notebook_recovered/source_verification_status.csv) | 100 | 0 independently authenticated observations |
| Recorded interval artifacts | [external_uncertainty_availability.csv](notebook_recovered/external_uncertainty_availability.csv) | 77, 99 | **Presence/counts only; displayed status text is truncated; not full files** |
| Phase 7 reference models | [phase7_reference_model_summary.csv](notebook_recovered/phase7_reference_model_summary.csv) | 82 | Separate later reference experiment |
| Reviewer status ledger | [reviewer_status_counts.csv](notebook_recovered/reviewer_status_counts.csv) | 103 | Notebook's provisional classification |

Every table's blob SHA and provenance are listed in [manifest.json](manifest.json). The 15 CSV files are byte-for-byte preserved from the previously recovered notebook-display archive; **not** claimed to be the original Kaggle-directory CSV files.

## Reviewer-by-reviewer evidence

[reviewer_evidence_index.csv](reviewer_evidence_index.csv) maps all 40 reviewer questions to notebook cells, the recovered tables, and the still-missing evidence. The statuses in that detailed index use a more granular scheme (5 computed, 14 partial, 5 source-blocked, 11 lab-blocked, 5 writing-pending) than the notebook's own 14/10/11/5 ledger. Neither represents reviewer acceptance.

## Regenerated figures

See [figures/recovered](../figures/recovered) for 7 *new SVG charts derived from recovered summary CSVs*:

- Cryogenic nine-model MAE
- Room-temperature nine-model MAE
- High-temperature exploratory MAE
- Selected augmentation ΔMAE
- Cryogenic held-out permutation importance
- Cryogenic out-of-range MAE
- Original observation counts

They are **not** claimed to be the original PNG figures extracted from the notebook. The executed notebook embeds 145 original PNG outputs; those bytes are retained in the local recovered archive, but are not in this Git commit.

## Scientific limits and what remains

- The original 54 + 160 + 42 = 256 rows conflict with the manuscript's 259; discrepancy unresolved.
- Full original Kaggle 176-file ZIP, original prediction-level CSVs and pickle snapshots are not included.
- Dataset publication IDs and source measurements are not independently authenticated.
- The high-temperature experiment involves one publication, so no cross-publication result is proven.
- Real-row effective-medium physical comparisons remain blocked by missing verified units/properties.
- Lab uncertainty and independent real measurement–prediction comparisons were not recovered.
- Later extended notebook appendix computations are not implied to have executed in this original notebook.

**Workflow for manuscript revision:** identify reviewer ID in `reviewer_evidence_index.csv` → open its CSV and figure → inspect exact cell in original executed notebook → check provenance and limitations → only then cite a result or decide to rerun the missing computation.
