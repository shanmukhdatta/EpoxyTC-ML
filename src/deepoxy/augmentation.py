"""Notebook cells 69 and 71: operate only on caller-supplied training rows."""
import numpy as np
import pandas as pd

FEATURES_CANDIDATE = ["base_tc_w_mk", "filler_tc_w_mk", "filler_loading_as_recorded", "temperature_k_recorded"]
FEATURES = FEATURES_CANDIDATE

def augment_train_only(X_train, y_train, noise_fraction, seed, copies=2):
    """Create two train-only copies, perturbing strictly positive conductivity inputs.

    Loading, measured temperature, and targets are never changed. The synthetic labels
    are an assumption-based sensitivity test, NOT new independent measurements.
    """
    assert noise_fraction is not None and 0 <= noise_fraction <= 0.03
    assert X_train.columns.tolist()[:2] == FEATURES_CANDIDATE[:2]

    original_x = X_train.to_numpy(dtype=float, copy=True)
    original_y = np.asarray(y_train, dtype=float).copy()
    assert np.isfinite(original_x).all() and np.isfinite(original_y).all()
    assert (original_x[:, :2] > 0).all(), "Conductivity perturbation requires positive k."

    rng = np.random.default_rng(seed)
    blocks = [original_x]
    for _ in range(copies):
        new = original_x.copy()
        if noise_fraction > 0:
            # Same random draws and seed for 1% and 3%, changing only amplitude.
            deviation = rng.normal(0, noise_fraction, size=(len(new), 2))
            deviation = np.clip(deviation, -0.15, 0.15)
            new[:, :2] *= (1.0 + deviation)
        assert np.isfinite(new).all() and (new[:, :2] > 0).all()
        assert np.array_equal(new[:, 2:], original_x[:, 2:])
        blocks.append(new)

    aug_x = np.vstack(blocks)
    aug_y = np.tile(original_y, copies + 1)
    assert len(aug_x) == len(aug_y) == (copies + 1) * len(X_train)
    assert np.array_equal(aug_x[:len(X_train)], original_x)
    assert np.array_equal(aug_y[:len(X_train)], original_y)
    return pd.DataFrame(aug_x, columns=X_train.columns), aug_y

def find_compatible_pairs(frame, regime):

    pairs = []

    for i in range(len(frame)):
        for j in range(i + 1, len(frame)):

            a = frame.iloc[i]
            b = frame.iloc[j]

            if a["publication_id"] != b["publication_id"]:
                continue

            constituent_match = all(
                np.isclose(
                    float(a[col]),
                    float(b[col]),
                    rtol=1e-9,
                    atol=1e-12
                )
                for col in FEATURES[:2]
            )

            if not constituent_match:
                continue

            if regime == "cryogenic":

                difference = abs(
                    float(a["temperature_k_recorded"])
                    - float(b["temperature_k_recorded"])
                )

                if difference > 5.0:
                    continue

            if np.isclose(
                float(a["filler_loading_as_recorded"]),
                float(b["filler_loading_as_recorded"])
            ):
                continue

            pairs.append((i, j))

    return np.asarray(pairs, dtype=int).reshape(-1, 2)

def make_cmix_training_data(X, y, pairs, seed):

    rng = np.random.default_rng(seed)

    x = X.to_numpy(dtype=float)
    y = np.asarray(y, dtype=float)

    assert len(pairs) > 0

    # C-Mixup-inspired label-similarity weighting.
    differences = np.abs(
        y[pairs[:, 0]] - y[pairs[:, 1]]
    )

    positive = differences[differences > 0]

    bandwidth = (
        float(np.median(positive))
        if len(positive)
        else max(float(np.std(y)), 1e-6)
    )

    bandwidth = max(bandwidth, 1e-6)

    log_weights = -0.5 * (
        differences / bandwidth
    ) ** 2

    weights = np.exp(
        log_weights - log_weights.max()
    )

    weights = weights / weights.sum()

    # Two synthetic observations per candidate pair.
    n_synthetic = 2 * len(pairs)

    chosen = pairs[
        rng.choice(
            len(pairs),
            size=n_synthetic,
            replace=True,
            p=weights
        )
    ]

    i = chosen[:, 0]
    j = chosen[:, 1]

    lam = rng.beta(
        2.0, 2.0,
        size=n_synthetic
    )

    mixed_x = (
        lam[:, None] * x[i]
        + (1 - lam[:, None]) * x[j]
    )

    mixed_y = (
        lam * y[i]
        + (1 - lam) * y[j]
    )

    # Pair-matched duplication control.
    choose_first = rng.integers(
        0, 2,
        size=n_synthetic
    ).astype(bool)

    endpoints = np.where(
        choose_first, i, j
    )

    duplicate_x = x[endpoints]
    duplicate_y = y[endpoints]

    assert np.isfinite(mixed_x).all()
    assert np.isfinite(mixed_y).all()
    assert (mixed_x[:, :2] > 0).all()

    variants = {
        "constrained_cmix": (
            pd.DataFrame(
                np.vstack([x, mixed_x]),
                columns=X.columns
            ),
            np.concatenate([y, mixed_y])
        ),

        "matched_pair_duplicate": (
            pd.DataFrame(
                np.vstack([x, duplicate_x]),
                columns=X.columns
            ),
            np.concatenate([y, duplicate_y])
        )
    }

    return variants
