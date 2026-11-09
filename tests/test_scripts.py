import importlib.util
from pathlib import Path
import pandas as pd
import pytest


def test_runner_modules_compile_and_import():
    root = Path(__file__).resolve().parents[1] / "scripts"
    for name in ("run_pipeline", "run_experiment", "validate_results", "export_results"):
        path = root / f"{name}.py"
        assert path.is_file()
        compile(path.read_text(), str(path), "exec")


def test_results_validation_script_with_existing_predictions(tmp_path):
    from deepoxy.reporting import save_csv
    import subprocess
    import sys
    import os
    src = tmp_path / "pred.csv"
    save_csv(pd.DataFrame({"model": ["A", "A"], "regime": ["room", "room"],
                           "observed": [1., 2.], "predicted": [1.2, 2.2]}), src)
    root = Path(__file__).resolve().parents[1]
    cmd = [sys.executable, str(root / "scripts" / "validate_results.py"),
           "--predictions", str(src), "--output-dir", str(tmp_path / "out")]
    job = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
    assert job.returncode == 0, job.stderr
    assert (tmp_path / "out" / "validated_recomputed_metrics.csv").is_file()
