# DEEPOXY — Verification-first continuation (dataset/source gate)

This directory is an **executed original-CSV audit** performed with `verify_data_integrity.py` on the three original `*_KAGGLE_READY.csv` files. It is **not another model-training experiment** and does not change any physical inputs, labels, sources or original records. The 256-row audit is saved under `source_authentication_gate_256.csv`.

## Reproduction

```bash
python results/verification/verify_data_integrity.py \
  --data-dir /absolute/path/to/data/raw \
  --output-dir results/verification
```

If the original CSVs are not present in GitHub `data/raw/`, supply them locally; do not replace them with synthetic examples. Input SHA-256 hashes are stored in `verification_summary.json` and `input_file_hashes.csv`. The code fails on absent files, unexpected row counts, absent critical columns, duplicated row IDs and publication-group overlap.

## Verified findings

- Cryogenic: **54 original rows, 5 provisional publications**, with measured/recorded temperature values in all rows.
- Room: **160 original rows, 5 provisional publications**; `temperature_k_recorded` is empty in all rows. Nominal 300 K is not a recorded measurement temperature.
- High: **42 original rows, 1 provisional publication**. Independent publication-held-out evaluation is not possible with one publication.
- Across all 256: `source_row_evidence`, `filler_loading_unit`, and `source_measurement_type` are empty. DOI presence is not evidence that each numeric row was read from that paper.
- Splitting code can partition the 5-group cryogenic and room regimes into 3 train source groups, 1 validation group and 1 test group. **Four** (train plus validation) independent *provisionally assigned* publication groups remain for development. Source identities must still be independently checked.
- Six room-temperature observations form **three pairs** of identical recorded 4-feature inputs but different recorded target conductivities (see `same_input_different_target_rows.csv`). One pair even spans two different provisional publication IDs. This is a demonstrable **feature insufficiency/possible provenance conflict**, *not proof that any target is wrong*.

## Concrete reviewer gates

| Reviewer concern | Code/data audit | Gate to claim completion |
|---|---|---|
| Grouped validation (R1-02, R2-02, R3-03) | Group-disjoint code path feasible for cryogenic and room | Authenticate material and publication IDs; freeze/publish split memberships and per-row OOF predictions |
| Single-source high regime (R1-07) | 1 publication, 42 rows | New genuinely independent high-temperature source required before claiming publication-held-out generalization |
| Source integrity (R1-06, R1-08, R2-03) | No row-level evidence or loading units in 256 rows | Recover originals and physical units; reconcile 259-vs-256 difference |
| Physics-vs-ML same-case benchmark (R1-05, R2-11) | Conditional 11-case physics output already saved in `results/physics/` | Need ML predictions for **those exact eligible experimental cases** with authentic inputs; do not pool unrelated benchmark scores |
| Train-only augmentation lineage (R1-01, R2-01, R3-02) | Implementation operates on training rows in `src/augmentation.py` | Persist row-level parent IDs, split IDs, and verify no child/parent crosses folds |
| Experimental uncertainty (R1-12, R2-09, R3-04) | Fourier equation and first-order independent propagation exist | Real heater-power, geometry, temperature differences, calibration and repeat records needed |
| Identical recorded inputs/different target outputs (R1-06, R2-03) | 3 two-row collision groups; 6 observations | Recover filler morphology, processing, specimen identity and exact source before interpreting ML error |

The notebook-recovered summary metrics in `results/` remain **provisional**; no rerun or full ML-result verification is claimed. The original physics comparisons and two SVG digitized plots remain at `results/physics/`.
