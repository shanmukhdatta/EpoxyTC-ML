# DEEPOXY physical-model reviewer verification (conditional)

This directory contains **actual executed physical-model results** and **approximate graph-digitization data** from the DEEPOXY reviewer response. These files are intentionally **separate** from the 15 recovered historical notebook CSVs in the parent `results/` directory.

## Data and outputs

- `core_results.csv`: 11 source-reconstructed model-comparison cases, including 2 published 80/298 K negative-thermal-expansion-filler/epoxy observations. **7 ROO-prefixed cases are unverified candidate original-row linkages**; do not report them as authenticated original CSV matches.
- `lab_digitized_core.csv`: 30 readings from manuscript Figure 3, page 6. `±0.04 W/(m·K)` describes estimated **graph-reading precision**, never actual specimen measurement uncertainty.
- `source_experiment_model_comparisons.csv`: complete 11-case evidence-and-model table (original V6 export).
- `lab_figure3_digitized_approx.csv`: full plot-coordinate provenance from prior graph-digitization execution.
- `lab_fig3_maxwell_inverse_checks.csv`, `lab_fig3_forward_model_scenarios.csv`, `lab_fig3_geometry_sensitivity.csv`, `lab_fig3_group_plausibility.csv`: conditional physical-plausibility checks; **not** experimental validation.
- `physical_property_source_register.csv`: material-property source URLs and evidence labels.
- `manuscript_tables_2_4_6_recalculated_errors.csv`: 16 mathematical prediction-error comparisons (some benchmarks are analytical, not experimental).
- `physics_reviewer_comment_coverage.csv`: 17 physics-related reviewer items, including unresolved laboratory evidence.
- `raw_lab_measurement_template.csv`: deliberately empty instrument inputs, **not a numerical GUM result**.
- `figures/ref23_models.svg` and `figures/lab_figure3_300k.svg`: vector plots of the conditional comparison and the 300 K digitized data.
- `results_summary.json`, `PAPER_READY.md`: decision status and qualified manuscript insertion.
- `verify_against_src.py`: tests saved numbers against the existing `src.physics` implementation.

## Reproduce verified arithmetic

From repository root, with dependencies from `requirements.txt` installed:

```bash
python results/physics/verify_against_src.py
```

The script checks the existing (not rewritten) `src/physics.py` equations, all eleven source comparison records, output error arithmetic, 30 graph data rows and reviewer-evidence labels.

## What is and is not proven

**Completed:** equation-level numerical reconstruction for the limited source experiments; explicit scientific evidence labels; graph-based sensitivity/plausibility screening.

**Not completed:** experimental authentication of the original 256 rows (currently 0/256); precise laboratory GUM budget; original un-digitalized laboratory readings; experimental ML-vs-physics comparison on exactly identical raw specimens. None of these limitations is hidden by a mathematical PASS status.
