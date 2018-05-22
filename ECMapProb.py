import elevation
import tifffile
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians
import sys
import os

# Auxiliary functions

def distance_two_points(lat1, lat2, lon1, lon2):

	R = 6373.0

	lat1 = radians(lat1)
	lon1 = radians(lon1)
	lat2 = radians(lat2)
	lon2 = radians(lon2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	return (R * c) * 1000

def interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, lon_cen, lat_cen, cells_lon, cells_lat, Topography):

	dlon = int(np.floor( (lon_cen - lon1 )/ (step_lon_deg) ))
	dlat = (cells_lat - 2) - int(np.floor( (lat_cen - lat1) / (step_lat_deg) ))

	if(dlon >= (cells_lon-1) or dlat >= (cells_lat-1) or dlon < 0 or dlat < 0):
		return np.nan

	aux_lon = 2 * ( lon_cen - (dlon * step_lon_deg + lon1) - step_lon_deg / 2 ) / step_lon_deg
	aux_lat = 2 *( - lat_cen + ((cells_lat - 1 - dlat) * step_lat_deg + lat1) - step_lat_deg / 2 ) / step_lat_deg

	dc = (Topography[dlat][dlon] + Topography[dlat][dlon+1] + Topography[dlat+1][dlon] + Topography[dlat+1][dlon+1]) / 4
	[x3, y3, z3] = [0, 0, dc]
	if( aux_lon >= 0.0 and abs(aux_lon) >= abs(aux_lat) ):
		[x1,y1,z1] = [1, 1, Topography[dlat+1][dlon+1]] 
		[x2,y2,z2] = [1, -1, Topography[dlat][dlon+1]] 
	elif( aux_lat >= 0.0 and abs(aux_lon) < abs(aux_lat) ):
		[x1,y1,z1] = [-1, 1, Topography[dlat+1][dlon]] 
		[x2,y2,z2] = [1, 1, Topography[dlat+1][dlon+1]] 
	elif( aux_lon < 0.0 and abs(aux_lon) >= abs(aux_lat) ):
		[x1,y1,z1] = [-1, 1, Topography[dlat+1][dlon]] 
		[x2,y2,z2] = [-1, -1, Topography[dlat][dlon]] 
	else:
		[x1,y1,z1] = [-1, -1, Topography[dlat][dlon]] 
		[x2,y2,z2] = [1, -1, Topography[dlat][dlon+1]]
 
	f1 = (y2-y1)*(z3-z1) - (y3-y1)*(z2-z1)
	f2 = (z2-z1)*(x3-x1) - (z3-z1)*(x2-x1)
	f3 = (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)

	return ((- aux_lon*f1 - aux_lat*f2) / f3 + dc)

def current_cell(lon1, lat1, step_lon_deg, step_lat_deg, lon_cen, lat_cen, cells_lon, cells_lat):

	dlon = int(np.floor( (lon_cen - lon1 )/ (step_lon_deg) ))
	dlat = (cells_lat - 2) - int(np.floor( (lat_cen - lat1) / (step_lat_deg) ))

	return [dlon, dlat]

##########################################################################################################################
################################################### MAIN PROGRAM #########################################################
##########################################################################################################################

# INPUT PARAMETERS

print 'Reading input file'

current_path = os.getcwd()
file_txt = open('input_data.py')
line = file_txt.readlines()
file_txt.close()

[run_name, source_dem, lon1, lon2, lat1, lat2] = ['run_default', 1, np.nan, np.nan, np.nan, np.nan]
[dist_source, var_cen, lon_cen, lat_cen, azimuth_lin] = [1, 0.0, np.nan, np.nan, np.nan]
[length_lin, radius_rad, ang1_rad, ang2_rad] = [np.nan, np.nan, np.nan, np.nan]
[height, var_height, hl, var_hl, N] = [np.nan, 200.0, 0.2, 0.05, 100]
[east_cen, north_cen] = [np.nan, np.nan]

