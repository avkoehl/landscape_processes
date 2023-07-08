import glob

import tomli

from landscape_processes.thresholds import compute_saturated_raster

# Load the config file
with open('../configs/battlecreek.toml', 'rb') as f:
    cfg = tomli.load(f)
ODIR = cfg['paths']['odir']

# raster file paths
elevation = glob.glob(ODIR + '/elevation.tif')[0]
soil = glob.glob(ODIR + '/soil.tif')[0]
precip = glob.glob(ODIR + '/precip.tif')[0]
wet_precip = glob.glob(ODIR + '/wet_precip.tif')[0]
bulk_density = glob.glob(ODIR + '/bulk_density.tif')[0]


# compute slope
slope = compute_slope(elevation)
