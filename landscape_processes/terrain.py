import numpy as np
import richdem as rd
import xarray as xr
from xrspatial import slope

def compute_slope_rd(elevation_raster_file, ofile):
    dem = rd.LoadGDAL(elevation_raster_file)
    nan = np.isnan(dem)
    rd.FillDepressions(dem, epsilon=True, in_place=True)
    slope = rd.TerrainAttribute(dem, attrib='slope_degrees')
    slope[nan] = np.nan
    rd.SaveGDAL(ofile, slope)
    return ofile

def compute_slope_xr(dem):
    slope = slope(dem)
    return slope

# flow accumulation
def compute_accumulation(elevation_raster_file, ofile):
    dem = rd.LoadGDAL(elevation_raster_file)
    nan = np.isnan(dem)
    rd.FillDepressions(dem, epsilon=True, in_place=True)
    flow_accum = rd.FlowAccumulation(dem, method='D8')
    flow_accum[nan] = np.nan
    rd.SaveGDAL(ofile, flow_accum)
    return ofile

# a: contributing area (area of each cell that flows into a given cell)
# b: width of each cell
def compute_a_over_b(flow_accum):
    # pixel width in meters
    pw = abs(flow_accum[0])
    # pixel hieght in meters
    ph = abs(flow_accum[1])

    area = pw*ph
    a = flow_accum * area
    b = pw

    with xarray.set_options(keep_attrs=True):
        ab = a/b
    return ab
