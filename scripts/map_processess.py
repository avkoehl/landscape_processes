import glob

import tomli
import xarray

from landscape_processes.raster_utils import load_raster_xr
from landscape_processes.terrain import dervied_terrain_rasters
from landscape_processes.thresholds import compute_saturated_raster
from landscape_processes.thresholds import compute_channelization_raster
from landscape_processes.thresholds import compute_landsliding_raster
from landscape_processes.thresholds import unconditionally_stable
from landscape_processes.thresholds import unconditionally_unstable

with open('../configs/battlecreek.toml', 'rb') as f:
    cfg = tomli.load(f)
ODIR = cfg['paths']['odir']

# ------------------------------------------------
# Load the input rasters
dem = load_raster_xr(cfg['raster_files']['elevation_file'])
T = load_raster_xr(cfg['raster_files']['transmissivity_file'])
ps = load_raster_xr(cfg['raster_files']['bulk_density_file'])
p = load_raster_xr(cfg['raster_files']['precip_file'])

# ------------------------------------------------
# compute derived rasters
theta, M, flow_accum, a_over_b = dervied_terrain_rasters(dem)
q = p # placeholder until loss factor raster exits

# ------------------------------------------------
# compute the threshold rasters
sat = compute_saturated_raster(M, q, T)
channelized = compute_channelization_raster(sat, M, q, cfg['constants'], cfg['variables'])
landsliding = compute_landsliding_raster(sat, M, ps, cfg['constants'], cfg['variables']
cs = unconditionally_stable(M, psi=cfg['variables']['psi'])
cu = unconditionally_unstable(M, psi=cfg['variables']['psi'])

# ------------------------------------------------
# map where the thresholds are exceeded

# saturated
sat_b = (a_over_b > sat)
sat_inds = np.where(sat_b)

# channelized
channel_b = (a_over_b > channelized)
channel_inds = np.where(channel_b)

# landsliding
ls_b = (a_over_b > landsliding)
ls_inds = np.where(ls_b)

# process codes:
# {0: 'soil creep',
#  1: 'sheet wash ',
#  2: 'gullying',
#  3: 'landsliding dry',
#  4: 'landsliding wet'}

processes = -1 * np.ones_like(a_over_b)
processes[np.where(a_over_b < sat)] = 0

processes[sat_inds] = 1

processes[channel_inds] = 2

#processes[ls_inds] = 3

test = pd.Series(processes.flatten())
test.value_counts()
