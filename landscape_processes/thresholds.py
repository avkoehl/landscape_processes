import numpy as np
import xarray

def compute_saturated_raster(M, q, T):
    with xarray.set_options(keep_attrs=True):
        sat = (T/q) * M
    return sat

def compute_channelization_raster(sat, M, q, k, v, g, pw, tau):
    with xarray.set_options(keep_attrs=True):
        # 2tau^3
        numerator = 2 * np.power(tau, 3) 
        # pw^3 * kvg^2 * M^2 * q
        denominator = np.power(pw,3) * k * v * np.power(g,2) * np.power(M,2) * q
    return numerator / denominator + sat

def compute_landsliding_raster(sat, ps, pw, M, psi):
    ps_over_pw = ps/pw
    middle = 1 - (np.tan(M) / np.tan(psi))
    return ps_over_pw * middle * sat

def unconditionally_stable(M, psi):
    return np.tan(M) < (0.5 * np.tan(psi))

def unconditionally_unstable(M, psi):
    return np.tan(M) > np.tan(psi)
