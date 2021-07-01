# Name of the run (used to save the parameters and the output).
run_name = Chaiten_F

# Type of simulation (1: Default mode: Construction of probability map. 2: Calibration mode).
type_sim = 1

# Source of DEM.
# source_dem = type of input data (1: SRTM 30 m. 2: Uploaded DEM (UTM). 3: Uploaded Data (lat, lon)).
# topography_file = location of file containing topography (only used when source_dem = 2 or 3).
# (See examples of source_dem = 2 in EXAMPLES/Normal_Version/Upload_DEM_UTM and of source_dem = 3 in EXAMPLES/Normal_Version/Upload_DEM_deg).
# (Simulations with source_dem = 1 and save_data = 1 create a compatible topography file for source_dem = 3 in Results/run_name called Topography_3.txt).
source_dem = 1

# Inputs for calibration mode (Only considered if type_sim = 2).
# comparison_polygon = name of file of bound points of comparison polygon (See an example in EXAMPLES/Normal_Version/Chaiten_D. If absent, only runout distance or inundation area-based calibrations can be performed).
# ang_cal = angle from vent to circumference arch center that defines the PDC dispersion direction used to calibrate. If absent, all the transport directions are considered.
# ang_cal_range = extent of the circumference arch that defines the PDC dispersion direction used to calibrate. If absent, all the transport directions are considered.

# Map limits (only considered if source_dem = 1).
# lon1 = longitude of the first limit of the map.
# lon2 = longitude of the second limit of the map.
# lat1 = latitude of the first limit of the map.
# lat2 = latitude of the second limit of the map.
lon1 = -72.8
lon2 = -72.5
lat1 = -42.95
lat2 = -42.75

# Parameters of the collapse position.
# vent_type = type of distribution of collapse position (1: Pointwise. 2: Linear. 3: Circumference arch. 4: Input file. Only considered if type_sim = 1, otherwise vent_type = 1).
# lon_cen = longitude of the collapse zone center (only considered if source_dem = 1 or 3 and vent_type = 1, 2 or 3).
# lat_cen = latitude of the collapse zone center (only considered if source_dem = 1 or 3 and vent_type = 1, 2 or 3).
# east_cen = east coordinate of collapse zone center (only considered if source_dem = 2 and vent_type = 1, 2 or 3).
# north_cen = north coordinate of collapse zone center (only considered if source_dem = 2 and vent_type = 1, 2 or 3).
# azimuth_lin = azimuth of the line defining the collapse zone (in degrees. Only considered if vent_type = 2).
# length_lin = length of the line defining the collapse zone (in meters. Only considered if vent_type = 2).
# radius_rad = radius of the circumference arch defining the collapse zone (in meters. Only considered if vent_type = 3).
# ang1_rad = initial angle of the circumference arch defining the collapse zone (in degrees. Only considered if vent_type = 3. Anticlockwise).
# ang2_rad = final angle of the circumference arch defining the collapse zone (in degrees. Only considered if vent_type = 3. Anticlockwise).
# var_cen = uncertainty of collapse position (in meters. Only considered if type_sim = 1 and vent_type = 1, 2 or 3).
# dist_input_cen = type of distribution for collapse position variability (1: Gaussian. 2: Uniform. Only considered if type_sim = 1 and vent_type = 1, 2 or 3).
# input_file_vent = name of the file with the set of values for vent positions (only considered if vent_type = 4).
vent_type = 1
lon_cen = -72.650
lat_cen = -42.835
var_cen = 0.00
dist_input_cen = 1

