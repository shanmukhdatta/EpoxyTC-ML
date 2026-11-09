import pandas as pd
import pytest
from deepoxy.reporting import (save_csv, save_config, verify_files,
                                load_verified_predictions, export_verified_results)


def test_hash_and_zip_without_fabricated_artifacts(tmp_path):
    root = tmp_path / "results"
    p = root / "predictions.csv"
    info = save_csv(pd.DataFrame({"observed": [1., 2.], "predicted": [1., 3.]}), p)
    assert verify_files({p: info["sha256"]})["complete"]
    assert not verify_files({root / "missing.csv": None})["complete"]
    assert len(load_verified_predictions(p)) == 2
    save_config({"verified": False}, root / "status.json")
    archive = export_verified_results(root, tmp_path / "saved.zip")
    assert archive["n_files"] == 2
    assert archive["sha256"]


def test_missing_prediction_file_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_verified_predictions(tmp_path / "not_there.csv")
    with pytest.raises(ValueError, match="No actual results"):
        export_verified_results(tmp_path, tmp_path / "empty.zip")
