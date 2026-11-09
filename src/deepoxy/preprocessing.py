"""Publication-held-out splitting and train-only preprocessing."""
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer

FEATURES = ['base_tc_w_mk', 'filler_tc_w_mk', 'filler_loading_as_recorded', 'temperature_k_recorded']
TARGET = 'composite_tc_w_mk'

def assert_disjoint_splits(frame, group='publication_id', split='split'):
    if frame[group].isna().any():
        raise ValueError('Missing group identifiers')
    if set(frame[split].unique()) != {'train', 'validation', 'test'}:
        raise ValueError('Expected nonempty train, validation and test splits')
    groups = [set(frame.loc[frame[split] == name, group]) for name in ('train','validation','test')]
    if any(groups[i] & groups[j] for i in range(3) for j in range(i)):
        raise ValueError('Group leakage between partitions')

def publication_split(frame, seed=42, group='publication_id'):
    """Original cell 45 split; fewer than three groups remain unassigned."""
    data = frame.copy().reset_index(drop=True)
    if group not in data or data[group].isna().any():
        raise ValueError('A nonmissing publication identifier is required for every row')
    data['source_row_index'] = np.arange(len(data))
    n = data[group].nunique()
    data['split'] = 'unassigned'
    if n < 3:
        return data
    outer = GroupShuffleSplit(n_splits=1, test_size=1/n, random_state=seed)
    development, test = next(outer.split(data, groups=data[group]))
    inner = GroupShuffleSplit(n_splits=1, test_size=1/(n-1), random_state=seed+1)
    train, validation = next(inner.split(data.iloc[development], groups=data.iloc[development][group]))
    data.loc[development[train], 'split'] = 'train'
    data.loc[development[validation], 'split'] = 'validation'
    data.loc[test, 'split'] = 'test'
    assert_disjoint_splits(data, group)
    return data

def log_conductivity_features(X):
    X = np.asarray(X, dtype=float).copy()
    for index in (0, 1):
        if np.any(X[:, index] <= 0):
            raise ValueError('Conductivity must be positive for log10')
        X[:, index] = np.log10(X[:, index])
    return X

def make_preprocessor(kind='standard'):
    steps = [('imputer', SimpleImputer(strategy='median'))]
    if kind == 'log_standard':
        steps.append(('log', FunctionTransformer(log_conductivity_features, validate=False)))
    if kind in ('standard', 'log_standard'):
        steps.append(('scaler', StandardScaler()))
    elif kind != 'raw':
        raise ValueError(f'Unknown preprocessing kind: {kind}')
    return Pipeline(steps)

def grouped_folds(X, y, groups, n_splits):
    groups = np.asarray(groups)
    if pd.isna(groups).any():
        raise ValueError('Missing group identifiers')
    for train, test in GroupKFold(n_splits=n_splits).split(X, y, groups):
        if set(groups[train]) & set(groups[test]):
            raise ValueError('Group leakage')
        yield train, test
