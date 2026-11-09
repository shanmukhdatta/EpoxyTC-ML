# DEEPOXY — Executed notebook results

This directory contains **15 CSV tables recovered from outputs already displayed by the executed `epoxty-checking.ipynb`**. They are here directly so you can open each result while analysing the experiments and later revising the paper.

**Important status:** Recovered historical results, **not** independently reproduced or laboratory-validated results. No model was retrained to create these files. Most CSVs are **summary tables**, not the complete original Kaggle exports. The values and Git blob identities of all 15 recovered CSVs were preserved when organizing this directory.

Original notebook: `epoxty-checking.ipynb`. Original notebook SHA-256 (recorded during recovery):
`ef371668103b26c19e9adfc5a1f59cf271dd7f5b66ba613d83faa63d9b185489`.

## A. Already executed — numerical tables recovered

| Experiment / analysis | CSV file | Saved notebook cell numbers (1-based) | What is available now |
|---|---|---|---|
| Classical five-model benchmark | [original_five_model_cv_summary.csv](original_five_model_cv_summary.csv) | 49, 51 | Mean/SD regression metrics for five models in cryogenic and room regimes |
| Expanded seven-model benchmark | [seven_model_cv_summary.csv](seven_model_cv_summary.csv) | 51 | Includes GPR and MLP alongside classical algorithms |
| Nine-model benchmark (includes TabFM/TabICLv2) | [nine_model_cv_summary.csv](nine_model_cv_summary.csv) | 69, 96 | Fold-mean MAE, RMSE, R², SD for 9 models × 2 regimes |
| Nine-model pooled OOF and bias summary | [nine_model_oof_bias_summary.csv](nine_model_oof_bias_summary.csv) | 76 | Pooled accuracy and residual summaries, **not per-observation prediction rows** |
| TabICLv2 paired comparisons | [nine_model_paired_comparisons.csv](nine_model_paired_comparisons.csv) | 69, 97 | Four paired comparisons; adjusted p-values |
| Seven-model paired statistical tests | [seven_model_pairwise_tests.csv](seven_model_pairwise_tests.csv) | 51 | Matched four-group statistical comparisons |
| Optuna hyperparameter tuning | [optuna_model_summary.csv](optuna_model_summary.csv) | 54 | Tuning performance summaries, **not individual Optuna trial records** |
| Augmentation comparison | [augmentation_ablation_summary.csv](augmentation_ablation_summary.csv) | 72, 98 | 60 model/regime/variant summaries, including no-augmentation controls |
| High-temperature exploratory models | [high_temperature_exploratory_models.csv](high_temperature_exploratory_models.csv) | 94–95 | Within-one-publication performance for 42 observations |
| Permutation feature importance | [feature_importance_summary.csv](feature_importance_summary.csv) | 82 | Held-out permutation-based importance, **not SHAP** |
| Out-of-distribution analysis | [ood_summary.csv](ood_summary.csv) | 86, 93 | Error comparisons for observations outside training feature ranges |
| Later reference-model comparison | [phase7_reference_model_summary.csv](phase7_reference_model_summary.csv) | 82 | Separate later reference experiment; **not identical to nine-model benchmark** |

### Other CSVs recorded by the notebook (bookkeeping, not new model runs)

| File | Saved notebook cell(s) | Purpose |
|---|---|---|
| [source_verification_status.csv](source_verification_status.csv) | 100 | Reports 54/160/42 original rows and source-authentication gaps |
| [external_uncertainty_availability.csv](external_uncertainty_availability.csv) | 77, 99 | Reports which uncertainty/calibration exports existed in Kaggle; it **does not contain those full exports** and one status string is truncated |
| [reviewer_status_counts.csv](reviewer_status_counts.csv) | 103 | The executed notebook's provisional counts for the 40 reviewer comments |

## B. What numerical results have we obtained so far?

