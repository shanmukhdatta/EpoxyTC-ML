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


def evaluate_prediction_table(frame, actual="observed", predicted="predicted",
                              groups=("model", "regime")):
    """Recompute metrics from actual row-level predictions without retraining."""
    import pandas as pd
    if not {actual, predicted}.issubset(frame):
        raise ValueError("Observed and predicted columns must both exist")
    available = [c for c in groups if c in frame.columns]
    grouped = frame.groupby(available, dropna=False) if available else [((), frame)]
    records = []
    for key, part in grouped:
        keys = key if isinstance(key, tuple) else (key,)
        record = dict(zip(available, keys))
        record.update(n_rows=int(len(part)), **regression_metrics(part[actual], part[predicted]))
        records.append(record)
    return pd.DataFrame(records)

def paired_fold_comparison(table, model_a, model_b, *,
                           metric="MAE", fold_keys=("regime", "fold")):
    """Exact matched-fold comparison; does not claim independent fold significance."""
    import pandas as pd
    needed = set(fold_keys) | {"model", metric}
    if not needed.issubset(table):
        raise ValueError("Missing paired metric fields: " + str(sorted(needed - set(table))))
    if table.duplicated(list(fold_keys) + ["model"]).any():
        raise ValueError("Multiple rows for the same model and held-out fold")
    left = table.loc[table["model"] == model_a, list(fold_keys) + [metric]]
    right = table.loc[table["model"] == model_b, list(fold_keys) + [metric]]
    both = left.merge(right, on=list(fold_keys), suffixes=("_a", "_b"), validate="one_to_one")
    if len(both) != len(left) or len(both) != len(right):
        raise ValueError("Models do not have identical held-out fold identifiers")
    differences = both[metric + "_a"].to_numpy() - both[metric + "_b"].to_numpy()
    return {"n_pairs": len(differences), "mean_a_minus_b": float(np.mean(differences)),
            "exact_two_sided_p": exact_sign_flip(differences),
            "note": "Small and dependent CV folds; interpret conservatively."}

def absolute_relative_errors(y_true, y_pred):
    y = np.asarray(y_true, dtype=float)
    p = np.asarray(y_pred, dtype=float)
    regression_metrics(y, p)
    absolute = np.abs(y-p)
    return {"absolute_error": absolute,
            "relative_error_pct": np.divide(100 * absolute, np.abs(y),
                                            out=np.full(len(y), np.nan), where=y!=0)}
