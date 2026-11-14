# Dataset index

The only committed datasets are the **three six-column exports** in [processed/](processed/README.md). The original full historical 24-column research inputs are **not** in this public repository; these exports are not substitutes for original specimen/source documentation.

| Regime | Direct download | Original rows | Recorded temperature | Provisional source groups |
| --- | --- | ---: | --- | ---: |
| Cryogenic | [CRYOGENIC.csv](processed/CRYOGENIC.csv) | 54 | 2–120 K | 5 |
| Nominal room | [ROOM.csv](processed/ROOM.csv) | 160 | Missing in all rows | 5 |
| High | [HIGH.csv](processed/HIGH.csv) | 42 | 308–423 K | 1 |

**Total: 256 rows.** The exports have four candidate input fields, one target, and `source_ref` (non-feature, provisional provenance); see the [column dictionary and three SHA-256 checksums](processed/README.md).

From repository root, check the exact public files with:

```bash
python scripts/verify_public_datasets.py
```

The original-file hashes and reported missing evidence are saved in [dataset verification](../docs/evidence/dataset_verification_summary.json), with the original-input checksum table in [results/input_file_hashes.csv](../results/input_file_hashes.csv). These are **previous audit records**, not a claim of freshly regenerated original-file evidence. Row-level source identity and filler-loading units are not independently authenticated. One source for the high-temperature records precludes a publication-held-out evaluation in that regime. [Full reproducibility guide](../docs/reproducibility.md).
