"""Metrics and exact paired sign-flip tests; inputs must be observed predictions."""
from itertools import product
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def regression_metrics(y_true, y_pred):
    y = np.asarray(y_true, dtype=float); p = np.asarray(y_pred, dtype=float)
    if y.ndim != 1 or y.shape != p.shape or not len(y) or not np.isfinite(y).all() or not np.isfinite(p).all():
        raise ValueError('Expected nonempty, finite and equally sized vectors')
    return {'MAE': mean_absolute_error(y,p), 'RMSE': float(np.sqrt(mean_squared_error(y,p))),
            'R2': r2_score(y,p) if len(y)>=2 and not np.isclose(np.var(y),0) else np.nan}

def exact_sign_flip(differences):
    d = np.asarray(differences, dtype=float)
    if d.ndim != 1 or not len(d) or len(d)>20 or not np.isfinite(d).all():
        raise ValueError('Provide 1–20 finite paired differences')
    observed = abs(np.mean(d))
    extreme = sum(abs(np.mean(d*np.asarray(s))) >= observed-1e-12 for s in product((-1,1), repeat=len(d)))
    return extreme / (2 ** len(d))
