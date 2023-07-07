# Landscape Processes

## Thresholds of landscape condition

| Variable     | Description |
|--------------|-------------|
| $` a `$      | contributing area
| $` b `$      | contour width
| $` M `$      | slope
| $` T `$      | transmissivity
| $` q `$      | runoff
| $` \tau `$   | critical sheer stress for channelization
| $` p_{w} `$  | density of water
| $` k `$      | surface roughness
| $` v `$      | kinematic viscosity of water
| $` g `$      | gravity
| $` p_{s} `$  | dry bulk density of sediment
| $` \theta `$ | slope
| $` \phi `$   | internal friction angle

| Constants           | Symbol      | Value              | Units
|---------------------|-------------|--------------------|------
| water density       | $` p_{w} `$ | 1000               | kg/m^3
| gravity constant    | $` g `$     | 9.81               | m/s^2
| kinematic viscosity | $` v `$     | $` 1.31 * 10 ^6 `$ | m/s^2
| seconds per day     |             |  86400             | s/d


Saturated:

$` \frac{a}{b}> \frac{\tau }{q}M `$

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

## Inputs

- 10m DEM of watershed
- Yearly Mean Precipitation (30 year PRISM); Yearly Monthly Max Precipitation (30 year PRISM)
- Soil Map for transmissivity [NRCS web soil survey](http://websoilsurvey.sc.egov.usda.gov/App/HomePage.htm)

## Process

DEM
1. Preprocess the DEM (fill sinks, add known channel)
2. create slope raster
3. create flow accumulation raster
4. create contributing area raster
5. create a/b raster (contributing area / pixel width)

PRECIPITATION
1.
2. 

SOIL
1. 
2. 