# Other parameters of energy cones
# type_input = type of distribution for height and H/L (1: Prescribed distribution. 2: Input file with values of height and hl. 3: Calibration-based sampling. Only considered if type_sim = 1, otherwise type_input = 1).
# dist_input_height = type of prescribed distribution for height(1: Gaussian. 2: Uniform. 3: Gamma. 4: Lognormal. Only considered if type_input = 1. If type_sim = 2, dist_input_height = 2).
# height = expected height of collapse (above the surface, in meters. Only considered if type_input = 1 and dist_input_height = 1, 2 or 4).
# var_height = uncertainty of collapse height (in meters. Only considered if type_input = 1 and dist_input_height = 1, 2 or 4).
# height_k = k in gamma distribution of collapse height (only considered if type_input = 1 and dist_input_height = 3).
# height_theta = theta in gamma distribution of collapse height (only considered if type_input = 1 and dist_input_height = 3).
# dist_input_hl = type of prescribed distribution for H/L (1: Gaussian. 2: Uniform. 3: Gamma. 4: Lognormal. Only considered if type_input = 1. If type_sim = 2, dist_input_hl = 2).
# hl = H/L for the energy cones (only considered if type_input = 1 and dist_input_hl = 1, 2 or 4).
# var_hl = uncertainty of hl (only considered if type_input = 1 and dist_input_hl = 1, 2 or 4).
# hl_k = k in gamma distribution of H/L (only considered if type_input = 1 and dist_input_hl = 3).
# hl_theta = theta in gamma distribution of H/L (only considered if type_input = 1 and dist_input_hl = 3).
# input_file_cal = name of the file with the set of values of height and H/L (when type_input = 2) or name of the calibration file (when type_input = 3). Only considered if type_input = 2 or 3.
# calibration_type = type of calibration (1: Jaccard. 2: HD. 3: RMSD. 4: Directional Jaccard. 5: Distance. 6: Directional distance. 7: Area). Only considered if type_sim = 1 and type_input = 3.
# dist_distance_calibration = type of distance distribution used for distance-based calibration (1: Gaussian. 2: Uniform. 3: Gamma. 4: Lognormal. 5: Input cumulative distribution. Only considered if type_sim = 1, type_input = 3, and calibration_type = 5 or 6).
# distance_calibration = expected distance used for distance-based calibration (In meters. Only considered if type_sim = 1, type_input = 3, calibration_type = 5 or 6, and dist_distance_calibration = 1, 2 or 4).
# var_distance_calibration = variability of distance used for distance-based calibration (In meters. Only considered if type_sim = 1, type_input = 3, calibration_type = 5 or 6, and dist_distance_calibration = 1, 2 or 4).
# distance_calibration_k = k in gamma distance distribution used for distance-based calibration (only considered if type_sim = 1, type_input = 3, calibration_type = 5 or 6, and dist_distance_calibration = 3).
# distance_calibration_theta = theta in gamma distance distribution used for distance-based calibration (only considered if type_sim = 1, type_input = 3, calibration_type = 5 or 6, and dist_distance_calibration = 3).
# file_cumulative_distance = name of the file with the cumulative distribution of runout distance used in the calibration procedure (only considered if type_sim = 1, type_input = 3, calibration_type = 5 or 6, and dist_distance_calibration = 5).
# dist_area_calibration = type of area distribution used for area-based calibration (1: Gaussian. 2: Uniform. 3: Gamma. 4: Lognormal. 5: Input cumulative distribution. Only considered if type_sim = 1, type_input = 3, and calibration_type = 7).
# area_calibration = expected area used for area-based calibration (In km2. Only considered if type_sim = 1, type_input = 3, calibration_type = 7, and dist_area_calibration = 1, 2 or 4).
# var_area_calibration = variability of area used for area-based calibration (In km2. Only considered if type_sim = 1, type_input = 3, calibration_type = 7, and dist_area_calibration = 1, 2 or 4).
# area_calibration_k = k in gamma area distribution used for area-based calibration (only considered if type_sim = 1, type_input = 3, calibration_type = 7, and dist_area_calibration = 3).
# area_calibration_theta = theta in gamma area distribution used for area-based calibration (only considered if type_sim = 1, type_input = 3, calibration_type = 7, and dist_area_calibration = 3).
# file_cumulative_area = name of the file with the cumulative distribution of runout distance or inundation area used in the calibration (only considered if type_sim = 1, type_input = 3, calibration_type = 7, and dist_area_calibration = 5).
type_input = 3
input_file_cal = ./EXAMPLES/Normal_Version/Chaiten_D/Calibration_Data.txt
calibration_type = 7
dist_area_calibration = 5
file_cumulative_area = ./EXAMPLES/Normal_Version/Chaiten_F/Cumulative_Data.txt

# Maximum order of energy cones.
cone_levels = 100

# Number of simulations (Only considered if type_input = 1 or 3 and vent_type = 1, 2 or 3).
N = 100

# Save results in files txt (1: Yes. 0: No).
save_data = 1
