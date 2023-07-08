import rasterio

from rasterio.warp import calculate_default_transform
from rasterio.warp import reproject
from rasterio.warp import Resampling

# See: https://pygis.io/docs/e_raster_resample.html#raster-resample-methods

def align_rasters(raster_path, reference_raster_path, outfile):
    """Snap a raster to a reference raster.

    Args:
        raster_path (str): Path to the raster to be snapped.
        reference_raster_path (str): Path to the reference raster.
        outfile (str): Path to the output raster.
    """
    with rasterio.open(raster_path) as src:

        with rasterio.open(reference_raster_path) as ref:
            transform, width, height = calculate_default_transform(
                src.crs, ref.crs, ref.width, ref.height, *ref.bounds
            )
            kwargs = src.meta.copy()
            kwargs.update(
                {
                    "crs": ref.crs,
                    "transform": transform,
                    "width": width,
                    "height": height,
                    'nodata': -9999
                    })
        with rasterio.open(outfile, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform = src.transform,
                    src_crs = src.crs,
                    dst_transform = transform,
                    dst_crs = ref.crs,
                    resampling=Resampling.nearest)

