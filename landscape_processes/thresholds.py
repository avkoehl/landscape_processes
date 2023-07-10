import math
import numpy as np

def compute_saturated_raster(M, q, T):
    with xarray.set_options(keep_attrs=True):
        sat = (T/q) * M
    return sat

def compute_channelization_raster(M, q, T, k, v, g, pw, tau):
    sat = compute_saturated_raster(M, q, T)
    
    with xarray.set_options(keep_attrs=True):
        # 2tau^3
        numerator = 2 * np.power(tau, 3) 

        # pw^3 * kvg^2 * M^2 * q
        denominator = np.power(pw,3) * k * v * np.power(g,2) * np.power(M,2) * q

    return numerator / denominator + sat

def compute_landsliding_raster(M, q, T, k, v, g, pw, tau):
    sat = compute_saturated_raster(slope, precip, T)

    ps_over_pw = pb/pw
    middle = 1 - (math.tan(M) / math.tan(psi))
    return ps_over_pw * middle * sat

def unconditionally_stable(M, psi):
    return math.tan(M) > math.tan(psi)

def unconditionally_unstable(M, psi):
    return math.tan(M) < (0.5 * math.tan(psi))