for i in range(0,len(line)):
	line[i] = line[i].replace('=',' ')
	aux = line[i].split()
	if(len(aux) > 0):
		if( aux[0][0] != '#'):
			if( aux[0] == 'run_name'):
				run_name = aux[1]
			if( aux[0] == 'source_dem'):
				source_dem = int(aux[1])
			if( aux[0] == 'lon1'):
				lon1 = float(aux[1])
			if( aux[0] == 'lon2'):
				lon2 = float(aux[1])
			if( aux[0] == 'lat1'):
				lat1 = float(aux[1])
			if( aux[0] == 'lat2'):
				lat2 = float(aux[1])
			if( aux[0] == 'lat2'):
				lat2 = float(aux[1])
			if( aux[0] == 'dist_source'):
				dist_source = int(aux[1])
			if( aux[0] == 'var_cen'):
				var_cen = float(aux[1])
			if( aux[0] == 'lon_cen'):
				lon_cen = float(aux[1])
			if( aux[0] == 'lat_cen'):
				lat_cen = float(aux[1])
			if( aux[0] == 'east_cen'):
				east_cen = float(aux[1])
			if( aux[0] == 'north_cen'):
				north_cen = float(aux[1])
			if( aux[0] == 'azimuth_lin'):
				azimuth_lin = float(aux[1])
			if( aux[0] == 'length_lin'):
				length_lin = float(aux[1])
			if( aux[0] == 'radius_rad'):
				radius_rad = float(aux[1])
			if( aux[0] == 'ang1_rad'):
				ang1_rad = float(aux[1])
			if( aux[0] == 'ang2_rad'):
				ang2_rad = float(aux[1])
			if( aux[0] == 'height'):
				height = float(aux[1])
			if( aux[0] == 'var_height'):
				var_height = float(aux[1])
			if( aux[0] == 'hl'):
				hl = float(aux[1])
			if( aux[0] == 'var_hl'):
				var_hl = float(aux[1])
			if( aux[0] == 'N'):
				N = int(aux[1])

if(source_dem == 1 and (np.isnan(lon1) or np.isnan(lon2) or np.isnan(lat1) or np.isnan(lat2) or np.isnan(lon_cen) or np.isnan(lat_cen) or np.isnan(height))):
	print 'Problems with input parameters'
	sys.exit(0)

if(source_dem == 2 and (np.isnan(east_cen) or np.isnan(north_cen) or np.isnan(height))):
	print 'Problems with input parameters'
	sys.exit(0)

# IMPORT MAP
if(source_dem == 1):
	print 'Importing map'
	aux_lon = np.array([lon1, lon2])
	aux_lat = np.array([lat1, lat2])
	lon1 = min(aux_lon)
	lon2 = max(aux_lon)
	lat1 = min(aux_lat)
	lat2 = max(aux_lat)
	elevation.clip(bounds=(lon1, lat1, lon2, lat2), output=current_path + '/' + run_name + '.tif')

# READ MAP
if(source_dem == 1):
	print 'Processing map'
	fp = run_name + '.tif'
	with tifffile.TIFFfile(fp) as tif:
		data = tif.asarray()
		for page in tif:
			for tag in page.tags.values():
				t = tag.name, tag.value
			image = page.asarray()
	elevation.clean()
	Topography = np.array(image)
	Topography  = (Topography  + abs(Topography)) / 2
	cells_lon = Topography.shape[1]
	cells_lat = Topography.shape[0]

if(source_dem == 2):
	print 'Reading map'
	file_txt = open('input_DEM.asc')
	line = file_txt.readlines()
	file_txt.close()

	n_north = -1
	n_east = -1
	cellsize = -1
	indexini = -1
	nodata = -9999

	for i in range(0,10):
		aux = line[i].split()
		if(aux[0] == 'ncols'):
			n_north = int(aux[1])
		if(aux[0] == 'nrows'):
			n_east = int(aux[1])
		if(aux[0] == 'cellsize'):
			cellsize = float(aux[1])
		if(aux[0] == 'xllcorner'):
			east_cor = float(aux[1])
		if(aux[0] == 'yllcorner'):
			north_cor = float(aux[1])
		if(aux[0] == 'NODATA_value'):
			nodata = float(aux[1])
		if(len(aux) >= 10):
			indexini = i
			break

	Topography = np.zeros((n_north,n_east)) 
	for i in range(indexini, indexini + n_north):
		aux = line[i].split()
		for j in range(0, n_east):
			Topography[n_north-1-i+indexini,j] = float(aux[j])

# DEFINE THE MATRIX OF COORDINATES
if(source_dem == 1):
	distance_lon = distance_two_points(lat1,lat1,lon1,lon2)
	distance_lat = distance_two_points(lat1,lat2,lon1,lon1)

	step_lon_m = distance_lon / (cells_lon-1)
	step_lat_m = distance_lat / (cells_lat-1)

	matrix_lon = np.zeros((cells_lat,cells_lon))
	matrix_lat = np.zeros((cells_lat,cells_lon))

	for i in range(0,cells_lon):
		matrix_lon[:,i] = lon1 + (lon2 - lon1)*(i)/(cells_lon-1)
	for j in range(0,cells_lat):
		matrix_lat[j,:] = lat1 + (lat2 - lat1)*(cells_lat-1-j)/(cells_lat-1)

	step_lon_deg = (lon2 - lon1)/(cells_lon - 1)
	step_lat_deg = (lat2 - lat1)/(cells_lat - 1)

