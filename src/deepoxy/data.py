"""CSV inspection and provenance. Historical expectations are not measurements."""
from pathlib import Path
import hashlib
import pandas as pd

HISTORICAL_ROWS = {'cryogenic': 54, 'room': 160, 'high': 42}

def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()

def load_csv(path, required_columns=(), expected_rows=None):
    """Read a real CSV and return frame and audit; row-count mismatch is reported."""
    path = Path(path)
    frame = pd.read_csv(path)
    missing = sorted(set(required_columns) - set(frame.columns))
    if missing:
        raise ValueError(f'{path}: missing required columns: {missing}')
    audit = {'path': str(path), 'sha256': sha256_file(path), 'rows': len(frame),
             'columns': list(frame.columns), 'missing': frame.isna().sum().to_dict(),
             'duplicate_rows': int(frame.duplicated().sum()),
             'expected_rows': expected_rows,
             'row_count_matches': None if expected_rows is None else len(frame) == expected_rows}
    return frame, audit

def load_regimes(paths, required_columns=()):
    """Inspect caller-provided paths; never create or replace missing data."""
    return {name: load_csv(path, required_columns, HISTORICAL_ROWS.get(name))
            for name, path in paths.items()}

def source_audit(frame, source_column='publication_id', evidence_columns=()):
    if source_column not in frame:
        raise ValueError(f'Missing source column: {source_column}')
    missing_evidence = [c for c in evidence_columns if c not in frame]
    counts = frame[source_column].value_counts(dropna=False).to_dict()
    return {'source_counts': counts, 'missing_source_rows': int(frame[source_column].isna().sum()),
            'missing_evidence_columns': missing_evidence,
            'warning': 'Publication identifiers do not independently verify experimental source evidence.'}


REGIME_FILENAMES = {
    "cryogenic": "CRYOGENIC_KAGGLE_READY.csv",
    "room": "ROOM_KAGGLE_READY.csv",
    "high": "HIGH_KAGGLE_READY.csv",
}

def resolve_regime_paths(directory):
    """Locate the three *existing* raw CSV files without changing them."""
    root = Path(directory)
    paths = {regime: root / filename for regime, filename in REGIME_FILENAMES.items()}
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing original datasets: " + ", ".join(missing))
    return paths

def load_original_datasets(directory, required_columns=()):
    """Return frames and provenance metadata from caller-provided originals."""
    return load_regimes(resolve_regime_paths(directory), required_columns=required_columns)

def provenance_table(frame, source_column="publication_id", evidence_columns=()):
    """Summarize sources without implying independently authenticated references."""
    if source_column not in frame.columns:
        raise ValueError("Missing publication/source identifier: " + source_column)
    rows = []
    for source, part in frame.groupby(source_column, dropna=False):
        record = {"publication_id": str(source), "n_rows": int(len(part)),
                  "source_verification": "UNVERIFIED"}
        for col in evidence_columns:
            record[f"{col}_present_rows"] = (int(part[col].notna().sum())
                                             if col in part else 0)
        rows.append(record)
    return pd.DataFrame(rows)
