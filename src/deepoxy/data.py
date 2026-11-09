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
