# Script navigation

| Entry point | Purpose |
|---|---|
| [verify_public_datasets.py](verify_public_datasets.py) | Validate tracked six-column CSV schemas, SHA-256, 256 rows, source labels and missing temperatures |
| [verify_data_integrity.py](verify_data_integrity.py) | Audit separately supplied full 24-column **originals** |
| [verify_physics_results.py](verify_physics_results.py) | Replay conditional saved physical-model arithmetic |
| [run_pipeline.py](run_pipeline.py) | Nontraining EDA; supports --data-format processed and original |
| [run_experiment.py](run_experiment.py) | Explicit grouped tuning; requires real frozen split and publication_id; or reuse original predictions |
| [validate_results.py](validate_results.py) | Metrics recomputation from actual supplied predictions |
| [export_results.py](export_results.py) | Curated artifact checksums/export |
| [recover_notebook_outputs.py](recover_notebook_outputs.py) | Extract available outputs from a caller-supplied notebook |

Quickstart: **python scripts/verify_public_datasets.py**, **python scripts/verify_physics_results.py**, **python -m pytest -q**. Never write generated results over the curated [results/](../results/README.md); choose **build/**. For original CSV audits, read [the reproducibility guide](../docs/reproducibility.md).
