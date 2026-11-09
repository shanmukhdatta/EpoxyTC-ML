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


def correlation_table(frame, columns):
    """Pairwise descriptive correlations; never infer causal mechanisms."""
    numeric = frame[list(columns)].apply(pd.to_numeric, errors="coerce")
    return numeric.corr()

def plot_scatter(frame, x, y, ax=None):
    import matplotlib.pyplot as plt
    if ax is None:
        _, ax = plt.subplots()
    ax.scatter(pd.to_numeric(frame[x], errors="coerce"),
               pd.to_numeric(frame[y], errors="coerce"), alpha=0.6)
    ax.set(xlabel=x, ylabel=y)
    return ax

def plot_missingness(frame, ax=None):
    import matplotlib.pyplot as plt
    if ax is None:
        _, ax = plt.subplots()
    frame.isna().sum().plot.bar(ax=ax)
    ax.set(ylabel="Missing row count")
    return ax
