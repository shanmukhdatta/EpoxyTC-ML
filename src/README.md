# DEEPOXY — Source code

The scientific Python modules live **directly in `src/`** (there is no nested `deepoxy/` folder). The installed Python distribution is named `deepoxy`, but the import package for this repository layout is **`src`**.

## What each module contains

| Module | Contents | Status / important limitation |
|---|---|---|
| [`data.py`](data.py) | Original CSV paths; SHA-256 checksums; dataset loading and row counts; source and provenance summaries | Real CSVs must be supplied by the user; source authenticity is not automatically verified |
| [`eda.py`](eda.py) | Descriptive statistics, missing values, IQR outliers, correlations, distributions, scatter and missingness plots | EDA operates without changing raw data |
| [`preprocessing.py`](preprocessing.py) | Publication-held-out splits, fold checks, imputation, scaling and log features | Real paper/material identifiers and historical split parity require audit |
| [`models.py`](models.py) | ExtraTrees, GradientBoosting, RandomForest, SVR, GPR, MLP, XGBoost factories; optional TabFM and TabICLv2 constructors | TabFM/TabICLv2 require separately verified optional dependencies and checkpoints; constructors alone are not full experiments |
| [`training.py`](training.py) | Grouped nested CV with randomized hyperparameter search; fixed-configuration reference CV | Does **not** implement every original notebook experiment, full Optuna pipeline or complete pretrained-model evaluation |
| [`augmentation.py`](augmentation.py) | Training-only Gaussian perturbations, duplication control, constrained same-source pairing and C-Mixup | Synthetic labels and physical assumptions remain experimental; fold/parent-row lineage requires further verification |
| [`evaluation.py`](evaluation.py) | MAE, RMSE, R², existing-prediction metric recovery and paired exact sign-flip tests | Four-source comparisons have low statistical power |
| [`physics.py`](physics.py) | Maxwell–Eucken, Bruggeman, Hashin–Shtrikman, Hamilton–Crosser, Lewis–Nielsen, Fourier-law estimate and basic independent uncertainty | Authentic inputs, units and source evidence needed before physics-versus-ML claims |
| [`diagnostics.py`](diagnostics.py) | Residual tables, held-out permutation importance and empirical interval coverage | Permutation importance is **not SHAP**; full OOD/calibration experimental orchestration still needs integration |
| [`reporting.py`](reporting.py) | Save/read and validate CSVs; SHA-256 verification; archive real results without fabricating missing files | Some historical Kaggle artifacts are unavailable |
| [`__init__.py`](__init__.py) | Makes `src` an importable Python package | Scientific numerical equivalence to all notebook cells has not been established |

## Installation and imports

Run at repository root:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

Then Python code imports modules as:

```python
from src.data import load_original_datasets
from src.evaluation import regression_metrics
from src.training import core_nested_cv
```

### Command-line scripts

See [`scripts/`](../scripts/): `run_pipeline.py` audits CSV inputs and EDA; `run_experiment.py` reuses predictions or explicitly runs grouped tuning; `validate_results.py` validates saved predictions; `export_results.py` builds a checksum-checked archive; `recover_notebook_outputs.py` extracts saved IPYNB displays.

**No experiment is trained on import.** Pretrained model downloads are not automatically triggered. Full reviewer-grade parity and independent data validation remain separate scientific tasks.

## Related repository directories

- [`results/`](../results/README.md): 15 notebook-recovered historical CSV results and a completed/incomplete evidence guide
- [`figures/`](../figures/README.md): seven charts regenerated from recovered CSV values
- [`docs/evidence/`](../docs/evidence/): provenance manifest, metrics snapshot and reviewer index
- [`tests/`](../tests/): lightweight synthetic checks, not a claim of full research reproduction
