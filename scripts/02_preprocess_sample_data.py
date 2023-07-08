import glob

import rasterio

from utils import snap_to

ODIR = "../data/battle_creek/"

# Snap all rasters to DEM
rasters = glob.glob(ODIR + "*.tif")
# remove elevation.tif from rasters list
rasters.remove(ODIR + "elevation.tif")
dem = ODIR + "elevation.tif"

ofiles = []
ofiles.append(dem)
for raster in rasters:
    base = raster.split("/")[-1].split(".")[0]
    ofile = f"{ODIR}{base}_snapped.tif"
    snap_to(raster, dem, ofile)
    ofiles.append(ofile)

# load snapped rasters as bands of a single raster
with rasterio.open(ofiles[0]) as src:
    meta = src.meta

meta.update(count=len(ofiles))

with rasterio.open(ODIR + "combined.tif", "w", **meta) as dst:
    names = []
    for i, layer in enumerate(ofiles, start=1):
        base = layer.split("/")[-1].split(".")[0]
        names.append(base)
        with rasterio.open(layer) as src1:
            dst.write_band(i, src1.read(1))
    dst.descriptions = names



# On DEM
# 1. Fill sinks
# 2. Add streams

# On precipitation rasters, convert to mm/day
