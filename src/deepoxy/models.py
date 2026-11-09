"""Model factories: phase 4.1 defaults, unless a configuration is supplied."""
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.neural_network import MLPRegressor

def make_model(name, seed=42, **params):
    if name == 'ExtraTrees': model = ExtraTreesRegressor(random_state=seed, n_jobs=1)
    elif name == 'GradientBoosting': model = GradientBoostingRegressor(random_state=seed)
    elif name == 'RandomForest': model = RandomForestRegressor(random_state=seed, n_jobs=1)
    elif name == 'SVR': model = SVR()
    elif name == 'GaussianProcessRegressor': model = GaussianProcessRegressor(random_state=seed)
    elif name == 'MLP': model = MLPRegressor(random_state=seed)
    elif name == 'XGBoost':
        try: from xgboost import XGBRegressor
        except ImportError as exc: raise ImportError('XGBoost requires the optional xgboost package') from exc
        model = XGBRegressor(objective='reg:squarederror', tree_method='hist', random_state=seed, n_jobs=1, verbosity=0)
    else: raise ValueError(f'Unknown or unsupported model: {name}')
    return model.set_params(**params)

CORE_SEARCH_SPACES = {
 'ExtraTrees': {'model__n_estimators':[80,140,220], 'model__max_depth':[None,6,12], 'model__min_samples_leaf':[1,2,3]},
 'GradientBoosting': {'model__n_estimators':[70,130,210], 'model__learning_rate':[.03,.07,.12], 'model__max_depth':[2,3]},
 'XGBoost': {'model__n_estimators':[70,130,210], 'model__max_depth':[2,3,4], 'model__learning_rate':[.03,.07,.12], 'model__min_child_weight':[1,3]},
 'RandomForest': {'model__n_estimators':[80,140,220], 'model__max_depth':[None,6,12], 'model__min_samples_leaf':[1,2,3]},
 'SVR': {'model__C':[.5,2.,10.,40.], 'model__epsilon':[.02,.07,.15], 'model__gamma':['scale',.01,.1]}}


def load_tabfm_backend(model_type="regression"):
    """Explicit checkpoint load. Never invoked merely by importing the package."""
    try:
        from tabfm import tabfm_v1_0_0_pytorch
    except ImportError as exc:
        raise ImportError("Install the notebook-verified TabFM backend first") from exc
    return tabfm_v1_0_0_pytorch.load(model_type=model_type)

def make_tabfm_regressor(backend, max_num_rows=200, n_estimators=1):
    """Create the notebook's real pretrained TabFM wrapper with an explicit backend."""
    import inspect
    if backend is None:
        raise ValueError("A real, explicitly loaded pretrained TabFM backend is required")
    try:
        from tabfm import TabFMRegressor
    except ImportError as exc:
        raise ImportError("TabFM is optional; install its compatible notebook version") from exc
    signature = inspect.signature(TabFMRegressor)
    kw = {"model": backend}
    if "max_num_rows" in signature.parameters:
        kw["max_num_rows"] = max_num_rows
    if "n_estimators" in signature.parameters:
        kw["n_estimators"] = n_estimators
    return TabFMRegressor(**kw)

def make_tabicl_regressor(*, allow_auto_download=False, device="cpu",
                          checkpoint_version="tabicl-regressor-v2-20260212.ckpt",
                          seed=42, **overrides):
    """Optional TabICLv2 constructor; downloads require explicit opt-in."""
    import inspect
    try:
        from tabicl import TabICLRegressor
    except ImportError as exc:
        raise ImportError("TabICLv2 is optional; install a compatible tabicl package") from exc
    kw = {"n_estimators": 8, "batch_size": 1, "device": device,
          "random_state": seed, "checkpoint_version": checkpoint_version,
          "allow_auto_download": allow_auto_download, "verbose": False}
    kw.update(overrides)
    unknown = set(kw) - set(inspect.signature(TabICLRegressor).parameters)
    if unknown:
        raise TypeError(f"TabICL API mismatch: unsupported arguments {sorted(unknown)}")
    return TabICLRegressor(**kw)
