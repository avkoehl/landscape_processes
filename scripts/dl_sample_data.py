"""
    Download the rasters necessary for the data analysis.

    Define a study area (polygon). From online sources download the necessary
    elevation, precipitation, and soil data. Clip the data to the study area.
    Save the output to the output folder as a series of rasters.

    input:
        odir 

    output:
      A series of rasters clipped to the study area
          1. elevation (10m DEM)
          2. annual precipitation (30 year mean annual precipitation)
          3. wet precipitation (30 year mean precipitation of wettest month)
          4. soil (raster of soil transmissivity)
"""
import os
import shutil

import py3dep
from pynhd import NLDI
import pydaymet
import rioxarray
import tomli

from landscape_processes.data_functions import get_elevation_raster
from landscape_processes.data_functions import get_annual_precip_raster
from landscape_processes.data_functions import get_wet_month_precip_raster
from landscape_processes.data_functions import get_soil_transmissivity_raster
from landscape_processes.data_functions import get_soil_bulk_density_raster
from landscape_processes.raster_utils import align_rasters

# load config file
with open('../configs/battlecreek.toml', 'rb') as f:
    cfg = tomli.load(f)
ODIR = cfg['paths']['odir']
USGS_gage = cfg['study_area']['USGS_gage']

# ------------------ #

if os.path.exists(ODIR):
    shutil.rmtree(ODIR)

os.mkdir(ODIR)

basin = NLDI().get_basins(feature_ids = USGS_gage, fsource = "ca_gages")
basin = basin.to_crs('EPSG:4326')
geom = basin.geometry[0]

# get the rasters clipped to the study area
elevation = get_elevation_raster(geom)
precip = get_annual_precip_raster(geom)
wet_precip = get_wet_month_precip_raster(geom)
soil = get_soil_transmissivity_raster(geom)
bulk_density = get_soil_bulk_density_raster(geom)

# align the rasters to the elevation raster (10m)
elevation.rio.to_raster(f'{ODIR}/elevation.tif')
rasters = zip(["precip", "wet_precip", "soil", "bulk_density"], 
                       [precip, wet_precip, soil, bulk_density])

for name, raster in rasters:
    temp_file = 'temp.tif'
    raster.rio.to_raster(temp_file)
    align_rasters(temp_file, f"{ODIR}/elevation.tif", f"{ODIR}/{name}.tif")
    os.remove(temp_file)