if(source_dem == 2):
	matrix_north = np.zeros((n_north,n_east))
	matrix_east = np.zeros((n_north,n_east))

	for i in range(0,n_east):
		matrix_east[:,i] = (east_cor + cellsize * i)
	for j in range(0,n_north):
		matrix_north[j,:] = (north_cor + cellsize * j)

# CREATE VECTORS OF INPUT PARAMETERS AND DELETE NEGATIVE DATA
print 'Creating input vectors'

height_vector = np.random.normal(height,var_height,N)
hl_vector = np.random.normal(hl,var_hl,N)

for i in range(0,N):
	if(height_vector[i] < 0):
		height_vector[i] = np.random.normal(height,var_height,1)
		i = i - 1
for i in range(0,N):
	if(hl_vector[i] < 0.1):
		hl_vector[i] = np.random.normal(hl,var_hl,1)
		i = i - 1

if(source_dem == 1):
	lon_cen_vector = np.random.normal(lon_cen,var_cen*step_lon_deg/step_lon_m,N)
	lat_cen_vector = np.random.normal(lat_cen,var_cen*step_lat_deg/step_lat_m,N)

	if(dist_source == 2):
		pos_structure = np.random.uniform(-1,1,N)
		lon_cen_vector = lon_cen_vector + pos_structure * np.sin(azimuth_lin * np.pi/180) * length_lin *  step_lon_deg / step_lon_m
		lat_cen_vector = lat_cen_vector + pos_structure * np.cos(azimuth_lin * np.pi/180) * length_lin * step_lat_deg / step_lat_m

	if(dist_source == 3):
		pos_structure = ang1_rad + np.random.uniform(0,1,N)*(ang2_rad - ang1_rad)
		lon_cen_vector = lon_cen_vector + np.cos(pos_structure * np.pi/180) * radius_rad  *  step_lon_deg / step_lon_m
		lat_cen_vector = lat_cen_vector + np.sin(pos_structure * np.pi/180) * radius_rad * step_lat_deg / step_lat_m

if(source_dem == 2):
	east_cen_vector = np.random.normal(east_cen,var_cen,N)
	north_cen_vector = np.random.normal(north_cen,var_cen,N)

	if(dist_source == 2):
		pos_structure = np.random.uniform(-1,1,N)
		east_cen_vector = east_cen_vector + pos_structure * np.sin(azimuth_lin * np.pi/180) * length_lin
		north_cen_vector = north_cen_vector + pos_structure * np.cos(azimuth_lin * np.pi/180) * length_lin

	if(dist_source == 3):
		pos_structure = ang1_rad + np.random.uniform(0,1,N)*(ang2_rad - ang1_rad)
		east_cen_vector = east_cen_vector  + np.cos(pos_structure * np.pi/180) * radius_rad 
		north_cen_vector = north_cen_vector + np.sin(pos_structure * np.pi/180) * radius_rad

# ENERGY CONES
print 'Computing energy cones'

