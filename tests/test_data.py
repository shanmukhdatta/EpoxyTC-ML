import pandas as pd
import pytest
from deepoxy.data import load_csv, load_original_datasets, provenance_table, sha256_file


def test_csv_preserved_and_hashed(tmp_path):
    source = tmp_path / "rows.csv"
    pd.DataFrame({"publication_id": ["a", "b"], "k": [1.0, 2.0]}).to_csv(source, index=False)
    frame, audit = load_csv(source, required_columns=["k"], expected_rows=2)
    assert len(frame) == 2 and audit["row_count_matches"] is True
    assert audit["sha256"] == sha256_file(source)
    assert provenance_table(frame).shape[0] == 2


def test_missing_originals_rejected(tmp_path):
    with pytest.raises(FileNotFoundError, match="Missing original datasets"):
        load_original_datasets(tmp_path)


def test_missing_columns_rejected(tmp_path):
    p = tmp_path / "only.csv"
    pd.DataFrame({"a": [1]}).to_csv(p, index=False)
    with pytest.raises(ValueError, match="missing required columns"):
        load_csv(p, required_columns=["not_present"])
