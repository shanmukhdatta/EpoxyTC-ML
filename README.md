# Thermal Conductivity of Particle-Filled Epoxy: Experimental and Machine-Learning Assessment Across Three Regimes

[![Research integrity checks](https://github.com/shanmukhdatta/EpoxyTC-ML/actions/workflows/tests.yml/badge.svg)](https://github.com/shanmukhdatta/EpoxyTC-ML/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Code, curated data, numerical checks, figures, and research evidence accompanying a manuscript submitted to Elsevier's *Measurement* (manuscript ID: MEAS-D-26-20648).** This is a research artifact, **not a claim of independently replicated experiments or complete retraining of every historical model**.

**Manuscript authors (as recorded in [CITATION.cff](CITATION.cff)):** Manas Kumar, Lalit Bansal, Govinda Rao Yenni, Ravi Verma, Pradeep Kumar Awasthi, and Shanmukh Datta.  
**Maintained at:** [github.com/shanmukhdatta/EpoxyTC-ML](https://github.com/shanmukhdatta/EpoxyTC-ML)  
**Publication status:** submitted / under revision; no accepted-paper link or article DOI is asserted. Update this field only when the publisher confirms publication.

## Repository contents

| Location | What a reader will find |
| --- | --- |
| [data/processed/](data/processed/README.md) | Three downloadable public six-column CSVs; schema, record counts, and SHA-256 hashes |
| [results/](results/README.md) | **26 tracked CSV tables**: saved ML comparisons, conditional physics analyses, and data audits |
| [figures/](figures/README.md) | **10 SVG plots**, with links to their underlying results and interpretation cautions |
| [src/](src/README.md) | Python modules for data handling, EDA, model construction, grouped training, augmentation, evaluation, physics, and diagnostics |
| [scripts/](scripts/README.md) | Commands for read-only dataset checks, physics replay, EDA, and explicitly requested model runs |
| [configs/](configs/README.md) | Dataset definitions, historical experiment settings, and model parameter references |
| [tests/](tests/README.md) | Automated software, data-integrity, and saved-numerical-evidence checks |
| [docs/reproducibility.md](docs/reproducibility.md) | **Step-by-step reproduction protocol**, supported claims, and unavailable dependencies |
| [docs/evidence/](docs/evidence/README.md) | Evidence snapshot, original-input hashes, reviewer index, and outstanding provenance limitations |
| [.github/workflows/](.github/workflows/README.md) | GitHub Actions checks on Python 3.11 and 3.12 |

## Public datasets

The repository contains **256 recorded rows** across three regimes. Download each CSV directly from GitHub or clone the whole repository.

| Regime | Dataset | Rows | Recorded per-row temperature | Provisional source groups |
| --- | --- | ---: | --- | ---: |
| Cryogenic | [CRYOGENIC.csv](data/processed/CRYOGENIC.csv) | 54 | 2–120 K | 5 |
| Nominal room temperature | [ROOM.csv](data/processed/ROOM.csv) | 160 | **Missing for all 160 records** | 5 |
| Elevated temperature | [HIGH.csv](data/processed/HIGH.csv) | 42 | 308–423 K | 1 |
| **Total** | | **256** | | |

The four *candidate* input fields are `base_tc_w_mk`, `filler_tc_w_mk`, `filler_loading_as_recorded`, and `temperature_k_recorded`. The target is `composite_tc_w_mk`. The sixth column, `source_ref`, is **provisional provenance metadata and must not be used as a prediction feature**. Filler-loading units are not authenticated uniformly, and the source-reference labels are not verified observation-to-paper assignments. Do **not** silently replace the room-temperature missing values with measured temperatures.

The **original full historical 24-column CSVs, exact frozen training splits, raw laboratory measurements, original notebooks, and pretrained model checkpoints are not bundled**. These public six-column extracts support inspection and certain audits, not an exact reconstruction of the historical training runs. Details: [data dictionary and file checksums](data/processed/README.md) and [scientific limitations](docs/reproducibility.md).

## Quick start: reproducible checks without model retraining

Run from the repository root with **Python 3.10 or newer**:

```bash
git clone https://github.com/shanmukhdatta/EpoxyTC-ML.git
cd EpoxyTC-ML
python -m pip install -e ".[test]"
python -m compileall -q src scripts tests
python -m pytest -q
python scripts/verify_public_datasets.py
python scripts/verify_physics_results.py
python scripts/run_pipeline.py --data-dir data/processed --data-format processed --output-dir build/eda-audit
```

These commands check the tracked CSV schema/counts/hashes, run regression tests, replay conditional physical-model calculations, and generate **new descriptive EDA outputs in `build/eda-audit/`**. They do not retrain TabFM, TabICLv2, or the other historical ML models, and they do not download checkpoints. `build/` is ignored; do not overwrite the curated `results/` archive.

For advanced workflows (full-original data audits, independently supplied row-level predictions, or new grouped CV with authentic splits), use the documented commands in [Reproducibility](docs/reproducibility.md). Optional model dependencies are listed in [pyproject.toml](pyproject.toml).

## Where to check the reported results

- **Nine-model development comparison:** [saved MAE/RMSE/R² table](results/nine_model_cv_summary.csv), [four paired tests](results/nine_model_paired_comparisons.csv), and [cryogenic](figures/cryogenic_nine_model_mean_fold_mae.svg) / [room](figures/room_nine_model_mean_fold_mae.svg) charts. TabICLv2's smallest *recorded* mean-fold MAEs are 0.06264 and 0.18339 W/(m·K), respectively. These are historical descriptive rankings, **not statistically established superiority** (all four recorded Holm-adjusted `p = 0.50`).
- **High-temperature comparison:** [exploratory metrics](results/high_temperature_exploratory_models.csv). All 42 observations originate from **one provisional publication**, so no independent publication holdout exists.
- **Augmentation and reliability:** [ablation](results/augmentation_ablation_summary.csv), [out-of-range diagnostics](results/ood_summary.csv), [feature importance](results/feature_importance_summary.csv), and the [full result index](results/README.md).
- **Physics and manuscript checks:** [source comparison](results/source_experiment_model_comparisons.csv), [300 K matrix sensitivity](results/manuscript_physics_300k_matrix_sensitivity.csv), [corresponding plot](figures/physics_matrix_sensitivity_300k.svg), and the [read-only numerical replay](scripts/verify_physics_results.py). Approximate digitization and external constituent-property proxies are **not new laboratory measurements or independently validated specimen predictions**.
- **Data-evidence gaps:** [saved original-input audit](docs/evidence/dataset_verification_summary.json), [room feature collisions](docs/evidence/room_feature_collision_finding.md), and [40-item reviewer evidence index](docs/evidence/reviewer_evidence_index.csv).

## Reproducibility status and boundaries

| Evidence type | What this repository supports |
| --- | --- |
| Public six-column dataset integrity | **Directly checkable** using recorded SHA-256, schema, and row counts |
| Python module and script smoke tests | **Directly checkable** using `pytest` and CI |
| Public-data EDA | **Rerunnable** using committed CSVs |
| Saved conditional effective-medium arithmetic | **Numerically replayable**; source material assumptions remain conditional |
| Historical ML tables and model rankings | **Inspectable archived outputs**; exact train/split/checkpoint parity not established |
| Source-to-row authentication, original laboratory uncertainty, independent external validity | **Not established** by the repository |

No article DOI is currently available. To cite the software/data artifact, use [CITATION.cff](CITATION.cff) and record the **exact Git commit SHA** used for the analysis (`git rev-parse HEAD` after cloning). A future tagged archival release and DOI, if created, should supplement—not silently replace—the versioned commit reference.

## License and responsible use

Code is provided under the [MIT License](LICENSE). Redistribution rights to third-party source publications, laboratory records, and original external measurements are **not conferred** by the code license. Follow the limits in [docs/reproducibility.md](docs/reproducibility.md) when citing or extending these results.
