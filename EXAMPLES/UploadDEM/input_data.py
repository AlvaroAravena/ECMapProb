# Name of the run (used to save the parameters and the output)
run_name = Example

# Source of DEM (1 => SRTM 30 m / 2 => uploaded DEM. A default location is assumed for uploaded DEMS: input_DEM.asc, see an example in EXAMPLES/UploadDEM)
source_dem = 2

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
east_cen = 499000.0
north_cen = 4175000.0
var_cen = 200.0

# Other parameters of energy cones
# height = expected height of collapse (above the surface, in meters)
# var_height = uncertainty of collapse height (in meters)
# hl = expected H/L for the energy cones
# var_hal = uncertainty of H/L
height = 300.0
var_height = 100.0
hl = 0.50
var_hl = 0.05

# Number of energy cones computed by the code
N = 100
