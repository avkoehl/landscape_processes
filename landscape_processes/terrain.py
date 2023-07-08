import richdem as rd

# slope
def compute_slope(elevation_raster_file):
    dem = rd.LoadGDAL(elevation_raster_file)
    slope = rd.TerrainAttribute(grid, attrib='slope_riserun')
    return slope

# flow accumulation
def compute_accumulation(elevation_raster_file):
    dem = rd.LoadGDAL(elevation_raster_file)
    rd.FillDepressions(dem, epsilon=True, in_place=True)
    flow_accum = rd.FlowAccumulation(dem, method='D8')
    return flow_accum

# a: contributing area (area of each cell that flows into a given cell)
# b: width of each cell
def compute_a_over_b(elevation_raster_file):
    flow_accum = compute_accumulation(elevation_raster_file)
    a = flow_accum * 100
    b = 10
    return a/b
