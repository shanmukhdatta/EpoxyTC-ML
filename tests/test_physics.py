import numpy as np
import pytest
from src.physics import (maxwell_eucken, bruggeman_symmetric, hashin_shtrikman,
                            hamilton_crosser, lewis_nielsen, fourier_conductivity,
                            fourier_independent_uncertainty)


def test_effective_medium_endpoints():
    km, kf = .2, 20.
    assert maxwell_eucken(km, kf, 0) == pytest.approx(km)
    assert bruggeman_symmetric(km, kf, 1) == pytest.approx(kf)
    lo, hi = hashin_shtrikman(km, kf, .25)
    assert lo <= hi
    assert hamilton_crosser(km, kf, 0, .9) == pytest.approx(km)
    assert lewis_nielsen(km, kf, 0, 1.5, .6) == pytest.approx(km)


def test_uncertainty_needs_supplied_inputs():
    assert fourier_conductivity(2, .01, .01, 2) == pytest.approx(1)
    result = fourier_independent_uncertainty(2, .1, .01, .001, .01, .001, 2, .1)
    assert result["combined_standard_uncertainty_w_mk"] > 0
    with pytest.raises(ValueError):
        fourier_conductivity(2, .01, 0, 2)


def test_invalid_fillers_rejected():
    with pytest.raises(ValueError):
        hashin_shtrikman(.2, 10, 1.2)
