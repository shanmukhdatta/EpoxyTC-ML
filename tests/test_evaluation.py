import numpy as np
import pandas as pd
import pytest
from src.evaluation import (regression_metrics, exact_sign_flip,
                                paired_fold_comparison, evaluate_prediction_table,
                                absolute_relative_errors)


def test_exact_metrics_and_sign_flip():
    m = regression_metrics([1, 2, 3], [1, 2, 4])
    assert np.isclose(m["MAE"], 1/3)
    assert np.isclose(m["RMSE"], np.sqrt(1/3))
    assert np.isclose(exact_sign_flip([1, 2, 3, 4]), .125)


def test_recompute_historical_predictions():
    f = pd.DataFrame({"model": ["A", "A"], "regime": ["room", "room"],
                      "observed": [2., 4.], "predicted": [3., 3.]})
    result = evaluate_prediction_table(f)
    assert result.iloc[0]["n_rows"] == 2
    assert result.iloc[0]["MAE"] == 1
    errors = absolute_relative_errors(f.observed, f.predicted)
    assert np.isclose(errors["relative_error_pct"][0], 50)


def test_mismatched_fold_rejected():
    t = pd.DataFrame({"regime": ["room", "room"], "fold": [1, 2],
                      "model": ["A", "B"], "MAE": [1, 2]})
    with pytest.raises(ValueError, match="identical"):
        paired_fold_comparison(t, "A", "B")


def test_invalid_prediction_sizes_rejected():
    with pytest.raises(ValueError):
        regression_metrics([1., 2.], [1.])
