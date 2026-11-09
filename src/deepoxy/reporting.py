"""Explicit output and integrity checks; never report missing artifacts as complete."""
import json
from pathlib import Path
from .data import sha256_file

def save_csv(frame, path):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return {'path': str(path), 'sha256': sha256_file(path)}

def save_config(config, path):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf8') as stream:
        json.dump(config, stream, indent=2, sort_keys=True, allow_nan=False)
    return {'path':str(path),'sha256':sha256_file(path)}

def verify_files(expected):
    """Map path to expected SHA-256; None requests existence only."""
    result = {}
    for name, expected_hash in expected.items():
        path = Path(name)
        actual = sha256_file(path) if path.is_file() else None
        result[str(path)] = {'exists':actual is not None,'sha256':actual,
                             'ok':actual is not None and (expected_hash is None or actual == expected_hash)}
    return {'complete':all(x['ok'] for x in result.values()),'files':result}
