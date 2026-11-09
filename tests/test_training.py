import numpy as np
import pandas as pd
from src.training import grouped_reference_cv, core_nested_cv
from src.models import CORE_SEARCH_SPACES


def _synthetic_frozen_data():
    groups = np.repeat(list("ABCDE"), 4)
    n = len(groups)
    rng = np.random.default_rng(10)
    df = pd.DataFrame({
        "publication_id": groups,
        "split": ["train" if g in "ABC" else "validation" if g == "D" else "test" for g in groups],
        "base_tc_w_mk": rng.uniform(.1, .3, n),
        "filler_tc_w_mk": rng.uniform(5., 20., n),
        "filler_loading_as_recorded": rng.uniform(.02, .2, n),
        "temperature_k_recorded": rng.uniform(15, 100, n),
        "composite_tc_w_mk": rng.uniform(.2, .8, n),
    })
    return df


def test_fixed_reference_keeps_reserved_test_unseen():
    metrics, pred = grouped_reference_cv(_synthetic_frozen_data(), models=("ExtraTrees",))
    assert len(metrics) == 4 and len(pred) == 16
    assert set(metrics["experiment"]) == {"fixed_reference_not_notebook_tuned"}
    assert not set(pred["row_index"]).intersection({str(i) for i in range(16, 20)})


def test_nested_training_on_tiny_fixture(monkeypatch):
    monkeypatch.setitem(CORE_SEARCH_SPACES, "ExtraTrees", {
        "model__n_estimators": [4], "model__max_depth": [3]
    })
    fold, predictions, tuning = core_nested_cv(
        _synthetic_frozen_data(), model_names=("ExtraTrees",), n_search=1, n_jobs=1
    )
    assert len(fold) == 4 and len(predictions) == 16 and len(tuning) == 4
