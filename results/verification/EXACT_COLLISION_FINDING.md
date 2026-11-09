# Identical model inputs, different conductivity readings — detected, not corrected

Three collisions in the original **room-temperature** CSV have the same recorded four-feature vector `(base_tc_w_mk, filler_tc_w_mk, filler_loading_as_recorded, temperature_k_recorded)`, but report different `composite_tc_w_mk`. The temperature field is blank throughout this regime.

| Row pair | Provisional source(s) | Same base/filler TC (W/mK) | Same recorded filler-loading number | Recorded composite TC values (W/mK) |
|---|---|---|---|---|
| `ROO_048` / `ROO_101` | REF_25 / REF_27 | 0.2 / 3000 | 0.58 | 0.38 / 0.85 |
| `ROO_060` / `ROO_125` | REF_25 / REF_25 | 0.2 / 3000 | 1.16 | 0.45 / 1.27 |
| `ROO_087` / `ROO_090` | REF_27 / REF_27 | 0.6 / 401 | 1.00 | 0.69 / 0.71 |

**Scientific implication:** a deterministic function of the four recorded features must return one prediction for two equal input vectors. It therefore cannot fit both distinct recorded targets exactly, absent additional predictors or a corrected source mapping. Measurement uncertainty, morphology, processing, experimental direction and source errors are possible explanations but **none is established here**. Do not delete these rows or average their measurements without authenticated sample records.

All values above were read directly from the original user-supplied room CSV and reproduced by `verify_data_integrity.py`. The original file hash appears in `input_file_hashes.csv`.
