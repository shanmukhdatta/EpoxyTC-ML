import matplotlib
matplotlib.use("Agg")
import pandas as pd
from deepoxy.eda import summarize, iqr_outliers, correlation_table, plot_distribution, plot_scatter


def test_eda_is_non_destructive():
    f = pd.DataFrame({"a": [1., 2., 3.], "b": [2., 3., 5.]})
    original = f.copy(deep=True)
    assert summarize(f)["shape"] == (3, 2)
    assert iqr_outliers(f, ["a"]).iloc[0]["count"] == 0
    assert correlation_table(f, ["a", "b"]).shape == (2, 2)
    assert plot_distribution(f, "a") is not None
    assert plot_scatter(f, "a", "b") is not None
    pd.testing.assert_frame_equal(f, original)
