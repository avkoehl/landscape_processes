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
          2. annual_p (30 year mean annual precipitation)
          3. wet_p (30 year mean precipitation of wettest month)
          4. soil (raster of soil transmissivity)
"""
import os
import shutil

import py3dep
from pynhd import NLDI
import pydaymet
import rioxarray

ODIR = '../data/battle_creek/'
USGS_gage = '11376550' # gage for battle creek (from wikipedia)

# ------------------ #

if os.path.exists(ODIR):
    shutil.rmtree(ODIR)

os.makedirs(ODIR)

basin = NLDI().get_basins(feature_ids = USGS_gage, fsource = "ca_gages")
geom = basin.geometry[0]

# DEM
print('download DEM')
dem = py3dep.get_map("DEM", geometry=geom, resolution=10, geo_crs=basin.crs, crs="epsg:4326")

# PRECIPIATION
# report uses PRISM data, but that is not available easily in python
print('download precipitation')
years = list(range(1992, 2022))
yearly_data = pydaymet.get_bygeom(geom, variables='prcp', dates= years, time_scale = "annual", crs=basin.crs)
yearly_mean= yearly_data.mean(dim = 'time')

monthly_data = pydaymet.get_bygeom(geom, variables='prcp', dates=years, time_scale = "monthly", crs=basin.crs)
monthly_means = monthly_data.groupby('time.month').mean(dim = 'time')
monthly_scalar_means = monthly_means.groupby('month').mean(dim = ['x','y'])
max_month = monthly_scalar_means['prcp'].argmax(dim='month')
wet_monthly_mean = monthly_means.sel(month = max_month+1) # note index (return of argmax) starts at 0 months start at 1


# SOIL
# report uses USDA NRCS data
# need spatially distributed soil transmissivity
# computed using Ksat and soil depth
# https://casoilresource.lawr.ucdavis.edu/soil-properties/download.php
print('download soil')
ksat_mean_url = 'https://soilmap2-1.lawr.ucdavis.edu/800m_grids/rasters/mean_ksat.tif'
bulk_density = 'https://soilmap2-1.lawr.ucdavis.edu/800m_grids/rasters/db.tif'
soil_depth = 'https://soilmap2-1.lawr.ucdavis.edu/800m_grids/rasters/soil_depth.tif'
# T = Ksat * soil_depth

ksat_mean = rioxarray.open_rasterio(ksat_mean_url)
ksat_mean = ksat_mean.rio.reproject_match(dem)
ksat_mean = ksat_mean.rio.clip(geometries=[geom], crs=basin.crs)

bd = rioxarray.open_rasterio(bulk_density)
bd = bd.rio.reproject_match(dem)
bd = bd.rio.clip(geometries=[geom], crs=basin.crs)

thickness = rioxarray.open_rasterio(soil_depth)
thickness = thickness.rio.reproject_match(dem)
thickness = thickness.rio.clip(geometries=[geom], crs=basin.crs)

transmissivity = ksat_mean * thickness
# need to set fill value
value = thickness.rio.nodata * ksat_mean.rio.nodata
transmissivity = transmissivity.where(transmissivity != value, thickness.rio.nodata)
transmissivity.attrs['_FillValue'] = thickness.rio.nodata

# save to disk
print(f'save to disk {ODIR}')
dem.rio.to_raster(os.path.join(ODIR, 'elevation.tif'))
yearly_mean.rio.to_raster(os.path.join(ODIR, 'annual_p.tif'))
wet_monthly_mean.rio.to_raster(os.path.join(ODIR, 'wet_p.tif'))
transmissivity.rio.to_raster(os.path.join(ODIR, 'soil.tif'))
bd.rio.to_raster(os.path.join(ODIR, 'bulk_density.tif'))

