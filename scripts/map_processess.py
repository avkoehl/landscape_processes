import glob

import tomli
import xarray

from landscape_processes.raster_utils import load_raster_xr
from landscape_processes.terrain import compute_a_over_b
from landscape_processes.terrain import compute_slope
from landscape_processes.terrain import compute_accumulation
from landscape_processes.thresholds import compute_saturated_raster
from landscape_processes.thresholds import compute_channelization_raster
from landscape_processes.thresholds import compute_landsliding_raster
from landscape_processes.thresholds import conditionally_stable
from landscape_processes.thresholds import conditionally_unstable

with open('../configs/battlecreek.toml', 'rb') as f:
    cfg = tomli.load(f)
ODIR = cfg['paths']['odir']

# ------------------------------------------------
M = compute_slope(cfg['raster_files']['elevation_file'], f"{ODIR}/slope.tif")
flow_accum = compute_accumulation(cfg['raster_files']['elevation_file'], f"{ODIR}/flow_accum.tif")
a_over_b = compute_a_over_b(flow_accum, f"{ODIR}/a_over_b.tif")

# ------------------------------------------------
# Load the rasters
M = load_raster_xr(f"{ODIR}/slope.tif")
a_over_b = load_raster_xr(f"{ODIR}/a_over_b.tif")

dem = load_raster_xr(cfg['raster_files']['elevation_file'])
T = load_raster_xr(cfg['raster_files']['transmissivity_file'])
ps = load_raster_xr(cfg['raster_files']['bulk_density_file'])
q = load_raster_xr(cfg['raster_files']['precip_file'])

# ------------------------------------------------
# compute the thresholds
saturated = compute_saturated_raster(M, q, T)
def compute_channelization_raster(M, q, T, k, v, g, pw, tau):
channelized = compute_channelization_raster(M, a_over_b, saturated)
landsliding = compute_landsliding_raster(M, ps, saturated)
