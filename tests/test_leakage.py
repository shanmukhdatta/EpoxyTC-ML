import pandas as pd
import pytest
from deepoxy.preprocessing import assert_disjoint_splits, validate_frozen_splits


def test_valid_frozen_partition():
    df = pd.DataFrame({"publication_id": ["A", "B", "C"],
                       "split": ["train", "validation", "test"]})
    assert validate_frozen_splits(df)


def test_train_eval_source_leakage_is_rejected():
    df = pd.DataFrame({"publication_id": ["A", "B", "A"],
                       "split": ["train", "validation", "test"]})
    with pytest.raises(ValueError, match="leakage"):
        assert_disjoint_splits(df)
