# Source-code modules and scope

The Python scientific modules intentionally live directly under `src/` rather than a nested `deepoxy/` package. The installed distribution is `epoxy-thermal-conductivity-ml`; imports use **`src`**.

| Module | Responsibility | Important boundary |
| --- | --- | --- |
| [data.py](data.py) | Input loading, hashes, row and source diagnostics | Historical full inputs require explicit user supply |
| [eda.py](eda.py) | Descriptive summaries, missingness, outlier and diagnostic plots | EDA does not alter original files |
| [preprocessing.py](preprocessing.py) | Group-based split checks and fold-specific preprocessing | Source IDs and frozen-split parity need external authentication |
| [models.py](models.py) | Classical regressor factories and optional TabFM/TabICLv2 constructors | Checkpoints and optional packages are not bundled |
| [training.py](training.py) | Grouped nested CV and tuning implementations | Not the complete original Optuna/TabFM notebook orchestration |
| [augmentation.py](augmentation.py) | Training-only perturbation, duplication and mixing utilities | Physical label assumptions and parent-row lineage need independent assessment |
| [evaluation.py](evaluation.py) | MAE/RMSE/R² and paired-comparison utilities | Four development groups provide weak statistical power |
| [physics.py](physics.py) | Effective-medium equations, Fourier estimate and independent-uncertainty utilities | Correct arithmetic cannot authenticate constituent-property inputs |
| [diagnostics.py](diagnostics.py) | Residual, feature-importance and interval diagnostics | Attribution and calibration validation are limited |
| [reporting.py](reporting.py) | Read/write/checksums of real saved artifacts | Missing historical outputs are not synthesized |
| [__init__.py](__init__.py) | Import-package marker | No training runs on import |

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

Example imports:

```python
from src.data import load_public_datasets
from src.evaluation import regression_metrics
from src.training import core_nested_cv
```

The [public processed data](../data/processed/README.md) use a **provisional** `source_ref` metadata field. Historical full-data model reruns require authentic `publication_id` and frozen `split` assignments; these are not recoverable from the public extracts alone. Saved outputs are indexed in [results/](../results/README.md) (**14 historical ML summary CSVs**, plus ten physics and two integrity CSVs). There are [seven historical ML figures and three physics figures](../figures/README.md). See [script entry points](../scripts/README.md) and [reproduction boundaries](../docs/reproducibility.md).
