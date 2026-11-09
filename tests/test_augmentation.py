import numpy as np
import pandas as pd
from src.augmentation import (augment_train_only, duplicate_training_rows,
                                   find_compatible_pairs, make_cmix_training_data)


def _train():
    return pd.DataFrame({"base_tc_w_mk": [.2, .2, .3],
                         "filler_tc_w_mk": [15., 15., 20.],
                         "filler_loading_as_recorded": [.1, .2, .3],
                         "temperature_k_recorded": [12., 13., 15.]})


def test_gaussian_changes_only_train_conductivity_columns():
    X = _train()
    y = np.array([.3, .4, .5])
    augmented, labels = augment_train_only(X, y, .01, 123)
    assert len(augmented) == len(labels) == 9
    assert np.array_equal(augmented.iloc[:3].to_numpy(), X.to_numpy())
    assert np.array_equal(augmented.iloc[3:, 2:].to_numpy(),
                          np.tile(X.iloc[:, 2:].to_numpy(), (2, 1)))
    assert len(X) == 3


def test_duplicate_control_has_no_new_labels():
    X = _train()
    duplicates, labels = duplicate_training_rows(X, [1., 2., 3.], copies=1)
    assert len(duplicates) == 6 and labels.tolist() == [1., 2., 3., 1., 2., 3.]


def test_cmix_uses_eligible_source_pairs_only():
    frame = _train()
    frame["publication_id"] = ["A", "A", "B"]
    pairs = find_compatible_pairs(frame, "cryogenic")
    assert pairs.tolist() == [[0, 1]]
    variants = make_cmix_training_data(frame[_train().columns], np.array([.3, .4, .5]), pairs, 21)
    assert set(variants) == {"constrained_cmix", "matched_pair_duplicate"}
    for values, labels in variants.values():
        assert len(values) == len(labels) == 5
