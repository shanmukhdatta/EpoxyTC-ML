# Thermal Conductivity of Particle-Filled Epoxy: Experimental and Machine-Learning Assessment Across Three Regimes — Figures

This folder contains **ten SVG figures directly under `figures/`**, seven generated from the recovered notebook results and two from conditional physics comparisons. There is no nested `recovered/` folder.

They are **regenerated visualizations of historical reported values**, **not the original 145 embedded PNG images**, and were created without training or rerunning ML models.

| Figure | What it shows | Underlying recovered results |
|---|---|---|
| [`cryogenic_nine_model_mean_fold_mae.svg`](cryogenic_nine_model_mean_fold_mae.svg) | Nine-model cryogenic mean MAE across four provisional publication-held-out folds | [Nine-model benchmark](../results/nine_model_cv_summary.csv) |
| [`room_nine_model_mean_fold_mae.svg`](room_nine_model_mean_fold_mae.svg) | Nine-model room-temperature mean fold MAE | [Nine-model benchmark](../results/nine_model_cv_summary.csv) |
| [`high_temperature_exploratory_mae.svg`](high_temperature_exploratory_mae.svg) | TabFM, TabICLv2 and baseline MAE for one-publication high-temperature dataset | [High-temp exploratory table](../results/high_temperature_exploratory_models.csv) |
| [`augmentation_selected_delta_mae.svg`](augmentation_selected_delta_mae.svg) | Selected MAE changes against no-augmentation controls; negative is improvement | [Augmentation table](../results/augmentation_ablation_summary.csv) |
| [`cryogenic_gradientboosting_permutation_importance.svg`](cryogenic_gradientboosting_permutation_importance.svg) | Cryogenic held-out permutation importance, measured by change in MAE | [Permutation importance table](../results/feature_importance_summary.csv) |
| [`cryogenic_ood_mae.svg`](cryogenic_ood_mae.svg) | MAE on two cryogenic outside-training-range observations | [OOD diagnostics table](../results/ood_summary.csv) |
| [`record_counts_by_regime.svg`](record_counts_by_regime.svg) | Recorded original dataset sizes: 54 cryogenic, 160 room, 42 high | [Source verification counts](../results/source_verification_status.csv) |

## Scientific interpretation

- The figures show **development/within-source metrics**, not independent external scientific validation.
- Publication and material group identifiers require authentication.
- The high-temperature comparison uses one publication; cross-publication generalization is untested.
- Augmentation comparisons are exploratory and do not establish universal benefit.
- Permutation importance is not a causal interpretation or SHAP analysis.
- The manuscript count of 259 versus the notebook's 256 original observations remains unresolved.
- Original notebook PNG figures have **not** been imported here.

See [`results/README.md`](../results/README.md) for completed computations, remaining tasks, notebook cell references and caveats. See [`docs/evidence/manifest.json`](../docs/evidence/manifest.json) for figure blob hashes and provenance.


## Two physics figures (kept directly in `figures/`)

| Figure | Description | Data |
|---|---|---|
| [`physics_ref23_models.svg`](physics_ref23_models.svg) | Published REF_23 measurements with conditional effective-medium predictions | [Source comparison](../results/source_experiment_model_comparisons.csv) |
| [`physics_lab_figure3_300k.svg`](physics_lab_figure3_300k.svg) | Approximate manuscript Figure 3 markers and proxy-property model predictions | [Digitized readings](../results/lab_figure3_digitized_approx.csv) |

Neither plot establishes experimental validation for all 256 original readings. Graph-read uncertainty is not an instrument calibration uncertainty.

## Updated paper-aligned sensitivity graph

| Figure | Underlying table |
|---|---|
| [physics_matrix_sensitivity_300k.svg](physics_matrix_sensitivity_300k.svg) | [Ten manuscript 300 K scenarios](../results/manuscript_physics_300k_matrix_sensitivity.csv) |

The earlier [physics_lab_figure3_300k.svg](physics_lab_figure3_300k.svg) remains for provenance but depicts **only an earlier low-conductivity proxy** and is superseded for the revised manuscript's balanced interpretation. No source figure is an instrument uncertainty calculation. Read the [scientific limitations](../docs/reproducibility.md).
