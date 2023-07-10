import numpy as np
import richdem as rd

# slope
def compute_slope(elevation_raster_file, ofile):
    dem = rd.LoadGDAL(elevation_raster_file)
    slope = rd.TerrainAttribute(dem, attrib='slope_riserun')
    rd.SaveGDAL(ofile, slope)
    return ofile

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
def compute_a_over_b(flow_accum_raster_file, ofile, area=100, width=10):
    flow_accum = rd.LoadGDAL(flow_accum_raster_file)
    a = flow_accum * area
    ab = a/width
    rd.SaveGDAL(ofile, ab)
    return ofile
