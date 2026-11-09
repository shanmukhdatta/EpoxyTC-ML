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


def prediction_residual_table(frame, actual="observed", predicted="predicted"):
    """Make inspectable row-level residuals without fitting a model."""
    import pandas as pd
    if actual not in frame or predicted not in frame:
        raise ValueError("Prediction table requires observed and predicted columns")
    result = frame.copy()
    result["residual"] = residuals(result[actual], result[predicted])
    result["absolute_error"] = np.abs(result["residual"])
    return result

def interval_coverage(y_true, lower, upper):
    """Empirical held-out interval coverage; no distribution-free claim implied."""
    y, lo, hi = map(lambda v: np.asarray(v, dtype=float), (y_true, lower, upper))
    if not len(y) or y.ndim != 1 or y.shape != lo.shape or y.shape != hi.shape:
        raise ValueError("Expected matching nonempty interval vectors")
    if not np.isfinite(np.concatenate([y, lo, hi])).all() or np.any(lo > hi):
        raise ValueError("Invalid interval boundaries")
    return {"n": int(len(y)), "coverage": float(np.mean((y >= lo) & (y <= hi))),
            "mean_width": float(np.mean(hi-lo))}
