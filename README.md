# Landscape Processes

## Input Rasters

All clipped to study area and coregistered 

| Name             | Description                           | units
|------------------|---------------------------------------|------
| `dem`            | elevation                             | m
| `precip`         | precipitation 30 year norm            | m/day
| `T`              | transmissivity of soil (Ksat * depth) | m^2/day
| $`p_{s}`$        | particle bulk density of the soil     | kg/m^3

## Thresholds of landscape condition

Derived Rasters:
| Input        | Description                  | Source                                     | units
|--------------|------------------------------|--------------------------------------------|--------
| $` a `$      | contributing area            | dem                                        | m^2
| $` b `$      | contour width                | dem pixel resolution                       | m
| $` M `$      | slope                        | dem                                        | degrees
| $` q `$      | runoff                       | precip * loss factor (ET, land use raster) | m/day
| $` \theta `$ | slope (same as M?)           | dem                                        | degrees

Parameters:
| Symbol         | Description                              | Default Value | units 
|----------------|------------------------------------------|---------------|-----
| $` \tau `$     | critical sheer stress for channelization | 16            | Pa
| $` \phi `$     | internal friction angle                  | 45            | degrees
| $` k `$        | surface roughness                        | 10000         | (dimensionless)

Constants:
|  Symbol      | Description         | Value               | Units
|--------------|---------------------|---------------------|------
|  $` p_{w} `$ | water density       | 1000                | kg/m^3
|  $` g `$     | gravity constant    | 9.81                | m/s^2
|  $` v `$     | kinematic viscosity | $` 1.31 * 10 ^-6 `$ | m^2/s
|              | seconds per day     |  86400              | s/d

Saturated:

$` \frac{a}{b}> \frac{T }{q}M `$

Channelization:

$` \frac{a}{b}> \frac{2T^3 }{p_{w}^{3}kvg^2M^2q} + \frac{T}{q}M `$

Shallow Landsliding:

$` \frac{a}{b}> \frac{p_{s}}{p_{w}} \left [ 1 - \frac{tan\theta}{tan\phi}   \right ]\frac{T}{q}M `$

Unconditionally stable:

$` tan\theta < 0.5 tan\phi `$

Unconditionally unstable

$` tan\theta > tan\phi `$


| Landscape Condition       | Process Domain  |
|---------------------------|-----------------|
| Unsaturated               | Soil Creep      |
| Saturated                 | Sheet Wash      |
| Channelized               | Channelization  |
| Unconditionally Stable    | Landslide (wet) |
| Unconditionally Unstable  | Landslide (dry) |
