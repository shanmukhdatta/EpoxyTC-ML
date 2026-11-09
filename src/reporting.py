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


def load_verified_predictions(path, required=("observed", "predicted")):
    """Fail loudly when old Kaggle outputs are absent or incomplete."""
    import pandas as pd
    import numpy as np
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Historical prediction file missing: {path}")
    data = pd.read_csv(path)
    missing = set(required) - set(data)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    if data.empty or not np.isfinite(data[list(required)].to_numpy(dtype=float)).all():
        raise ValueError(f"{path}: empty/nonfinite prediction records")
    return data

def export_verified_results(root, destination, *, include_prefixes=None):
    """Create a checksum-verified ZIP from existing artifacts; never fabricate files."""
    import zipfile
    import hashlib
    root = Path(root).resolve()
    destination = Path(destination).resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    files = sorted(p for p in root.rglob("*") if p.is_file() and not p.is_symlink()
                   and p.resolve() != destination and p.name != ".gitkeep")
    if include_prefixes is not None:
        prefixes = tuple(include_prefixes)
        files = [p for p in files if p.relative_to(root).parts[0] in prefixes]
    if not files:
        raise ValueError("No actual results to archive")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as out:
        for path in files:
            out.write(path, path.relative_to(root).as_posix())
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None or len(archive.namelist()) != len(files):
            raise RuntimeError("Results ZIP CRC/member verification failed")
        for path in files:
            member = path.relative_to(root).as_posix()
            if hashlib.sha256(archive.read(member)).hexdigest() != sha256_file(path):
                raise RuntimeError(f"Archive hash mismatch: {member}")
    return {"path": str(destination), "n_files": len(files),
            "sha256": sha256_file(destination)}
