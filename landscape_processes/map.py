"""
Given input rasters, make map
"""

from landscape_processes.terrain import compute_a_over_b
from landscape_processes.terrain import  compute_slope 
from landscape_processes.thresholds import  compute_saturated_raster
from landscape_processes.thresholds import  compute_channelization_raster
from landscape_processes.thresholds import  compute_stability

def map_dominant_processes(
        elevation_raster,
        precipitation_raster,
        soil_raster,
        adjusted_constants = {}
        constants = {}
        ):

    # TODO: figure out should rasters be in memory or on disk when passed to functions

    a_over_b = compute_a_over_b(elevation_raster, constants)
    slope = compute_slope(elevation_raster, constants)

    saturated = compute_saturated_raster(slope, precipitation


