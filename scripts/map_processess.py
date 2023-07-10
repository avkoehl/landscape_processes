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
from landscape_processes.thresholds import unconditionally_stable
from landscape_processes.thresholds import unconditionally_unstable

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

T = load_raster_xr(cfg['raster_files']['transmissivity_file'])
ps = load_raster_xr(cfg['raster_files']['bulk_density_file'])
q = load_raster_xr(cfg['raster_files']['precip_file'])

# ------------------------------------------------
# compute the threshold rasters
sat = compute_saturated_raster(M, q, T)
channelized = compute_channelization_raster(sat, M, q, k=cfg['variables']['k'], 
                                            v=cfg['constants']['water_viscosity'],
                                            g=cfg['constants']['gravitational_acceleration'], 
                                            pw=cfg['constants']['water_density'], 
                                            tau=cfg['variables']['tau'])
landsliding = compute_landsliding_raster(sat, ps, pw=cfg['constants']['water_density'], M, psi=cfg['variables']['psi'])
cs = unconditionally_stable(M, psi=cfg['variables']['psi'])
cu = unconditionally_ustable(M, psi=cfg['variables']['psi'])

# ------------------------------------------------
# map where the thresholds are exceeded
