"""Held-out prediction diagnostics; permutation importance is not SHAP."""
import numpy as np
from sklearn.inspection import permutation_importance

def residuals(y_true, y_pred):
    y, p = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    if y.shape != p.shape or y.ndim != 1 or not np.isfinite(y).all() or not np.isfinite(p).all():
        raise ValueError('Expected equal-length finite vectors')
    return y-p

def heldout_permutation_importance(model, X_heldout, y_heldout, n_repeats=10, random_state=42, scoring='neg_mean_absolute_error'):
    """Caller must supply data held out from fitting and feature selection."""
    return permutation_importance(model, X_heldout, y_heldout, n_repeats=n_repeats, random_state=random_state, scoring=scoring)
