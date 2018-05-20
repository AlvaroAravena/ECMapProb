# Name of the run (used to save the parameters and the output)
run_name = Vesuvius

# Source of DEM (1 => SRTM 30 m / 2 => uploaded DEM. A default location is assumed for uploaded DEMS: input_DEM.asc, see example in EXAMPLES/UploadDEM)
source_dem = 1

# Map limits (only considered if source_dem = 1)
# lon1 = longitude of the first limit of the map
# lon2 = longitude of the second limit of the map 
# lat1 = latitude of the first limit of the map
# lat2 = latitude of the second limit of the map
lon1 = 14.1
lon2 = 14.8
lat1 = 40.5
lat2 = 41.1

# Probability distribution of collapse location (1 => Punctual / 2 => Linear / 3 => Radial)
dist_source = 1

# Parameters of the collapse location
# lon_cen = longitude of the collapse position center (only considered if source_dem = 1)
# lat_cen = latitude of the collapse position center (only considered if source_dem = 1)
# east_cen = east position of collapse center (only considered if source_dem = 2)
# north_cen = north position of collapse center (only considered if source_dem = 2)
# var_cen = uncertainty of collapse position center (in meters)
# azimuth_lin = azimuth of the line that define the collapse position (in degrees, only considered if dist_source = 2)
# length_lin = length of the line that define the collapse position (in meters, only considered if dist_source = 2)
# radius_rad = radius of the circumference arch that define the collapse position (in meters, only considered if dist_source = 3)
# ang1_rad = initial angle of the circumference arch that define the collapse position (in degrees, only considered if dist_source = 3)
# ang2_rad = initial angle of the circumference arch that define the collapse position (in degrees, only considered if dist_source = 3)
lon_cen = 14.427
lat_cen = 40.822
var_cen = 500.0

# Other parameters of energy cones
# height = expected height above the surface of collapse (in meters)
# var_height = uncertainty of collapse height (in meters)
# hl = expected H/L for the energy cones
# var_hal = uncertainty of H/L
height = 1500.0
var_height = 500.0
hl = 0.20
var_hl = 0.05

# Number of energy cones computed by the code
N = 100
