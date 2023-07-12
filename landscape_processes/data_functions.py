import os

import numpy as np
import py3dep
import pydaymet
import rioxarray
import xarray

def get_elevation_raster(geom, geom_crs="epsg:4326", crs="EPSG:5070"):
    """ Get a DEM raster for a given geometry
    Reproject to a projected crs (default is 5070) for future operations
    """
    dem = py3dep.get_map("DEM", geom, resolution=10, geo_crs=geom_crs)
    dem = dem.rio.reproject(crs)
    return dem

def get_annual_precip_raster(geom, geom_crs="epsg:4326", crs="EPSG:5070"):
    years = list(range(1992, 2022))
    yearly_data = pydaymet.get_bygeom(geom, variables='prcp', dates= years, time_scale = "annual", crs=geom_crs)
    response_crs = yearly_data.rio.crs
    
    yearly_mean = yearly_data.mean(dim = 'time') # get raster that is the mean of all the years
    yearly_mean = yearly_mean['prcp']

    with xarray.set_options(keep_attrs=True):
        yearly_mean = yearly_mean / 365 # days per year
        yearly_mean = yearly_mean / 1000 # (convert from mm to m)
        
    yearly_mean.attrs['units'] = 'm/day'
    yearly_mean.attrs['long_name'] = "mean annual total precipitation"
    yearly_mean.attrs['_FillValue'] = np.nan
    yearly_mean.rio.write_nodata(np.nan, inplace=True)

    yearly_mean.rio.write_crs(response_crs, inplace=True)
    yearly_mean = yearly_mean.rio.reproject(crs)
    return yearly_mean

def get_wet_month_precip_raster(geom, geom_crs="epsg:4326", crs="EPSG:5070"):
    years = list(range(1992, 2022))
    monthly_data = pydaymet.get_bygeom(geom, variables='prcp', dates=years, time_scale = "monthly", crs=geom_crs)
    response_crs = monthly_data.rio.crs
    
    monthly_means = monthly_data.groupby('time.month').mean(dim = 'time')
    monthly_scalar_means = monthly_means.groupby('month').mean(dim = ['x','y'])
    max_month = monthly_scalar_means['prcp'].argmax(dim='month')
    wet_monthly_mean = monthly_means.sel(month = max_month+1) # note index (return of argmax) starts at 0 months start at 1
    wet_monthly_mean = wet_monthly_mean['prcp']
    
    with xarray.set_options(keep_attrs=True):
        wet_monthly_mean = wet_monthly_mean / 30 # avg 30 days per month
        wet_monthly_mean = wet_monthly_mean / 1000 # (convert from mm to m)
        
    wet_monthly_mean.attrs['units'] = 'm/day'
    wet_monthly_mean.rio.write_crs(response_crs, inplace=True)
    wet_monthly_mean = wet_monthly_mean.rio.reproject(crs)
    wet_monthly_mean = wet_monthly_mean.drop_vars(['month'])
    wet_monthly_mean.attrs['_FillValue'] = np.nan
    wet_monthly_mean.rio.write_nodata(np.nan, inplace=True)

    return wet_monthly_mean

def get_soil_transmissivity_raster(geom, geom_crs="epsg:4326", crs="EPSG:5070"):
    ksat_mean_url = 'https://soilmap2-1.lawr.ucdavis.edu/800m_grids/rasters/mean_ksat.tif'
    soil_depth_url = 'https://soilmap2-1.lawr.ucdavis.edu/800m_grids/rasters/soil_depth.tif'

    ksat_mean = rioxarray.open_rasterio(ksat_mean_url) # micrometers per second

    # convert to meters per day
    with xarray.set_options(keep_attrs=True):
        ksat_mean = ksat_mean * 86400 * 1e-6
  
    soil_depth = rioxarray.open_rasterio(soil_depth_url) # cm
    # convert to meters
    with xarray.set_options(keep_attrs=True):
        soil_depth = soil_depth * 1e-2

    with xarray.set_options(keep_attrs=True):
        t = ksat_mean * soil_depth
    
    t = t.rio.reproject(crs)
    t = t.rio.clip(geometries=[geom], crs=geom_crs)
    
    # this sets nodata values to np.nan
    t.rio.to_raster('temp.tif')
    t = rioxarray.open_rasterio('temp.tif', masked=True).squeeze()
    os.remove('temp.tif')
    t.attrs['_FillValue'] = np.nan
    t.rio.write_nodata(np.nan, inplace=True)

    return t


def get_soil_bulk_density_raster(geom, geom_crs="epsg:4326", crs="EPSG:5070"):
    bulk_density_url = 'https://soilmap2-1.lawr.ucdavis.edu/800m_grids/rasters/db.tif'
    bulk_density = rioxarray.open_rasterio(bulk_density_url)
    
    with xarray.set_options(keep_attrs=True):
        bulk_density = bulk_density * 1e3
        
    bulk_density = bulk_density.rio.reproject(crs)
    bulk_density = bulk_density.rio.clip(geometries=[geom], crs=geom_crs)
    
    # this sets nodata values to np.nan
    bulk_density.rio.to_raster('temp.tif')
    bulk_density = rioxarray.open_rasterio('temp.tif', masked=True).squeeze()
    os.remove('temp.tif')
    bulk_density.attrs['_FillValue'] = np.nan
    bulk_density.rio.write_nodata(np.nan, inplace=True)
    
    return bulk_density

def get_aligned_input_rasters(geom, geom_crs="EPSG:4326", crs="EPSG:5070", wet=False):
    dem = get_elevation_raster(geom, geom_crs=geom_crs, crs=crs)
    t = get_soil_transmissivity_raster(geom, geom_crs=geom_crs, crs=crs)
    bd = get_soil_bulk_density_raster(geom, geom_crs=geom_crs, crs=crs)

    if wet:
        p = get_wet_month_precip_raster(geom, geom_crs=geom_crs, crs=crs)
    else:
        p = get_annual_precip_raster(geom, geom_crs=geom_crs, crs=crs)

    t = t.rio.reproject_match(dem)
    bd = bd.rio.reproject_match(dem)
    p = p.rio.reproject_match(dem)
        
    return dem, t, bd, p

