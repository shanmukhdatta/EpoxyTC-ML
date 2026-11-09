# DEEPOXY — Epoxy Thermal Conductivity ML
Modular research code for leakage-aware analysis of cryogenic, room-temperature, and elevated-temperature datasets.
Datasets, experiment results, and scientific conclusions will be added only after verification.

## Reviewer physics equation results (limited and conditional)

The existing [`src/physics.py`](src/physics.py) implements Maxwell–Eucken, Bruggeman, Hamilton–Crosser, Lewis–Nielsen, Hashin–Shtrikman bounds and Fourier-law utilities. See [`results/physics/`](results/physics/README.md) for source-reconstructed model comparisons, approximately digitized manuscript Figure 3 readings, vector plots, 158 numerical replay checks and evidence-status limitations. These are **not** validation of all 256 original CSV observations; laboratory GUM calibration inputs are not yet available.
