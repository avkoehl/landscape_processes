import math
import numpy

def compute_saturated_raster(slope, precipitation, tau):
""" a/b > tau/q * M
"""
    tau_over_q = tau / precipitation
    saturated = slope * tau_over_q
    return saturated

def compute_channelization_raster(slope, precipitation, transmissivity, k, v, g, pw, tau):
"""
"""
   saturated = compute_saturated_raster(slope, precipitation, tau)

   numerator = 2 * np.power(transmissivity, 3)
   denominator = np.power(pw, 3) * k * v * np.power(g, 2) * np.power(slope, 2) * precipitation

   channelization = numerator / denominator + saturated
   return channelization

def compute_landsliding_raster(slope, precipitation, transmissivity, bulk_density, pw, psi, tau=0.5):
"""
"""
   saturated = compute_saturated_raster(slope, precipitation, tau)
   ps_over_pw = ps / pw
   middle = 1 - math.tan(slope) / math.tan(psi)

   landsliding = ps_over_pw * middle * saturated
   return landsliding


def compute_stability(theta, psi):
    if math.tan(theta) < (0.5 * math.tan(psi)):
        return True
    elif math.tan(theta) > math.tan(psi):
        return False
    else:
        ValueError("tan(psi) >= tan(theta) >= 0.5tan(psi)")
