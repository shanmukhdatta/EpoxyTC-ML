# Software tests and recorded-evidence checks

Run from the repository root:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
python scripts/verify_public_datasets.py
python scripts/verify_physics_results.py
```

The test suite checks module imports, synthetic ML/physics routines, preprocessing and augmentation invariants, selected saved table shapes, and the **actual 26-CSV results archive**. The public-data verifier independently reads committed six-column files and checks their recorded hashes, fields, 256 total rows and missingness. The physics verifier replays conditional numeric calculations with `src/physics.py`. [GitHub Actions](../.github/workflows/README.md) runs these checks on Python 3.11/3.12.

**Limit:** Tests demonstrate software/archived-arithmetic consistency, not the original notebooks' model-training parity, authenticated material/provenance mapping, experimental apparatus uncertainty or unseen-system predictive validity. Historic source-verification CSVs no longer tracked are not silently regenerated or treated as present. For the detailed distinction, read [docs/reproducibility.md](../docs/reproducibility.md).
