import math
import numpy as np

def compute_saturated_raster(slope, precipitation, transmissivity):
    return slope * (transmissivity / precipitation)

"""
def compute_channelization_raster(slope, precipitation, transmissivity, k, v, g, pw, tau):
   saturated = compute_saturated_raster(slope, precipitation, transmissivity)

   numerator = 2 * np.power(transmissivity, 3)
   denominator = np.power(pw, 3) * k * v * np.power(g, 2) * np.power(slope, 2) * precipitation

   channelization = numerator / denominator + saturated
   return channelization

def compute_landsliding_raster(slope, precipitation, transmissivity, bulk_density, pw, psi, tau):
   saturated = compute_saturated_raster(slope, precipitation, transmissivity)
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
"""
