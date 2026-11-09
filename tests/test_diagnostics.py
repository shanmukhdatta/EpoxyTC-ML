import numpy as np
import pandas as pd
import pytest
from deepoxy.diagnostics import residuals, prediction_residual_table, interval_coverage


def test_saved_prediction_residuals():
    frame = pd.DataFrame({"observed": [2., 4.], "predicted": [3., 3.]})
    output = prediction_residual_table(frame)
    assert output["residual"].tolist() == [-1., 1.]
    assert output["absolute_error"].tolist() == [1., 1.]


def test_empirical_interval_coverage():
    result = interval_coverage([1., 2.], [0., 0.], [1.5, 1.5])
    assert result["coverage"] == .5
    with pytest.raises(ValueError):
        interval_coverage([1], [2], [0])
