# Tests

Run **python -m pytest -q** at the repository root. Tests cover imports, synthetic model/physics routines, EDA, leakage checks, augmentation, file hashes, result-table shapes and the updated ten-row manuscript 300 K conditional model predictions.

Additionally run **python scripts/verify_public_datasets.py** and **python scripts/verify_physics_results.py**. These do **not** guarantee original experimental calibration, authenticated source-row mapping or complete pretrained-model training parity. See [reproducibility](../docs/reproducibility.md).