if(source_dem == 1):

	data_cones = np.zeros((cells_lat,cells_lon))
	for i in range(0,N):
		boolean_map = 0
		polygon=[]
		height_eff = height_vector[i] + interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, lon_cen_vector[i], lat_cen_vector[i], cells_lon, cells_lat, Topography)
		for angle_deg in range(0,360,1):
			angle_rad = angle_deg * np.pi /180
			boolean_data = 0
			for distance in range(0, 100000, 50):
				h = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, lon_cen_vector[i] + distance*cos(angle_rad)*step_lon_deg/step_lon_m , lat_cen_vector[i] + distance*sin(angle_rad)*step_lat_deg/step_lat_m , cells_lon, cells_lat, Topography)
				if( h >= height_eff - hl_vector[i]*distance ):
					polygon.append(distance)
					boolean_data = 1
					break
			if(boolean_data == 0):
				polygon.append(2 * distance)
				boolean_map = 1

		if(boolean_map == 1):
			print ' WARNING: Please use a larger map'	
	
		[lon_index, lat_index] = current_cell(lon1, lat1, step_lon_deg, step_lat_deg, lon_cen_vector[i], lat_cen_vector[i], cells_lon, cells_lat)
		data_cones[lat_index,lon_index] = data_cones[lat_index,lon_index] + 1.0/N


		face_1 = 1
		face_2 = 1
		face_3 = 1
		face_4 = 1

		for radius in range(1,10000,1):
			sum_radius = 0
			if( face_1 == 1 ):
				face_1 = 0
				for l in range(0, 1 + 2 * radius , 1):
					[lat_ind,lon_ind] = [lat_index + radius, lon_index - radius + l]
					if(lat_ind >= 0 and lat_ind <cells_lat and lon_ind >= 0 and lon_ind <cells_lon):
						var_lon = (matrix_lon[0,lon_ind] - lon_cen_vector[i]) * step_lon_m / step_lon_deg
						var_lat = (matrix_lat[lat_ind,0] - lat_cen_vector[i]) * step_lat_m / step_lat_deg
						distance = np.sqrt(var_lon*var_lon + var_lat*var_lat)
						if(var_lon >= 0):
							angle = np.arctan(var_lat/var_lon)
						else:
							angle = np.arctan(var_lat/var_lon) + np.pi
						if(angle < 0):
							angle = angle + 2*np.pi
						dr = polygon[int(angle*180/np.pi)]
						if( dr >= distance):
							data_cones[lat_ind,lon_ind] = data_cones[lat_ind,lon_ind] + 1.0/N
							sum_radius = 1
							face_1 = 1
			if( face_2 == 1 ):
				face_2 = 0
				for l in range(0, 1 + 2 * radius , 1):
					[lat_ind,lon_ind] = [lat_index - radius, lon_index - radius + l]
					if(lat_ind >= 0 and lat_ind <cells_lat and lon_ind >= 0 and lon_ind <cells_lon):
						var_lon = (matrix_lon[0,lon_ind] - lon_cen_vector[i]) * step_lon_m / step_lon_deg
						var_lat = (matrix_lat[lat_ind,0] - lat_cen_vector[i]) * step_lat_m / step_lat_deg
						distance = np.sqrt(var_lon*var_lon + var_lat*var_lat)
						if(var_lon >= 0):
							angle = np.arctan(var_lat/var_lon)
						else:
							angle = np.arctan(var_lat/var_lon) + np.pi
						if(angle < 0):
							angle = angle + 2*np.pi
						dr = polygon[int(angle*180/np.pi)]
						if( dr >= distance):
							data_cones[lat_ind,lon_ind] = data_cones[lat_ind,lon_ind] + 1.0/N
							sum_radius = 1
							face_2 = 1
			if( face_3 == 1 ):
				face_3 = 0
				for l in range(1, 2 * radius , 1):
					[lat_ind,lon_ind] = [lat_index - radius + l, lon_index + radius]
					if(lat_ind >= 0 and lat_ind <cells_lat and lon_ind >= 0 and lon_ind <cells_lon):
						var_lon = (matrix_lon[0,lon_ind] - lon_cen_vector[i]) * step_lon_m / step_lon_deg
						var_lat = (matrix_lat[lat_ind,0] - lat_cen_vector[i]) * step_lat_m / step_lat_deg
						distance = np.sqrt(var_lon*var_lon + var_lat*var_lat)
						if(var_lon >= 0):
							angle = np.arctan(var_lat/var_lon)
						else:
							angle = np.arctan(var_lat/var_lon) + np.pi
						if(angle < 0):
							angle = angle + 2*np.pi
						dr = polygon[int(angle*180/np.pi)]
						if( dr >= distance):
							data_cones[lat_ind,lon_ind] = data_cones[lat_ind,lon_ind] + 1.0/N
							sum_radius = 1
							face_3 = 1
			if( face_4 == 1 ):
				face_4 = 0
				for l in range(1, 2 * radius , 1):
					[lat_ind,lon_ind] = [lat_index - radius + l, lon_index - radius]
					if(lat_ind >= 0 and lat_ind <cells_lat and lon_ind >= 0 and lon_ind <cells_lon):
						var_lon = (matrix_lon[0,lon_ind] - lon_cen_vector[i]) * step_lon_m / step_lon_deg
						var_lat = (matrix_lat[lat_ind,0] - lat_cen_vector[i]) * step_lat_m / step_lat_deg
						distance = np.sqrt(var_lon*var_lon + var_lat*var_lat)
						if(var_lon >= 0):
							angle = np.arctan(var_lat/var_lon)
						else:
							angle = np.arctan(var_lat/var_lon) + np.pi
						if(angle < 0):
							angle = angle + 2*np.pi
						dr = polygon[int(angle*180/np.pi)]
						if( dr >= distance):
							data_cones[lat_ind,lon_ind] = data_cones[lat_ind,lon_ind] + 1.0/N
							sum_radius = 1
							face_4 = 1
			if(sum_radius == 0):
				break
		print ' Simulation finished (N = ' + str(i+1) + ')'

