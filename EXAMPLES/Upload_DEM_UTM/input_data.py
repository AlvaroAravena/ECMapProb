# Name of the run (used to save the parameters and the output)
run_name = Upload_DEM_UTM

# Source of DEM
# source_dem = type of input data (1 => SRTM 30 m / 2 => Uploaded DEM (UTM) / 3 => Uploaded Data (lat,lon)).
# topography_file = location of file containing topography (only used when source_dem = 2 or source_dem = 3).
# (see examples of source_dem = 2 in EXAMPLES/Upload_DEM_UTM and of source_dem = 3 in EXAMPLES/Upload_DEM_deg).
# (Simulations with source_dem = 1 and save_data = 1 create a compatible topography file for source_dem = 3 in Results
# called Topography_3.txt).
source_dem = 2
topography_file = input_DEM.asc

# Map limits (only considered if source_dem = 1)
# lon1 = longitude of the first limit of the map
# lon2 = longitude of the second limit of the map 
# lat1 = latitude of the first limit of the map
# lat2 = latitude of the second limit of the map

# Maximum order of energy cones
cone_levels = 30

# Probability distribution of collapse location (1 => Punctual / 2 => Linear / 3 => Circumference arch)
dist_source = 1

# Parameters of the collapse location
# lon_cen = longitude of the collapse zone center (only considered if source_dem = 1 or 3)
# lat_cen = latitude of the collapse zone center (only considered if source_dem = 1 or 3)
# east_cen = east coordinate of collapse zone center (only considered if source_dem = 2)
# north_cen = north coordinate of collapse zone center (only considered if source_dem = 2)
# var_cen = uncertainty of collapse position (in meters)
# azimuth_lin = azimuth of the line that define the collapse zone (in degrees, only considered if dist_source = 2)
# length_lin = length of the line that define the collapse zone (in meters, only considered if dist_source = 2)
# radius_rad = radius of the circumference arch that define the collapse zone (in meters, only considered if dist_source = 3)
# ang1_rad = initial angle of the circumference arch that define the collapse zone (in degrees, only considered if dist_source = 3. Anticlockwise)
# ang2_rad = initial angle of the circumference arch that define the collapse zone (in degrees, only considered if dist_source = 3. Anticlockwise)
east_cen = 501000.0
north_cen = 4178000.0
var_cen = 100.0

# Other parameters of energy cones
# height = expected height of collapse (above the surface, in meters)
# hl = H/L for the energy cones
# var_height = uncertainty of collapse height (in meters)
# var_hl = uncertainty of hl
# dist_input = type of distribution for height and H/L (1 => Gaussian / 2 => Uniform)
height = 50.0
hl = 0.65
var_height = 50.0
var_hl = 0.05
dist_input = 2

# Number of simulations computed by the code
N = 200

# Save results in files txt ( 1 => Yes / 0 => No )
save_data = 1

# Assumption for redistributing potential energy (1, 2, 3 or 4. Please use 4)
redist_energy = 4
