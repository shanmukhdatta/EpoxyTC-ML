# Reproducibility and scientific limitations

## Install and verify (no GPU, no external download)

~~~bash
python -m pip install -e ".[test]"
python -m pytest -q
python scripts/verify_public_datasets.py
python scripts/verify_physics_results.py
~~~

CI repeats these checks on Python 3.11 and 3.12. Tests validate code behavior, six-column CSV integrity, and conditional saved physical calculations. They do **not** independently reproduce the historical training notebooks, pretrained TabFM/TabICLv2 checkpoints, instrument measurements, or lab calibration.

## Reproduce published-data inspection

~~~bash
python scripts/run_pipeline.py --data-dir data/processed --data-format processed --output-dir build/eda-audit
~~~

All saved EDA summaries go to **build/** (ignored), not curated results/. The original full-file historical audit requires separately supplied 24-column inputs:

~~~bash
python scripts/run_pipeline.py --data-dir /path/to/full-originals --data-format original --output-dir build/original-audit
python scripts/verify_data_integrity.py --data-dir /path/to/full-originals --output-dir build/source-audit
~~~

Original-file hashes and the 256-row evidence gate are in [dataset_verification_summary.json](evidence/dataset_verification_summary.json) and [results/](../results/README.md). The SHA256 values in the public-data README refer to **six-column exports**, not to original 24-column CSVs.

## Model experiments: honest reproducibility boundary

[run_experiment.py](../scripts/run_experiment.py) deliberately demands frozen split and publication_id metadata for grouped training. Six-column public CSVs **do not supply** those fields, so the script will refuse to claim original five-group/4-development-fold parity. Authentic frozen splits, row-level predictions, full Optuna trials, dependency versions and external pretrained checkpoints are required for complete reruns. Source-ref is historical metadata, not an input to the regressors. Provisional labels permit exploratory split checks only; high temperature (one source) cannot support independent publication-held-out tests.

The 28 older result CSVs were retained, not retrained. A new [10-row 300 K matrix-sensitivity table](../results/manuscript_physics_300k_matrix_sensitivity.csv) follows the revised manuscript: using a low 0.200 W/(m·K) proxy vs 1.064 W/(m·K) epoxy from a **different published study** produces very different Maxwell curves. This is **conditional input sensitivity, not 1.43% validated experimental accuracy**. [Figure](../figures/physics_matrix_sensitivity_300k.svg). Manuscript Figure 3 graph readings are approximate and their reading tolerance is not instrument uncertainty.

## Missing primary evidence

Fully authenticated paper/DOI-to-row matching, filler-loading units, actual room temperatures, raw specimen heat-flow measurements, apparatus uncertainty budget, independent sample replicates, and equivalence between matrix batches remain unresolved. A successful CI badge cannot close these scientific gaps. See [reviewer index](evidence/reviewer_evidence_index.csv) and [evidence directory](evidence/README.md).

Main paper title: **Thermal Conductivity of Particle-Filled Epoxy: Experimental and Machine-Learning Assessment Across Three Regimes**. Submission: Elsevier *Measurement*, MEAS-D-26-20648; official paper link/DOI not yet verified.
