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
    # Select by schema alone; imputation and any dropping of empty columns are
    # fitted by the pipeline on each inner training fold.  The original cell 48
    # selected nonempty columns using all development rows before outer CV.
    # This deliberately removes that leakage and requires fresh parity checks.
    features = [c for c in FEATURES if c in development]
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


def grouped_reference_cv(frame, models=("ExtraTrees", "GradientBoosting"), *,
                         group_column="publication_id", seed=42):
    """Fixed-configuration reference folds; NOT the tuned notebook benchmark."""
    from sklearn.base import clone
    dev = frame.loc[frame["split"].isin(["train", "validation"])].copy()
    if dev.empty or dev[group_column].isna().any():
        raise ValueError("Nonempty, source-identified development rows required")
    groups = dev[group_column]
    if groups.nunique() < 3:
        raise ValueError("At least three independent development source groups required")
    cols = [col for col in FEATURES if col in dev.columns]
    X = dev[cols].apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(dev[TARGET], errors="raise")
    metric_rows, prediction_rows = [], []
    for fold, (tr, ev) in enumerate(GroupKFold(n_splits=groups.nunique()).split(X, y, groups), 1):
        for model_name in models:
            pipeline = Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", clone(make_model(model_name, seed=seed))),
            ])
            pipeline.fit(X.iloc[tr], y.iloc[tr])
            predictions = pipeline.predict(X.iloc[ev])
            metric_rows.append({"model": model_name, "fold": fold,
                                "held_out_publication": str(groups.iloc[ev].iloc[0]),
                                "experiment": "fixed_reference_not_notebook_tuned",
                                **regression_metrics(y.iloc[ev].to_numpy(), predictions)})
            prediction_rows.extend({
                "model": model_name, "fold": fold, "row_index": str(row),
                "observed": float(actual), "predicted": float(predicted),
            } for row, actual, predicted in zip(dev.index[ev], y.iloc[ev], predictions))
    return pd.DataFrame(metric_rows), pd.DataFrame(prediction_rows)
