# Public research data

The only tracked dataset folder is [processed/](processed/README.md), containing the three verified **six-column** CSVs (54 cryogenic + 160 nominal-room + 42 high = 256 original records). They are cleaned *copies*; the 24-column originals have not been altered.

| Regime | CSV | Rows | Actual temperatures | Source groups |
|---|---|---:|---|---:|
| Cryogenic | [CRYOGENIC.csv](processed/CRYOGENIC.csv) | 54 | 2–120 K recorded | 5 provisional |
| Nominal room | [ROOM.csv](processed/ROOM.csv) | 160 | Not recorded per row | 5 provisional |
| High | [HIGH.csv](processed/HIGH.csv) | 42 | 308–423 K recorded | 1 provisional |

See [schema, hashes, and missing-evidence caveats](processed/README.md); [source verification](../results/source_authentication_gate_256.csv); and [reproducibility](../docs/reproducibility.md). Original full inputs are not published here, and no source-ref number alone proves authenticated specimen identity.
