"""Original notebook cell 73 effective-medium formulae; caller supplies verified inputs."""
import numpy as np
from scipy.optimize import brentq

def valid_inputs(km, kf, phi):
    vals = np.asarray([km, kf, phi], dtype=float)
    if not np.isfinite(vals).all() or km <= 0 or kf <= 0 or not 0 <= phi <= 1:
        raise ValueError('Conductivities must be positive and volume fraction in [0, 1].')

def maxwell_eucken(km, kf, phi):
    valid_inputs(km, kf, phi)
    delta = kf-km
    return km*(kf+2*km+2*phi*delta)/(kf+2*km-phi*delta)

def bruggeman_symmetric(km, kf, phi):
    valid_inputs(km, kf, phi)
    if phi == 0: return float(km)
    if phi == 1: return float(kf)
    if km == kf: return float(km)
    def balance(k):
        return (1-phi)*(km-k)/(km+2*k) + phi*(kf-k)/(kf+2*k)
    return float(brentq(balance, min(km,kf), max(km,kf), xtol=1e-13))

def hashin_shtrikman(km, kf, phi):
    valid_inputs(km, kf, phi)
    if km == kf: return float(km),float(km)
    kl,kh = min(km,kf),max(km,kf)
    fl = (1-phi) if km == kl else phi
    fh = 1-fl
    lower = kl + fh / (1/(kh-kl) + fl/(3*kl))
    upper = kh + fl / (1/(kl-kh) + fh/(3*kh))
    return float(lower),float(upper)

def hamilton_crosser(km, kf, phi, sphericity):
    valid_inputs(km, kf, phi)
    if not np.isfinite(sphericity) or not 0 < sphericity <= 1:
        raise ValueError('Verified particle sphericity must be in (0,1].')
    n = 3/sphericity
    delta = kf-km
    return float(km*(kf+(n-1)*km+(n-1)*phi*delta)/
                 (kf+(n-1)*km-phi*delta))

def lewis_nielsen(km, kf, phi, A, phi_max):
    valid_inputs(km, kf, phi)
    if not (np.isfinite(A) and A > 0 and np.isfinite(phi_max) and 0 < phi_max <= 1):
        raise ValueError('Verified A>0 and 0<maximum packing<=1 required.')
    if phi > phi_max + 1e-12:
        raise ValueError('Filler volume fraction exceeds documented packing limit.')
    B = (kf/km-1)/(kf/km+A)
    psi = 1 + (1-phi_max)/(phi_max**2)*phi
    den = 1-B*psi*phi
    if den <= 0: raise ValueError('Lewis–Nielsen denominator nonpositive.')
    return float(km*(1+A*B*phi)/den)
