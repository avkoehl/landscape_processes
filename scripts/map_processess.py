import glob

import tomli
import xarray

from landscape_processes.terrain import compute_a_over_b
from landscape_processes.terrain import compute_slope
from landscape_processes.terrain import compute_accumulation
from landscape_processes.thresholds import compute_saturated_raster

with open('../configs/battlecreek.toml', 'rb') as f:
    cfg = tomli.load(f)
ODIR = cfg['paths']['odir']

# ------------------------------------------------
M = compute_slope(cfg['raster_files']['elevation_file'], f"{ODIR}/slope.tif")
flow_accum = compute_accumulation(cfg['raster_files']['elevation_file'], f"{ODIR}/flow_accum.tif")
a_over_b = compute_a_over_b(flow_accum, f"{ODIR}/a_over_b.tif")

# ---------
# Thresholds
def compute_saturated_raster(slope, precip, T):
    M,q,T = [load_raster_xr(f) for f in [slope, precip, T]]
    
    with xarray.set_options(keep_attrs=True):
        sat = M*T/q

    return sat

