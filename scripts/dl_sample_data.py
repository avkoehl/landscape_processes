"""
    Download the rasters necessary for the data analysis.

    Define a study area (polygon). From online sources download the necessary
    elevation, precipitation, and soil data. Clip the data to the study area.
    Save the output to the output folder as a series of rasters.

    input:
        USGS gage
        odir 

    output:
      A series of rasters clipped to the study area
          1. elevation (10m DEM)
          2. annual precipitation (30 year mean annual precipitation)
          3. wet precipitation (30 year mean precipitation of wettest month)
          4. soil (raster of soil transmissivity)
          5. particle bulk density 
"""
import os
import shutil

import py3dep
from pynhd import NLDI
import pydaymet
import rioxarray

from landscape_processes.data_functions import get_elevation_raster
from landscape_processes.data_functions import get_annual_precip_raster
from landscape_processes.data_functions import get_wet_month_precip_raster
from landscape_processes.data_functions import get_soil_transmissivity_raster
from landscape_processes.data_functions import get_soil_bulk_density_raster

USGS_Gage = '11376550'
ODIR = '../data/battlecreek/'

# ------------------ #

print(f"prepping {ODIR}")
if os.path.exists(ODIR):
    print("\tremoving existing data folder")
    shutil.rmtree(ODIR)

print("\tmaking new data folder")
os.mkdir(ODIR)

basin = NLDI().get_basins(feature_ids = USGS_Gage, fsource = "ca_gages")
basin = basin.to_crs('EPSG:4326')
geom = basin.geometry[0]

# get the rasters clipped to the study area
print("getting Data")
elevation = get_elevation_raster(geom)
precip = get_annual_precip_raster(geom)
wet_precip = get_wet_month_precip_raster(geom)
soil = get_soil_transmissivity_raster(geom)
bulk_density = get_soil_bulk_density_raster(geom)

# align the rasters to the elevation raster (10m)
elevation.rio.to_raster(f'{ODIR}/elevation.tif')
rasters = zip(["precip", "wet_precip", "soil", "bulk_density"], 
                       [precip, wet_precip, soil, bulk_density])

print("Saving Data")
for name, raster in rasters:
    print(f"\tsaving {ODIR}/{name}")
    raster = raster.rio.reproject_match(elevation)
    raster.rio.to_raster(f"{ODIR}/{name}.tif")
