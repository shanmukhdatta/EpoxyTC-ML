# DEEPOXY — Epoxy Thermal Conductivity ML

Evidence-first research code for cryogenic, room-temperature and elevated-temperature thermal-conductivity modeling.

- [`src/`](src/README.md) — implemented ML and physics equations, including [`src/physics.py`](src/physics.py).
- [`results/`](results/README.md) — **flat directory of 28 CSV tables plus one README**, with no nested physics/verification folders.
- [`figures/`](figures/README.md) — the original summary figures and two qualified physics comparison SVGs.
- [`scripts/`](scripts/) — model runners and reproducibility checks, including `verify_physics_results.py` and `verify_data_integrity.py`.
- [`docs/evidence/`](docs/evidence/) — source notes, conditional paper draft, reviewer index and laboratory input template.

Run `python -m pytest -q` and `python scripts/verify_physics_results.py` to check the repository. To audit original data, use `python scripts/verify_data_integrity.py --data-dir /path/to/original/CSVs --output-dir /path/to/new/audit`.

**Evidence limits:** The 256 original rows do not yet have authenticated specimen provenance/volume-fraction evidence. The physics calculations use conditional source reconstructions or property proxies. The laboratory uncertainty budget requires original instrument data. The high-temperature dataset has one provisional publication; no cross-publication generalization has been established. The original raw CSVs are off-repository and unchanged.
