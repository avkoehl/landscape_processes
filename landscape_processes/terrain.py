import os

import numpy as np
import richdem as rd
import xarray 
from xrspatial import slope

from landscape_processes.raster_utils import load_raster_xr

def compute_slope_xr(dem):
    slope = slope(dem)
    return slope

def compute_accumulation(elevation):
    # save to temp file
    temp_file = 'temp.tif'
    elevation.rio.to_raster(temp_file)

    # load dem with rd
    dem = rd.LoadGDAL(temp_file)
    nan = np.isnan(dem)
    rd.FillDepressions(dem, epsilon=True, in_place=True)
    flow_accum = rd.FlowAccumulation(dem, method='D8')
    flow_accum[nan] = np.nan
    os.remove(temp_file)

    # convert to xarray
    rd.SaveGDAL(temp_file, flow_accum)
    flow_accum = load_raster_rx(temp_file)
    os.remove(temp_file)
    return flow_accum

# a: contributing area (area of each cell that flows into a given cell)
# b: width of each cell
def compute_a_over_b(flow_accum):
    # pixel width in meters
    pw = abs(flow_accum.rio.resolution()[0])
    # pixel hieght in meters
    ph = abs(flow_accum.rio.resolution()[1])

    area = pw*ph
    a = flow_accum * area
    b = pw

    with xarray.set_options(keep_attrs=True):
        ab = a/b
    return ab

def derived_terrain_rasters(elevation):
    theta = compute_slope_xr(elevation)
    M = np.sine(theta)
    flow_accum = compute_accumulation(elevation)
    a_over_b = compute_a_over_b(flow_accum)

    return theta, M, flow_accum, a_over_b
