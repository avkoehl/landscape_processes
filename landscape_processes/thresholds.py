import numpy as np
import xarray

def compute_saturated_raster(M, q, T):
    with xarray.set_options(keep_attrs=True):
        sat = (T/q) * M
    return sat

def compute_channelization_raster(sat, M, q, constants={}, variables={}):
    # unpack constants
    v = constants['water_viscosity']
    g = constants['gravitational_acceleration']
    pw = constants['water_density']

    # unpack variables
    k = variables['k']
    tau = variables['tau']

    with xarray.set_options(keep_attrs=True):
        # 2tau^3
        numerator = 2 * np.power(tau, 3) 
        # pw^3 * kvg^2 * M^2 * q
        denominator = np.power(pw,3) * k * v * np.power(g,2) * np.power(M,2) * q
    return numerator / denominator + sat

def compute_landsliding_raster(sat, M, ps, constants={},  variables={}):
    # unpack constants
    pw = constants['water_density']

    # unpack variables
    psi = variables['psi']

    ps_over_pw = ps/pw
    middle = 1 - (np.tan(M) / np.tan(psi))
    return ps_over_pw * middle * sat

def unconditionally_stable(M, psi):
    return np.tan(M) < (0.5 * np.tan(psi))

def unconditionally_unstable(M, psi):
    return np.tan(M) > np.tan(psi)
