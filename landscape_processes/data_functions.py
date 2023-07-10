import os
import shutil

import py3dep
import pydaymet
import rioxarray
import xarray

def get_elevation_raster(geom, crs="epsg:4326"):
    dem = py3dep.get_map("DEM", geom, resolution=10, crs=crs)
    return dem

def get_annual_precip_raster(geom, crs="epsg:4326"):
    years = list(range(1992, 2022))
    yearly_data = pydaymet.get_bygeom(geom, variables='prcp', dates= years, time_scale = "annual", crs=crs)
    actual_crs = yearly_data.rio.crs

    with xarray.set_options(keep_attrs=True):
        yearly_mean = yearly_data.mean(dim = 'time')
        yearly_mean = yearly_mean['prcp']
        yearly_mean = yearly_mean / 365 # days per year
        yearly_mean = yearly_mean / 1000 # (convert from mm to m)
        yearly_mean.attrs['units'] = 'm'
        yearly_mean.rio.write_crs(actual_crs, inplace=True)
        yearly_mean = yearly_mean.rio.reproject(crs)
    return yearly_mean

def get_wet_month_precip_raster(geom, crs="epsg:4326"):
    years = list(range(1992, 2022))
    monthly_data = pydaymet.get_bygeom(geom, variables='prcp', dates=years, time_scale = "monthly", crs=crs)
    actual_crs = monthly_data.rio.crs

    with xarray.set_options(keep_attrs=True):
        monthly_means = monthly_data.groupby('time.month').mean(dim = 'time')
        monthly_scalar_means = monthly_means.groupby('month').mean(dim = ['x','y'])
        max_month = monthly_scalar_means['prcp'].argmax(dim='month')
        wet_monthly_mean = monthly_means.sel(month = max_month+1) # note index (return of argmax) starts at 0 months start at 1
        wet_monthly_mean = wet_monthly_mean['prcp']
        wet_monthly_mean = wet_monthly_mean / 30 # avg 30 days per month
        wet_monthly_mean = wet_monthly_mean / 1000 # (convert from mm to m)
        wet_monthly_mean.attrs['units'] = 'm'
        wet_monthly_mean.rio.write_crs(actual_crs, inplace=True)
        wet_monthly_mean = wet_monthly_mean.rio.reproject(crs)
    return wet_monthly_mean

def get_soil_transmissivity_raster(geom, crs="epsg:4326"):
    ksat_mean_url = 'https://soilmap2-1.lawr.ucdavis.edu/800m_grids/rasters/mean_ksat.tif'
    soil_depth_url = 'https://soilmap2-1.lawr.ucdavis.edu/800m_grids/rasters/soil_depth.tif'

    ksat_mean = rioxarray.open_rasterio(ksat_mean_url) # micrometers per second
    # convert to meters per day
    ksat_mean = ksat_mean * 86400 * 1e-6
    ksat_mean = ksat_mean.rio.reproject(crs)
    ksat_mean = ksat_mean.rio.clip(geometries=[geom], crs=crs)

    soil_depth = rioxarray.open_rasterio(soil_depth_url) # cm
    # convert to meters
    soil_depth = soil_depth * 1e-2
    soil_depth = soil_depth.rio.reproject(crs)
    soil_depth = soil_depth.rio.clip(geometries=[geom], crs=crs)

    with xarray.set_options(keep_attrs=True):
        t = ksat_mean * soil_depth
        t = t.where(t != ksat_mean.rio.nodata * soil_depth.rio.nodata, t.rio.nodata)

    return t

def get_soil_bulk_density_raster(geom, crs="epsg:4326"):
    bulk_density_url = 'https://soilmap2-1.lawr.ucdavis.edu/800m_grids/rasters/db.tif'
    bulk_density = rioxarray.open_rasterio(bulk_density_url)
    bulk_density = bulk_density.rio.reproject(crs)
    # convert from g/cm3 to kg/m3
    bulk_density = bulk_density * 1e3
    bulk_density = bulk_density.rio.clip(geometries=[geom], crs=crs)
    return bulk_density
