"""Phase 4.1 grouped nested CV; final test groups remain untouched."""
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from .models import make_model, CORE_SEARCH_SPACES
from .preprocessing import FEATURES, TARGET, assert_disjoint_splits
from .evaluation import regression_metrics

def core_nested_cv(data, model_names=('ExtraTrees','GradientBoosting','XGBoost','RandomForest','SVR'), seed=42, n_search=8, n_jobs=-1):
    """Return fold metrics, predictions, tuning records; no final test fitting."""
    assert_disjoint_splits(data)
    development = data.loc[data['split'].isin(['train','validation'])].copy()
    features = [c for c in FEATURES if c in development and development[c].notna().any()]
    X = development[features].apply(pd.to_numeric, errors='coerce')
    y = pd.to_numeric(development[TARGET], errors='coerce')
    groups = development['publication_id']
    if len(features)==0 or groups.nunique()<4 or not np.isfinite(y).all():
        raise ValueError('At least four development publications, valid target and features required')
    metrics, predictions, tuning = [], [], []
    for fold,(tr,ev) in enumerate(GroupKFold(n_splits=groups.nunique()).split(X,y,groups),1):
        for name in model_names:
            pipe = Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler()),('model',make_model(name,seed))])
            search = RandomizedSearchCV(pipe, CORE_SEARCH_SPACES[name], n_iter=n_search, scoring='neg_mean_absolute_error',
                     cv=GroupKFold(n_splits=min(3,groups.iloc[tr].nunique())), random_state=seed,n_jobs=n_jobs,refit=True,error_score='raise')
            search.fit(X.iloc[tr],y.iloc[tr],groups=groups.iloc[tr])
            pred = search.predict(X.iloc[ev]); held = str(groups.iloc[ev].iloc[0])
            metrics.append({'model':name,'fold':fold,'n_train':len(tr),'n_eval':len(ev),'held_out_publication':held,
                            'augmentation':'none','status':'EXPLORATORY_UNVERIFIED_GROUPS',**regression_metrics(y.iloc[ev],pred)})
            predictions.extend({'model':name,'fold':fold,'row_index':idx,'observed':truth,'predicted':p} for idx,truth,p in zip(X.iloc[ev].index,y.iloc[ev],pred))
            tuning.append({'model':name,'fold':fold,'best_params':search.best_params_,'best_inner_mae':-search.best_score_})
    return pd.DataFrame(metrics),pd.DataFrame(predictions),pd.DataFrame(tuning)
