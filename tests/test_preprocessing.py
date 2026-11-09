import numpy as np
import pandas as pd
import pytest
from deepoxy.preprocessing import (publication_split, assert_disjoint_splits,
                                   validate_frozen_splits, grouped_folds, make_preprocessor)


def test_publication_split_has_no_group_overlap():
    df = pd.DataFrame({"publication_id": np.repeat(list("ABCDEF"), 3), "x": range(18)})
    split = publication_split(df, seed=42)
    assert validate_frozen_splits(split)
    assert assert_disjoint_splits(split) is None
    assert set(split["source_row_index"]) == set(range(18))


def test_grouped_folds_disjoint():
    X = np.arange(24).reshape(-1, 2)
    groups = np.repeat(list("ABC"), 4)
    for tr, ev in grouped_folds(X, np.arange(12), groups, 3):
        assert set(groups[tr]).isdisjoint(groups[ev])


def test_preprocessor_requires_positive_log_inputs():
    prep = make_preprocessor("log_standard")
    assert np.isfinite(prep.fit_transform([[1, 10, 2, 4], [2, 20, 3, 5]])).all()
    with pytest.raises(ValueError):
        prep.fit_transform([[-1, 10, 1, 1], [2, 20, 2, 2]])


def test_source_overlap_rejected():
    df = pd.DataFrame({"publication_id": ["A", "A", "B", "C"],
                       "split": ["train", "test", "validation", "test"]})
    with pytest.raises(ValueError, match="leakage"):
        validate_frozen_splits(df)
