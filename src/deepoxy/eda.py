"""Read-only exploratory summaries (original notebook cells 13–38)."""
import numpy as np
import pandas as pd

def summarize(frame):
    return {'shape': frame.shape, 'missing': frame.isna().sum(),
            'numeric_summary': frame.describe(include=[np.number]),
            'duplicates': frame.duplicated(keep=False)}

def iqr_outliers(frame, columns):
    rows = []
    for column in columns:
        values = pd.to_numeric(frame[column], errors='coerce')
        q1, q3 = values.quantile([.25, .75]); width = q3 - q1
        mask = (values < q1 - 1.5 * width) | (values > q3 + 1.5 * width)
        rows.append({'feature': column, 'q1': q1, 'q3': q3, 'count': int(mask.sum())})
    return pd.DataFrame(rows)

def plot_distribution(frame, column, ax=None):
    import matplotlib.pyplot as plt
    if ax is None:
        _, ax = plt.subplots()
    pd.to_numeric(frame[column], errors='coerce').dropna().hist(ax=ax)
    ax.set_xlabel(column)
    return ax
