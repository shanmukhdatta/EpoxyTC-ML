# Six-column manuscript training tables

These three tracked files retain exactly four candidate inputs, one target, and one source-reference tag. They preserve numeric values and row order from the uploaded full original CSVs without changing raw research files.

| Column | Role | Notes |
|---|---|---|
| base_tc_w_mk | Input | Matrix conductivity, W/(m·K) |
| filler_tc_w_mk | Input | Filler conductivity, W/(m·K) |
| filler_loading_as_recorded | Input | Unit is **not** verified uniformly wt% or vol% |
| temperature_k_recorded | Input if available | Kelvin; blank in all 160 room rows |
| composite_tc_w_mk | Target | Composite conductivity, W/(m·K) |
| source_ref | **Not an input** | Provisional historical paper number, e.g. [23] |

| File | Rows | SHA-256 |
|---|---:|---|
| [CRYOGENIC.csv](CRYOGENIC.csv) | 54 | 29e84afc8e8d9e63bda07b668c423686fa31df3ffc53c02292d2bd76152f680d |
| [ROOM.csv](ROOM.csv) | 160 | 2143d2b4cc8aa71c7361a4394d0f5f685438a3384481a0a0ed394d12eadfc422 |
| [HIGH.csv](HIGH.csv) | 42 | be3da1d568c441a42c8b580fa577a07b5c44d613799f5f56e2621e286d8933b6 |

Run **python scripts/verify_public_datasets.py** from the repository root. The recorded [19]–[29] IDs are **legacy source-reference labels from the original compilation** and might not equal the final manuscript's renumbered citation numbers. Source-to-observation extraction evidence is incomplete; high has one source; room has 160 unknown actual temperatures. Three distinct room feature-vector groups contain conflicting recorded target values and were **not** removed or averaged; see [audit](../../docs/evidence/room_feature_collision_finding.md).

The six-column files alone do not reproduce historic frozen publication IDs, Optuna trials or raw laboratory uncertainty. To intentionally change an input file, first authenticate it and update the integrity checksum and all relevant evidence. Return to [data navigation](../README.md).
