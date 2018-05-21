# Name of the run (used to save the parameters and the output)
run_name = Example

# Source of DEM (1 => SRTM 30 m / 2 => uploaded DEM. A default location is assumed for uploaded DEMS: input_DEM.asc, see an example in EXAMPLES/UploadDEM)
source_dem = 1

# Map limits (only considered if source_dem = 1)
# lon1 = longitude of the first limit of the map
# lon2 = longitude of the second limit of the map 
# lat1 = latitude of the first limit of the map
# lat2 = latitude of the second limit of the map
lon1 = -97.7
lon2 = -96.8
lat1 = 18.6
lat2 = 19.4

# Probability distribution of collapse location (1 => Punctual / 2 => Linear / 3 => Circumference arch)
dist_source = 1

# Parameters of the collapse location
# lon_cen = longitude of the collapse zone center (only considered if source_dem = 1)
# lat_cen = latitude of the collapse zone center (only considered if source_dem = 1)
# east_cen = east coordinate of collapse zone center (only considered if source_dem = 2)
# north_cen = north coordinate of collapse zone center (only considered if source_dem = 2)
# var_cen = uncertainty of collapse position (in meters)
# azimuth_lin = azimuth of the line that define the collapse zone (in degrees, only considered if dist_source = 2)
# length_lin = length of the line that define the collapse zone (in meters, only considered if dist_source = 2)
# radius_rad = radius of the circumference arch that define the collapse zone (in meters, only considered if dist_source = 3)
# ang1_rad = initial angle of the circumference arch that define the collapse zone (in degrees, only considered if dist_source = 3. Anticlockwise)
# ang2_rad = initial angle of the circumference arch that define the collapse zone (in degrees, only considered if dist_source = 3. Anticlockwise)
lon_cen = -97.268
lat_cen = 19.030
east_cen = 499000.0
north_cen = 4175000.0
var_cen = 500.0
azimuth_lin = 40.0
length_lin = 1000.0
radius_rad = 2000.0
ang1_rad = -40.0
ang2_rad = 300.0

# Other parameters of energy cones
# height = expected height of collapse (above the surface, in meters)
# var_height = uncertainty of collapse height (in meters)
# hl = expected H/L for the energy cones
# var_hal = uncertainty of H/L
height = 1000.0
var_height = 500.0
hl = 0.20
var_hl = 0.05

# Number of energy cones computed by the code
N = 10
