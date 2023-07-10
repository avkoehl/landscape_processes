import rioxarray as rxr

def load_raster_xr(raster):
    if isinstance(raster, str):
        return rxr.open_rasterio(raster).squeeze()
    elif isinstance(raster, xr.DataArray):
        return raster
    else:
        raise ValueError("raster must be a string or xarray.DataArray")
