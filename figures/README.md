# Figures and numerical sources

There are **10 tracked SVG files** in this directory: **seven** plots based on recovered historical saved results and **three** conditional physics/sensitivity visualizations. They are not the original embedded notebook PNGs and were not produced by retraining historical ML models.

| SVG figure | What is displayed | Linked source |
| --- | --- | --- |
| [cryogenic_nine_model_mean_fold_mae.svg](cryogenic_nine_model_mean_fold_mae.svg) | Historical nine-model cryogenic development-fold MAE | [Nine-model CSV](../results/nine_model_cv_summary.csv) |
| [room_nine_model_mean_fold_mae.svg](room_nine_model_mean_fold_mae.svg) | Historical room development-fold MAE | [Nine-model CSV](../results/nine_model_cv_summary.csv) |
| [high_temperature_exploratory_mae.svg](high_temperature_exploratory_mae.svg) | Single-publication exploratory MAE | [High-temp CSV](../results/high_temperature_exploratory_models.csv) |
| [augmentation_selected_delta_mae.svg](augmentation_selected_delta_mae.svg) | Selected recorded MAE changes with augmentation | [Ablation CSV](../results/augmentation_ablation_summary.csv) |
| [cryogenic_gradientboosting_permutation_importance.svg](cryogenic_gradientboosting_permutation_importance.svg) | Permutation importance, not causal attribution or SHAP | [Importance CSV](../results/feature_importance_summary.csv) |
| [cryogenic_ood_mae.svg](cryogenic_ood_mae.svg) | Errors for the recorded outside-training-range cryogenic subset | [OOD CSV](../results/ood_summary.csv) |
| [record_counts_by_regime.svg](record_counts_by_regime.svg) | Recorded 54/160/42 regime counts | [Dataset index](../data/README.md) |
| [physics_ref23_models.svg](physics_ref23_models.svg) | Source-reconstructed conditional effective-medium comparison | [Source comparison](../results/source_experiment_model_comparisons.csv) |
| [physics_lab_figure3_300k.svg](physics_lab_figure3_300k.svg) | Approximate plotted readings with a previous proxy choice | [Digitized data](../results/lab_figure3_digitized_approx.csv) |
| [physics_matrix_sensitivity_300k.svg](physics_matrix_sensitivity_300k.svg) | Revised two-matrix-assumption 300 K sensitivity | [Revised table](../results/manuscript_physics_300k_matrix_sensitivity.csv) |

**Reading cautions:** Source identities are provisional, the high-temperature source group is singular, and the paired development tests do not establish significant rank differences. The earlier `physics_lab_figure3_300k.svg` remains as an evidence snapshot; for revised **matrix-property sensitivity**, consult `physics_matrix_sensitivity_300k.svg`. Plot digitization error is not an apparatus uncertainty budget, and property values from another publication are not necessarily valid for these specimens.

These plots should be attributed to their **specific saved source table and commit**, not described as independently reproduced experimental measurements. See [results/README.md](../results/README.md) and [reproducibility](../docs/reproducibility.md).
