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