if( source_dem == 2):

	data_cones = np.zeros((n_north,n_east))

	for i in range(0,N):
		boolean_map = 0
		polygon=[]
		height_eff = height_vector[i] + interpol_pos(east_cor, north_cor, cellsize, cellsize, east_cen_vector[i], north_cen_vector[i], n_east, n_north, Topography)
		for angle_deg in range(0,360,1):
			angle_rad = angle_deg * np.pi /180
			boolean_data = 0
			for distance in range(0, 100000, 50):
				h = interpol_pos(east_cor, north_cor, cellsize, cellsize, east_cen_vector[i] + distance*cos(angle_rad), north_cen_vector[i] + distance*sin(angle_rad), n_east, n_north, Topography)
				if( h >= height_eff - hl_vector[i]*distance ):
					polygon.append(distance)
					boolean_data = 1
					break
			if(boolean_data == 0):
				polygon.append(1e10)
				boolean_map = 1

		if(boolean_map == 1):
			print ' WARNING: Please use a larger map'	
	
		[east_index, north_index] = current_cell(east_cor, north_cor, cellsize, cellsize, east_cen_vector[i], north_cen_vector[i], n_east, n_north)
		data_cones[north_index, east_index] = data_cones[north_index, east_index] + 1.0/N

		face_1 = 1
		face_2 = 1
		face_3 = 1
		face_4 = 1

		for radius in range(1,10000,1):
			sum_radius = 0
			if( face_1 == 1 ):
				face_1 = 0
				for l in range(0, 1 + 2 * radius , 1):
					[east_ind, north_ind] = [east_index + radius, north_index - radius + l]
					if(north_ind >= 0 and north_ind < n_north and east_ind >= 0 and east_ind < n_east):
						var_east = (matrix_east[0,east_ind] - east_cen_vector[i])
						var_north = (matrix_north[north_ind,0] - north_cen_vector[i])
						distance = np.sqrt(var_east*var_east + var_north*var_north)
						if(var_east >= 0):
							angle = np.arctan(var_north/var_east)
						else:
							angle = np.arctan(var_north/var_east) + np.pi
						if(angle < 0):
							angle = angle + 2*np.pi
						dr = polygon[int(angle*180/np.pi)]
						if( dr >= distance):
							data_cones[north_ind,east_ind] = data_cones[north_ind,east_ind] + 1.0/N
							sum_radius = 1
							face_1 = 1
			if( face_2 == 1 ):
				face_2 = 0
				for l in range(0, 1 + 2 * radius , 1):
					[east_ind,north_ind] = [east_index - radius, north_index - radius + l]
					if(north_ind >= 0 and north_ind < n_north and east_ind >= 0 and east_ind < n_east):
						var_east = (matrix_east[0,east_ind] - east_cen_vector[i])
						var_north = (matrix_north[north_ind,0] - north_cen_vector[i])
						distance = np.sqrt(var_east*var_east + var_north*var_north)
						if(var_east >= 0):
							angle = np.arctan(var_north/var_east)
						else:
							angle = np.arctan(var_north/var_east) + np.pi
						if(angle < 0):
							angle = angle + 2*np.pi
						dr = polygon[int(angle*180/np.pi)]
						if( dr >= distance):
							data_cones[north_ind,east_ind] = data_cones[north_ind,east_ind] + 1.0/N
							sum_radius = 1
							face_2 = 1
			if( face_3 == 1 ):
				face_3 = 0
				for l in range(1, 2 * radius , 1):
					[east_ind,north_ind] = [east_index - radius + l, north_index + radius]
					if(north_ind >= 0 and north_ind < n_north and east_ind >= 0 and east_ind < n_east):
						var_east = (matrix_east[0,east_ind] - east_cen_vector[i])
						var_north = (matrix_north[north_ind,0] - north_cen_vector[i])
						distance = np.sqrt(var_east*var_east + var_north*var_north)
						if(var_east >= 0):
							angle = np.arctan(var_north/var_east)
						else:
							angle = np.arctan(var_north/var_east) + np.pi
						if(angle < 0):
							angle = angle + 2*np.pi
						dr = polygon[int(angle*180/np.pi)]
						if( dr >= distance):
							data_cones[north_ind,east_ind] = data_cones[north_ind,east_ind] + 1.0/N
							sum_radius = 1
							face_3 = 1
			if( face_4 == 1 ):
				face_4 = 0
				for l in range(1, 2 * radius , 1):
					[east_ind,north_ind] = [east_index - radius + l, north_index - radius]
					if(north_ind >= 0 and north_ind < n_north and east_ind >= 0 and east_ind < n_east):
						var_east = (matrix_east[0,east_ind] - east_cen_vector[i])
						var_north = (matrix_north[north_ind,0] - north_cen_vector[i])
						distance = np.sqrt(var_east*var_east + var_north*var_north)
						if(var_east >= 0):
							angle = np.arctan(var_north/var_east)
						else:
							angle = np.arctan(var_north/var_east) + np.pi
						if(angle < 0):
							angle = angle + 2*np.pi
						dr = polygon[int(angle*180/np.pi)]
						if( dr >= distance):
							data_cones[north_ind,east_ind] = data_cones[north_ind,east_ind] + 1.0/N
							sum_radius = 1
							face_4 = 1
			if(sum_radius == 0):
				break
		print ' Simulation finished (N = ' + str(i+1) + ')'


