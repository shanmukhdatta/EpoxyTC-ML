# Reproducibility protocol and scientific scope

This document distinguishes **(1) present public files and executable checks**, **(2) historical recorded experiment outputs**, and **(3) scientific evidence that is not yet publicly available or authenticated**. All commands assume the repository root as the current working directory.

## 1. Software environment and executable checks

Use Python **3.10+**, with CI exercising **3.11 and 3.12**. Installation is local; no GPU, TabFM/TabICLv2 checkpoints, or external model downloads are required for the commands below.

```bash
git clone https://github.com/shanmukhdatta/EpoxyTC-ML.git
cd EpoxyTC-ML
python -m pip install -e ".[test]"
python -m compileall -q src scripts tests
python -m pytest -q
python scripts/verify_public_datasets.py
python scripts/verify_physics_results.py
```

The first verification script checks recorded hashes, counts (54/160/42), schema, provisional labels and missing temperatures of [three tracked CSVs](../data/processed/README.md). The second numerically replays **conditional** physical-model entries from [results/](../results/README.md), rather than validating an instrument against calibrated specimen readings. CI runs the corresponding checks via [tests.yml](../.github/workflows/tests.yml).

Tests and CI **do not independently establish** notebook-equivalent training runs, paper-to-record provenance, raw calorimetry/heat-flow measurements, material composition or experimental error bars.

## 2. Recreate a nontraining public-data EDA audit

```bash
python scripts/run_pipeline.py --data-dir data/processed --data-format processed --output-dir build/eda-audit
```

This uses exactly the public six-column tables and writes summaries plus `dataset_audit.json` to `build/eda-audit/`. It does not modify committed datasets or train regressors. The room temperature feature is missing for all 160 room observations; any imputation/nominal-temperature assumption must be explicitly described in downstream experiments, not presented as a measured value.

## 3. Audit the original full research CSVs (not bundled)

If the original 24-column data are lawfully available **from their actual holder**, place these exact filenames in a local directory:

- `CRYOGENIC_KAGGLE_READY.csv` (54 rows)
- `ROOM_KAGGLE_READY.csv` (160 rows)
- `HIGH_KAGGLE_READY.csv` (42 rows)

Run:

```bash
python scripts/run_pipeline.py --data-dir /path/to/full-originals --data-format original --output-dir build/original-eda
python scripts/verify_data_integrity.py --data-dir /path/to/full-originals --output-dir build/original-integrity
```

Use the [saved original-input SHA-256 list](evidence/dataset_verification_summary.json) to distinguish inputs, and compare the [saved input hash table](../results/input_file_hashes.csv). This command re-generates certain audit CSVs **only if the originals are supplied**; their missing source-evidence fields do not become authenticated by passing code checks. The archived 256-row per-record gate CSV is not currently distributed.

## 4. Recompute metrics from independent row-level predictions (optional)

The archived [26 result CSVs](../results/README.md) contain **aggregated historical metrics**, not sufficient original predictions for exact metric replay. If valid per-observation predictions are supplied separately, the following script validates the expected prediction schema and recomputes metric tables:

```bash
python scripts/validate_results.py --predictions /path/to/predictions.csv --output-dir build/prediction-validation
```

A successful schema/numerical check is not proof that the supplied predictions came from the historical notebooks or an untouched test set.

## 5. Run **new** grouped ML training (optional; not historical parity)

`scripts/run_experiment.py` requires a supplied table with **authentic** `publication_id` group labels and frozen `split` assignments, in addition to the predictor/target fields. The public six-column files **do not satisfy this requirement**. With such verified inputs and the package environment, a new experiment can be requested explicitly:

```bash
python scripts/run_experiment.py --data /path/to/authenticated_frozen_training_table.csv --models ExtraTrees --n-search 8 --output-dir build/new-cv
```

Do not interpret a completed new CV run as numerical replication of the historical results without additional evidence: frozen partition membership, row-level source identity, preprocessing configuration, trial histories, package/environment versions, random seeds, and external pretrained-model checkpoint integrity would have to match. Optional XGBoost/Optuna dependencies are available as `pip install -e ".[optional-models]"`; TabFM and TabICLv2 require separately validated installation/checkpoints. **No automatic checkpoint download is performed.**

## 6. What the archived results establish (and do not)

| Artifact | Recheck possible from this repository? | Boundary |
| --- | --- | --- |
| Public six-column CSV integrity | Yes: hashes, columns, counts | This does not authenticate originating publications |
| Public-data EDA summaries | Yes | Missing nominal-room temperature remains missing |
| Conditional Maxwell/Bruggeman/etc. calculations | Yes: arithmetic replay | Inputs may be proxy properties or approximate plot readings |
| Saved nine-model, augmentation, Optuna and reliability tables | Inspectable | Exact source notebooks and splits/checkpoints are not bundled |
| Original grouped holdout methodology | Code paths inspectable | Original split identity and row-level publication assignments not verified |
| Elevated-temperature independent publication holdout | No | Only one provisional source |
| Laboratory uncertainty/independent specimen replication | No | Raw observations, calibration and uncertainty inputs are unavailable |

Saved four-fold model comparisons have Holm-adjusted `p = 0.50` in the four recorded paired tests. These comparisons support **descriptive numerical differences**, not proven superiority. The 300 K revised [matrix-input sensitivity](../results/manuscript_physics_300k_matrix_sensitivity.csv) changes when cross-study epoxy conductivity is substituted; that exercise is **not** demonstrated 1.43% accuracy for the manuscript specimens. The 30 manuscript Figure 3 data points were read approximately from a graph and their reading tolerance is not a GUM laboratory uncertainty.

## 7. Scientific provenance, versioning, and citation

The saved [dataset verification summary](evidence/dataset_verification_summary.json) reports 256 original rows, provisional source groups (5/5/1), missing room recorded temperatures (160), and absent row-level source/loading-unit authentication. The [room collision report](evidence/room_feature_collision_finding.md) documents three identical-four-feature/different-target pairs. Historical notes mentioning **259 rows** should not be treated as evidence for three additional data records; **256** is the count of the available original-input audit and public dataset.

The paper associated with this repository has been **submitted to *Measurement*** (MEAS-D-26-20648); acceptance, DOI and publisher-hosted publication are not asserted. For reproducible referencing, cite [CITATION.cff](../CITATION.cff) plus the specific Git SHA (`git rev-parse HEAD`). Treat the MIT [software license](../LICENSE) separately from third-party data rights. See [reviewer evidence index](evidence/reviewer_evidence_index.csv).
