import pytest
from deepoxy.models import (make_model, make_tabfm_regressor, CORE_SEARCH_SPACES)


@pytest.mark.parametrize("name", [
    "ExtraTrees", "GradientBoosting", "RandomForest",
    "SVR", "GaussianProcessRegressor", "MLP"
])
def test_classical_models_construct(name):
    model = make_model(name, seed=17)
    assert hasattr(model, "fit") and hasattr(model, "predict")


def test_core_search_spaces_present():
    assert {"ExtraTrees", "GradientBoosting", "XGBoost",
            "RandomForest", "SVR"}.issubset(CORE_SEARCH_SPACES)


def test_unrecognized_model_fails():
    with pytest.raises(ValueError, match="Unknown"):
        make_model("FakePretrainedModel")


def test_tabfm_never_loads_without_backend():
    with pytest.raises(ValueError, match="backend"):
        make_tabfm_regressor(None)