- **Original data:** cryogenic **54**, room **160**, high **42** = **256 recorded rows**. Their original CSV contents have not been uploaded to this GitHub repository.
- **Four-fold nine-model development benchmarks:** lowest displayed mean MAE is **TabICLv2 = 0.06264 W/(m·K)** for cryogenic and **0.18339 W/(m·K)** for room temperature. These results use **provisional source grouping**.
- **High temperature:** TabICLv2 exploratory MAE = **0.03327 W/(m·K)** and TabFM exploratory MAE = **0.06444 W/(m·K)**, from **one publication**.
- **Augmentation:** the notebook recorded comparisons for six variants, five classical models and two development regimes. Effects are mixed: improvements are not universal, and duplicate controls can also help.
- **Paired statistical comparisons:** the four selected nine-model paired comparisons have **Holm-adjusted p = 0.5**; no significant superiority at 0.05 was established by those comparisons.
- **Physics:** 15 equation-level checks were recorded in the notebook, but no authenticated real-row physics-vs-ML comparison CSV has been recovered.

These are notebook-reported historical figures, **not final manuscript claims**.

## C. What is not completed, or still needs verification?

| Workstream | Current status | Remaining work |
|---|---|---|
| Full historical row-level OOF predictions | **NOT RECOVERED HERE** | Recover if embedded or stored elsewhere; otherwise reproduce only missing outputs |
| Complete calibration/interval prediction rows | **NOT RECOVERED HERE** | Availability/counts appear in notebook, but original complete CSV bytes are absent |
| Complete original 145 notebook PNG plots | **NOT COMMITTED HERE** | The notebook embeds them; seven summary plots were separately regenerated as SVGs |
| Original input datasets | **NOT UPLOADED** | Add the three real CSVs later and verify hashes, units, source identities and row counts |
| Train-only augmentation lineage | **PARTIAL VERIFICATION** | Check parent rows, fold separation and exact augmentation settings |
| Frozen source/material split artifacts | **PARTIAL VERIFICATION** | Verify actual group identities and reproduce exact split memberships |
| Original literature provenance | **NOT AUTHENTICATED** | Check experimental material, source type, constituent properties and filler-loading units |
| Physical-model vs measured-data comparison | **BLOCKED BY INPUT VERIFICATION** | Need physically eligible observations and verified properties/volume fractions |
| High-temperature external generalization | **NOT ESTABLISHED** | Existing 42-row experiment is within a single publication |
| Original 259-vs-256 count discrepancy | **UNRESOLVED** | Locate historical dataset versions or source records |
| Complete 40-reviewer scientific resolution | **NOT CLAIMED** | Review computational evidence separately from missing source/laboratory evidence |
| Additional outputs from the corrected *extended* notebook | **NOT VERIFIED BY THIS ARCHIVE** | Do not claim those later cells were executed simply because code exists |

## D. Plots and evidence tracking

The following are **seven new SVG visualizations of the recovered CSV data**, not a replacement for the executed notebook's original PNG figures:

[All seven regenerated result figures](../figures/README.md)

Detailed provenance and reviewer status files are stored **outside the results directory**:

- [Recovery manifest — hashes and limits](../docs/evidence/manifest.json)
- [Derived numerical snapshot](../docs/evidence/metrics_snapshot.json)
- [Reviewer-by-reviewer evidence index (40 questions)](../docs/evidence/reviewer_evidence_index.csv)

## E. How to use these for the manuscript later

Open a CSV above → verify its notebook cell and evaluation protocol → inspect the matching figure if relevant → check the reviewer evidence index → distinguish **recorded numerical evidence** from a claim that requires further computation or authenticated inputs. If full prediction rows are unavailable, never invent them from summary metrics.

**Directory rule:** `results/` contains the 15 recovered historical CSV tables and this README. Manuscript/reviewer indexes, provenance JSON, and derived metadata are kept under `docs/evidence/`.

## F. Reviewer physical-model evidence (new, separate)

The separately audited [`physics/`](physics/README.md) subdirectory contains conditional Maxwell–Eucken / Bruggeman / Hamilton–Crosser / Lewis–Nielsen / Hashin–Shtrikman results, manuscript Figure 3 approximate digitization, experimental-reference comparisons, SVG plots and verification code. The existing 15 root-level historical CSVs are unchanged. **0 of the original 256 records are fully source-authenticated**; the new physics cases must not be represented as measurements on the exact original data. Reproduce checks with `python results/physics/verify_against_src.py`.

## G. Verification-first original-data and reviewer gates

See [`verification/`](verification/README.md) for a self-contained audit script, original-CSV SHA-256 digests, all-256-row source-evidence gate, high-temperature single-source limitation, room-temperature same-input/different-target collisions and next evidence required. The underlying CSVs are not included in this Git repository, and historical experiment tables have not been altered.