# FIGURES
if(source_dem == 1):
	plt.figure(1)
	cmapg = plt.cm.get_cmap('Greys')
	plt.contourf(matrix_lon,matrix_lat,Topography,100,cmap=cmapg,min=0)
	plt.colorbar()
	cmapr = plt.cm.get_cmap('Reds')
	CS = plt.contourf(matrix_lon,matrix_lat,data_cones, N+1, alpha= 0.5, interpolation='nearest', cmap=cmapr, min=1e-20, max=1.01, antialiased=True, lw=0.01)	
	fmt = '%.1f'
	CS_lines = plt.contour(matrix_lon,matrix_lat,data_cones, np.array([0.1, 0.2, 0.4, 0.7]), min=1e-20, max=1.01, colors='w', interpolation='nearest')
	plt.clabel(CS_lines, inline=1, fontsize=10, colors='k', fmt=fmt)
	plt.axes().set_aspect(step_lat_m/step_lon_m)
	plt.xlabel('Longitude $[^\circ]$')
	plt.ylabel('Latitude $[^\circ]$')
	for i in range(0,N):
		plt.plot( lon_cen_vector[i], lat_cen_vector[i], 'r.', markersize=2)
	plt.savefig(run_name + '_map.png')

	plt.figure(2)
	plt.subplot(121)
	plt.hist(height_vector)
	plt.xlabel('Initial height [m]')
	plt.subplot(122)
	plt.hist(hl_vector)
	plt.xlabel('H/L')
	plt.savefig(run_name + '_histogram.png')
	plt.show()

if(source_dem == 2):
	plt.figure(1)
	cmapg = plt.cm.get_cmap('Greys')
	plt.contourf(matrix_east,matrix_north,Topography,100,cmap=cmapg,min=0)
	plt.colorbar()
	cmapr = plt.cm.get_cmap('Reds')
	CS = plt.contourf(matrix_east,matrix_north,data_cones, N+1, alpha= 0.5, interpolation='nearest', cmap=cmapr, min=1e-20, max=1.01, antialiased=True, lw=0.01)	
	fmt = '%.1f'
	CS_lines = plt.contour(matrix_east,matrix_north,data_cones, np.array([0.1, 0.2, 0.4, 0.7]), min=1e-20, max=1.01, colors='w', interpolation='nearest')
	plt.clabel(CS_lines, inline=1, fontsize=10, colors='k', fmt=fmt)
	plt.axes().set_aspect(1.0)
	plt.xlabel('East [m]')
	plt.ylabel('North [m]')
	for i in range(0,N):
		plt.plot( east_cen_vector[i], north_cen_vector[i], 'r.', markersize=2)
	plt.savefig(run_name + '_map.png')

	plt.figure(2)
	plt.subplot(121)
	plt.hist(height_vector)
	plt.xlabel('Initial height [m]')
	plt.subplot(122)
	plt.hist(hl_vector)
	plt.xlabel('H/L')
	plt.savefig(run_name + '_histogram.png')
	plt.show()
