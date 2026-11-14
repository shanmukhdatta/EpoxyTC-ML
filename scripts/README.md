# Executable scripts: purpose and safe commands

Run commands from the **repository root** after `python -m pip install -e ".[test]"`. Scripts that generate output should write to `build/`, **not** to the curated `results/` folder.

| Script | What it checks / produces | Required inputs |
| --- | --- | --- |
| [verify_public_datasets.py](verify_public_datasets.py) | Read-only SHA-256, schema, 54/160/42 record-count and missingness checks | Bundled `data/processed/*.csv` |
| [verify_physics_results.py](verify_physics_results.py) | Replay saved effective-medium calculations and consistency checks | Bundled conditional physics CSV tables |
| [run_pipeline.py](run_pipeline.py) | Read-only original/public dataset load and descriptive EDA summaries | Public six-column or separately supplied original CSVs |
| [verify_data_integrity.py](verify_data_integrity.py) | Recompute original full-data source/feature collision and group feasibility audits | **Original full 24-column CSVs**, not bundled |
| [validate_results.py](validate_results.py) | Check caller-supplied prediction table and recompute metrics | Separate row-level predictions |
| [run_experiment.py](run_experiment.py) | Explicit grouped nested CV, or re-evaluation of supplied predictions | Authentic frozen `split` and `publication_id`, or prediction table |
| [export_results.py](export_results.py) | Archive/checksum curated saved evidence | Existing result files; select a destination outside `results/` |
| [recover_notebook_outputs.py](recover_notebook_outputs.py) | Recover displays from an explicitly provided IPYNB | Historical notebook is not bundled |

**Safe first check:**

```bash
python -m pytest -q
python scripts/verify_public_datasets.py
python scripts/verify_physics_results.py
python scripts/run_pipeline.py --data-dir data/processed --data-format processed --output-dir build/eda-audit
```

Example *optional* original-file audit (requires files not in this repository):

```bash
python scripts/verify_data_integrity.py --data-dir /path/to/full-originals --output-dir build/original-integrity
```

**Warning:** `run_experiment.py`, `validate_results.py` and `export_results.py` can have output defaults targeting the current repository. Always set `--output-dir build/...` or, for export, `--zip build/...zip`, to avoid accidentally replacing archived evidence. No script invents missing source evidence or independently validates laboratory readings.

[Reproducibility instructions](../docs/reproducibility.md) · [Results index](../results/README.md).
