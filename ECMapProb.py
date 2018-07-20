import elevation
import tifffile
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians, log, factorial, tan
import sys
import os
from PIL import Image, ImageDraw

# Auxiliary functions

def distance_two_points(lat1, lat2, lon1, lon2):

	R = 6373.0

	lat1 = radians(lat1)
	lon1 = radians(lon1)
	lat2 = radians(lat2)
	lon2 = radians(lon2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2.0)**2.0 + cos(lat1) * cos(lat2) * sin(dlon / 2.0)**2.0
	c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a))
	return (R * c) * 1000.0

def interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, lon_cen, lat_cen, cells_lon, cells_lat, Topography):

	dlon = int(np.floor( (lon_cen - lon1 )/ (step_lon_deg) ))
	dlat = (cells_lat - 2) - int(np.floor( (lat_cen - lat1) / (step_lat_deg) ))

	if(dlon >= (cells_lon-1.0) or dlat >= (cells_lat-1.0) or dlon < 0.0 or dlat < 0.0):
		return 99999

	aux_lon = 2.0 * ( lon_cen - (dlon * step_lon_deg + lon1) - step_lon_deg / 2.0 ) / step_lon_deg
	aux_lat = 2.0 *( - lat_cen + ((cells_lat - 1.0 - dlat) * step_lat_deg + lat1) - step_lat_deg / 2.0 ) / step_lat_deg

	dc = (Topography[dlat][dlon] + Topography[dlat][dlon+1] + Topography[dlat+1][dlon] + Topography[dlat+1][dlon+1]) / 4
	[x3, y3, z3] = [0.0, 0.0, dc]
	if( aux_lon >= 0.0 and abs(aux_lon) >= abs(aux_lat) ):
		[x1,y1,z1] = [1.0, 1.0, Topography[dlat+1][dlon+1]] 
		[x2,y2,z2] = [1.0, -1.0, Topography[dlat][dlon+1]] 
	elif( aux_lat >= 0.0 and abs(aux_lon) < abs(aux_lat) ):
		[x1,y1,z1] = [-1.0, 1.0, Topography[dlat+1][dlon]] 
		[x2,y2,z2] = [1.0, 1.0, Topography[dlat+1][dlon+1]] 
	elif( aux_lon < 0.0 and abs(aux_lon) >= abs(aux_lat) ):
		[x1,y1,z1] = [-1.0, 1.0, Topography[dlat+1][dlon]] 
		[x2,y2,z2] = [-1.0, -1.0, Topography[dlat][dlon]] 
	else:
		[x1,y1,z1] = [-1.0, -1.0, Topography[dlat][dlon]] 
		[x2,y2,z2] = [1.0, -1.0, Topography[dlat][dlon+1]]
 
	f1 = (y2-y1)*(z3-z1) - (y3-y1)*(z2-z1)
	f2 = (z2-z1)*(x3-x1) - (z3-z1)*(x2-x1)
	f3 = (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)

	return ((- aux_lon * f1 - aux_lat * f2) / f3 + dc)

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
[dist_source, var_cen, lon_cen, lat_cen, east_cen, north_cen, azimuth_lin] = [1, 0.0, np.nan, np.nan, np.nan, np.nan, np.nan]
[length_lin, radius_rad, ang1_rad, ang2_rad] = [np.nan, np.nan, np.nan, np.nan]
[height, hl, var_height, var_hl, N, cone_levels] = [np.nan, 0.2, 200.0, 0.05, 100, 1]

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
			if( aux[0] == 'hl'):
				hl = float(aux[1])
			if( aux[0] == 'var_height'):
				var_height = float(aux[1])
			if( aux[0] == 'var_hl'):
				var_hl = float(aux[1])
			if( aux[0] == 'N'):
				N = int(aux[1])
			if( aux[0] == 'cone_levels'):
				cone_levels = int(aux[1])

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

	file_txt = open('Cities.txt')
	line = file_txt.readlines()
	file_txt.close()

	for population in range(10000,10000000,10000):
		Cities = []
		for i in range(1,len(line)):
			aux = line[i].split(',')
			pop = float(aux[4])
			lat_dat = float(aux[5])
			lon_dat = float(aux[6])
			if( lon_dat > lon1 and lon_dat < lon2 and lat_dat > lat1 and lat_dat < lat2 and pop > population):
				Cities.append([lon_dat, lat_dat, aux[2]])
		if(len(Cities) <= 5):
			break

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
	Topography  = (Topography  + abs(Topography)) / 2.0
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
			Topography[i-indexini,j] = float(aux[j])

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
	matrix_north = matrix_north[ range(len(matrix_north[:,0]) -1 , -1 , -1 ) , : ]

# CREATE VECTORS OF INPUT PARAMETERS AND DELETE NEGATIVE DATA
print 'Creating input vectors'

if(var_height > 0.0):
	height_vector = np.random.normal(height,var_height,N)
else:
	height_vector = np.ones(N) * height

if(var_hl > 0.0):
	hl_vector = np.random.normal(hl,var_hl,N)
else:
	hl_vector = np.ones(N) * hl

if(var_height > 0.0):
	while( 1 == 1 ):
		aux_boolean = 0
		for i in range(0,N):
			if(height_vector[i] < 0):
				height_vector[i] = np.random.normal(height,var_height,1)
				aux_boolean = 1
		if(aux_boolean == 0):
			break

if(var_hl > 0.0):
	while( 1 == 1 ):
		aux_boolean = 0
		for i in range(0,N):
			if(hl_vector[i] < 0.05):
				hl_vector[i] = np.random.normal(hl,var_hl,1)
				aux_boolean = 1
		if(aux_boolean == 0):
			break

if(source_dem == 1):
	if( var_cen > 0.0):
		lon_cen_vector = np.random.normal(lon_cen, var_cen * step_lon_deg / step_lon_m, N)
		lat_cen_vector = np.random.normal(lat_cen, var_cen * step_lat_deg / step_lat_m, N)
	else:
		lon_cen_vector = np.ones(N) * lon_cen
		lat_cen_vector = np.ones(N) * lat_cen

	if(dist_source == 2):
		pos_structure = np.random.uniform(-1,1,N)
		lon_cen_vector = lon_cen_vector + pos_structure * np.sin(azimuth_lin * np.pi/180) * length_lin *  step_lon_deg / step_lon_m
		lat_cen_vector = lat_cen_vector + pos_structure * np.cos(azimuth_lin * np.pi/180) * length_lin * step_lat_deg / step_lat_m

	if(dist_source == 3):
		pos_structure = ang1_rad + np.random.uniform(0,1,N)*(ang2_rad - ang1_rad)
		lon_cen_vector = lon_cen_vector + np.cos(pos_structure * np.pi/180) * radius_rad  *  step_lon_deg / step_lon_m
		lat_cen_vector = lat_cen_vector + np.sin(pos_structure * np.pi/180) * radius_rad * step_lat_deg / step_lat_m

if(source_dem == 2):

	if( var_cen > 0.0):
		east_cen_vector = np.random.normal(east_cen,var_cen,N)
		north_cen_vector = np.random.normal(north_cen,var_cen,N)
	else:
		east_cen_vector = np.ones(N) * east_cen
		north_cen_vector = np.ones(N) * north_cen

	if(dist_source == 2):
		pos_structure = np.random.uniform(-1,1,N)
		east_cen_vector = east_cen_vector + pos_structure * np.sin(azimuth_lin * np.pi/180) * length_lin
		north_cen_vector = north_cen_vector + pos_structure * np.cos(azimuth_lin * np.pi/180) * length_lin

	if(dist_source == 3):
		pos_structure = ang1_rad + np.random.uniform( 0 , 1 , N ) * ( ang2_rad - ang1_rad )
		east_cen_vector = east_cen_vector  + np.cos(pos_structure * np.pi/180 ) * radius_rad 
		north_cen_vector = north_cen_vector + np.sin(pos_structure * np.pi/180 ) * radius_rad

# ENERGY CONES
print 'Computing energy cones'

angstep = 10
anglen = 360 / angstep
pix_min = 0.0

if(source_dem == 1):

	data_cones = np.zeros((cells_lat,cells_lon))
	data_aux_t = np.ones((cells_lat,cells_lon))
	data_aux_b = np.zeros((cells_lat,cells_lon))
	vec_ang = range(0, 360, angstep)

	for i in range(0,N):

		current_level = 0
		data_step = np.zeros((cells_lat,cells_lon))
		polygon = []
		height_eff = height_vector[i] + interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, lon_cen_vector[i], lat_cen_vector[i], cells_lon, cells_lat, Topography)
		polygon.append((lon_cen_vector[i], lat_cen_vector[i],  height_eff, 1.0 ))
		sum_pixels = 0
		hl_current = hl_vector[i]		

		for j in range(10000): 

			if(j == len(polygon)):
				if( N == 1 ):			
					data_cones = data_cones + data_step
				break
			if( cone_levels < polygon[j][3] ):
				if( N == 1 ):
					data_cones = data_cones + data_step
				break
			elif(current_level < polygon[j][3]):
				current_level = polygon[j][3]
				if( N == 1 ):
					data_cones = data_cones + data_step

			polygon_xy = []
			polygons_new = []

			for angle_deg in vec_ang:
				angle_rad = angle_deg * np.pi /180
				for distance in range(0, 100000, 10):
					h = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, polygon[j][0] + distance * cos(angle_rad) * step_lon_deg / step_lon_m , polygon[j][1] + distance*sin(angle_rad)*step_lat_deg/step_lat_m , cells_lon, cells_lat, Topography)
					if( h >= polygon[j][2] - hl_current * distance ):
						polygon_xy.append((int((polygon[j][0] + distance*cos(angle_rad)*step_lon_deg/step_lon_m - lon1) * cells_lon / (lon2 - lon1)),int((polygon[j][1] + distance*sin(angle_rad)*step_lat_deg/step_lat_m - lat1) * cells_lat / (lat2 - lat1))))
						polygons_new.append(distance)
						break

			img = Image.new('L', (cells_lon, cells_lat), 0)
			if( len(polygon_xy) > 0 ):
				draw = ImageDraw.Draw(img).polygon(polygon_xy, outline = 1 , fill = 1.0)
				data_step = np.maximum( np.minimum(data_aux_t, data_step + np.array(img)), data_aux_b)

			if( cone_levels > polygon[j][3] and sum(sum(data_step)) > sum_pixels + pix_min ):
				aux = np.zeros(len(polygons_new)+2) 
				aux[1:len(polygons_new)+1] = np.array(polygons_new) 
				aux[0] = polygons_new[len(polygons_new)-1]
				aux[len(polygons_new)+1] = polygons_new[0]
				der1 = (aux[1:len(aux)-1] - aux[2:len(aux)])
				der2 = (aux[1:len(aux)-1] - aux[0:len(aux)-2])
				wh1 = np.where(der1 >= 0)
				wh2 = np.where(der2 >= 0)
				wh_max = np.intersect1d(wh1[0], wh2[0])
				wh_grouped = np.split(wh_max, np.where(np.diff(wh_max) > 1)[0] + 1 )
				wh3 = np.where( abs(der1) + abs(der2) > 0)
				wh4 = np.intersect1d(wh_max, wh3[0])
				grouped_filter = np.zeros(len(wh_grouped))

				for x_grouped in range(len(wh_grouped)):
					if( len(np.intersect1d(wh_grouped[x_grouped],wh4)) > 0):
						grouped_filter[x_grouped] = 1

				if( (np.min(wh_grouped[0])) == 0 and (np.max(wh_grouped[len(wh_grouped)-1])) == len(polygons_new)-1 ):
					aux_grouped = np.concatenate((wh_grouped[len(wh_grouped)-1], wh_grouped[0] + len(polygons_new)))
					aux_filter = grouped_filter[len(wh_grouped)-1] + grouped_filter[0]
					wh_grouped = wh_grouped[1:-1]
					wh_grouped.append(aux_grouped)
					grouped_filter = np.append(grouped_filter[1:-1],aux_filter)

				wh_max = []
				for k in range(len(grouped_filter)):
					if(grouped_filter[k] > 0):
						if(np.mean(wh_grouped[k]) <= len(polygons_new) - 1.0):
							wh_max.append(np.mean(wh_grouped[k]))
						else:
							wh_max.append(len(polygons_new) - np.mean(wh_grouped[k]))

				wh_sum = np.zeros(len(polygons_new)) 

				if(len(wh_max) > 0):
					for l_max_real in wh_max:
						lmax = np.int(l_max_real)
						l_it = 	len(polygons_new) - 1		
						for l in range(1,len(polygons_new)):
							l_index = lmax + l
							if(l_index >= len(polygons_new)):
								l_index = l_index - len(polygons_new)
							if( polygons_new[lmax] < polygons_new[l_index] ):
								l_it = l
								break
							wh_sum[lmax] = wh_sum[lmax] + (polygons_new[lmax] - polygons_new[l_index])							
						for l in range(1,len(polygons_new) - l_it):
							l_index = lmax - l
							if(l_index < 0):
								l_index = l_index + len(polygons_new)
							if( polygons_new[lmax] < polygons_new[l_index] ):
								break							
							wh_sum[lmax] = wh_sum[lmax] + (polygons_new[lmax] - polygons_new[l_index])

					wh_sum = wh_sum * hl_current * angstep / 360

					for l in wh_max:
						lint = np.int(l)
						if( wh_sum[lint] > 0 ):
							new_x = polygon[j][0] + polygons_new[lint] * cos((vec_ang[lint] + angstep*(l-lint) ) * np.pi / 180 ) *step_lon_deg/step_lon_m ; 
							new_y = polygon[j][1] + polygons_new[lint] * sin((vec_ang[lint] + angstep*(l-lint) ) * np.pi / 180 ) *step_lat_deg/step_lat_m ;
							height_eff = wh_sum[lint] + interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, new_x, new_y, cells_lon, cells_lat, Topography)
							if(interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, new_x, new_y, cells_lon, cells_lat, Topography) < 99999):
								polygon.append(( new_x, new_y, height_eff, polygon[j][3] + 1 ))
			
			sum_pixels = sum(sum(data_step))	
			print j, len(polygon), polygon[j][3], polygon[j][2], sum(sum(data_step))

		if( N > 1 ):
			data_cones = data_cones + data_step

		print ' Simulation finished (N = ' + str(i+1) + ')'

if( source_dem == 2):

	data_cones = np.zeros((n_north,n_east))
	data_aux_t = np.ones((n_north,n_east))
	data_aux_b = np.zeros((n_north,n_east))
	vec_ang = range(0, 360, angstep)

	for i in range(0,N):

		current_level = 0
		data_step = np.zeros((n_north,n_east))
		polygon = []
		height_eff = height_vector[i] + interpol_pos(east_cor, north_cor, cellsize, cellsize, east_cen_vector[i], north_cen_vector[i], n_east, n_north, Topography)
		polygon.append((east_cen_vector[i], north_cen_vector[i],  height_eff, 1.0 ))
		sum_pixels = 0
		hl_current = hl_vector[i]

		for j in range(10000): 

			if(j == len(polygon)):
				if( N == 1 ):			
					data_cones = data_cones + data_step
				break
			if( cone_levels < polygon[j][3] ):
				if( N == 1 ):
					data_cones = data_cones + data_step
				break
			elif(current_level < polygon[j][3]):
				current_level = polygon[j][3]
				if( N == 1 ):
					data_cones = data_cones + data_step

			polygon_xy = []
			polygons_new = []

			for angle_deg in vec_ang:
				angle_rad = angle_deg * np.pi /180
				for distance in range(0, 100000, 10):
					h = interpol_pos(east_cor, north_cor, cellsize, cellsize, polygon[j][0] + distance * cos(angle_rad) , polygon[j][1] + distance*sin(angle_rad) , n_east, n_north, Topography)
					if( h >= polygon[j][2] - hl_current * distance ):
						polygon_xy.append((int((polygon[j][0] + distance* cos(angle_rad) - east_cor) * n_east / ( cellsize * ( n_east - 1 ) ) ), int((polygon[j][1] + distance*sin(angle_rad) - north_cor) * n_north / ( cellsize * ( n_north - 1 ) ))))
						polygons_new.append(distance)
						break

			img = Image.new('L', (n_east, n_north), 0)
			if( len(polygon_xy) > 0 ):
				draw = ImageDraw.Draw(img).polygon(polygon_xy, outline = 0 , fill = 1)
				data_step = np.maximum( np.minimum(data_aux_t, data_step + np.array(img)), data_aux_b)

			if( cone_levels > polygon[j][3] and sum(sum(data_step)) > sum_pixels + pix_min ):
				aux = np.zeros(len(polygons_new)+2) 
				aux[1:len(polygons_new)+1] = np.array(polygons_new) 
				aux[0] = polygons_new[len(polygons_new)-1]
				aux[len(polygons_new)+1] = polygons_new[0]
				der1 = (aux[1:len(aux)-1] - aux[2:len(aux)])
				der2 = (aux[1:len(aux)-1] - aux[0:len(aux)-2])
				wh1 = np.where(der1 >= 0)
				wh2 = np.where(der2 >= 0)
				wh_max = np.intersect1d(wh1[0], wh2[0])
				wh_grouped = np.split(wh_max, np.where(np.diff(wh_max) > 1)[0] + 1 )
				wh3 = np.where( abs(der1) + abs(der2) > 0)
				wh4 = np.intersect1d(wh_max, wh3[0])
				grouped_filter = np.zeros(len(wh_grouped))

				for x_grouped in range(len(wh_grouped)):
					if( len(np.intersect1d(wh_grouped[x_grouped],wh4)) > 0):
						grouped_filter[x_grouped] = 1

				if( (np.min(wh_grouped[0])) == 0 and (np.max(wh_grouped[len(wh_grouped)-1])) == len(polygons_new)-1 ):
					aux_grouped = np.concatenate((wh_grouped[len(wh_grouped)-1], wh_grouped[0] + len(polygons_new)))
					aux_filter = grouped_filter[len(wh_grouped)-1] + grouped_filter[0]
					wh_grouped = wh_grouped[1:-1]
					wh_grouped.append(aux_grouped)
					grouped_filter = np.append(grouped_filter[1:-1],aux_filter)

				wh_max = []
				for k in range(len(grouped_filter)):
					if(grouped_filter[k] > 0):
						if(np.mean(wh_grouped[k]) <= len(polygons_new) - 1.0):
							wh_max.append(np.mean(wh_grouped[k]))
						else:
							wh_max.append(len(polygons_new) - np.mean(wh_grouped[k]))

				wh_sum = np.zeros(len(polygons_new)) 
				if(len(wh_max) > 0):
					for l_max_real in wh_max:
						lmax = np.int(l_max_real)
						l_it = 	len(polygons_new) - 1		
						for l in range(1,len(polygons_new)):
							l_index = lmax + l
							if(l_index >= len(polygons_new)):
								l_index = l_index - len(polygons_new)
							if( polygons_new[lmax] < polygons_new[l_index] ):
								l_it = l
								break
							wh_sum[lmax] = wh_sum[lmax] + (polygons_new[lmax] - polygons_new[l_index])							
						for l in range(1,len(polygons_new) - l_it):
							l_index = lmax - l
							if(l_index < 0):
								l_index = l_index + len(polygons_new)
							if( polygons_new[lmax] < polygons_new[l_index] ):
								break							
							wh_sum[lmax] = wh_sum[lmax] + (polygons_new[lmax] - polygons_new[l_index])

					wh_sum = wh_sum * hl_current * angstep / 360

					for l in wh_max:
						lint = np.int(l)
						if( wh_sum[lint] > 0 ):
							new_x = polygon[j][0] + polygons_new[lint] * cos((vec_ang[lint] + angstep*(l-lint) ) * np.pi / 180 ) ; 
							new_y = polygon[j][1] + polygons_new[lint] * sin((vec_ang[lint] + angstep*(l-lint) ) * np.pi / 180 ) ;
							height_eff = wh_sum[lint] + interpol_pos(east_cor, north_cor, cellsize, cellsize, new_x, new_y, n_east, n_north, Topography)
							if(interpol_pos(east_cor, north_cor, cellsize, cellsize, new_x, new_y, n_east, n_north, Topography) < 99999):
								polygon.append(( new_x, new_y, height_eff, polygon[j][3] + 1 ))

			sum_pixels = sum(sum(data_step))	
			print j, len(polygon), polygon[j][3], polygon[j][2], sum(sum(data_step))

		if( N > 1 ):
			data_cones = data_cones + data_step

		print ' Simulation finished (N = ' + str(i+1) + ')'

# FIGURES

if(source_dem == 1):

	data_cones = data_cones[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ] / N
	plt.figure(1)
	cmapg = plt.cm.get_cmap('Greys')
	plt.contourf(matrix_lon,matrix_lat,Topography,100,cmap=cmapg,min=0)
	plt.colorbar()
	cmapr = plt.cm.get_cmap('Reds')
	if( N > 1 ):
		CS = plt.contourf(matrix_lon, matrix_lat, data_cones, 100, vmax = 1,  alpha= 0.6, interpolation='linear', cmap=cmapr, antialiased=True, lw=0.01)	
		fmt = '%.2f'
		plt.colorbar()
		CS_lines = plt.contour(matrix_lon,matrix_lat,data_cones, np.array([0.05, 0.5]), colors='k', interpolation='linear', lw=0.01)
		plt.clabel(CS_lines, inline=1, fontsize=10, colors='k', fmt=fmt)
	else:
		CS = plt.contourf(matrix_lon, matrix_lat, data_cones, 100, alpha= 0.6, interpolation='nearest', cmap=cmapr, antialiased=True, lw=0.01)
	plt.axes().set_aspect(step_lat_m/step_lon_m)
	plt.xlabel('Longitude $[^\circ]$')
	plt.ylabel('Latitude $[^\circ]$')
	plt.xlim(lon1, lon2 )
	plt.ylim(lat1, lat2 )

	for i in range(len(Cities)):
		plt.text(float(Cities[i][0]), float(Cities[i][1]), str(Cities[i][2]), horizontalalignment='center', verticalalignment='center', fontsize = 6)

	for i in range(0,N):
		plt.plot( lon_cen_vector[i], lat_cen_vector[i], 'r.', markersize=2)

	if( N == 1 ):
		for i in range(1,len(polygon)):
			plt.plot( polygon[i][0],polygon[i][1], 'b.', markersize=2)

	plt.savefig(run_name + '_map.png')

	if( N > 1 ):

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
	data_cones = data_cones[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ] / N
	plt.figure(1)
	cmapg = plt.cm.get_cmap('Greys')
	plt.contourf(matrix_east,matrix_north,Topography,100,cmap=cmapg,min=0)
	plt.colorbar()
	cmapr = plt.cm.get_cmap('Reds')
	if( N > 1 ):
		CS= plt.contourf(matrix_east,matrix_north,data_cones, 100, vmax = 1, alpha= 0.6,interpolation='linear',cmap=cmapr ,antialiased=True, lw=0.01)	
		fmt = '%.2f'
		CS.set_clim([0.0,1.0])
		plt.colorbar()
		CS_lines = plt.contour(matrix_east, matrix_north, data_cones, np.array([0.05, 0.5]), colors='k', interpolation='linear', lw=0.01)
		plt.clabel(CS_lines, inline=1, fontsize=10, colors='k', fmt=fmt)
	else:
		CS = plt.contourf(matrix_east,matrix_north,data_cones, 100, alpha= 0.6, interpolation='nearest', cmap=cmapr, antialiased=True, lw=0.01)	
	plt.axes().set_aspect(1.0)
	plt.xlabel('East [m]')
	plt.ylabel('North [m]')
	plt.xlim(east_cor, east_cor + cellsize * (n_east - 1) )
	plt.ylim(north_cor,north_cor +cellsize * (n_north - 1) )

	for i in range(0,N):
		plt.plot( east_cen_vector[i], north_cen_vector[i], 'r.', markersize = 2 )

	if( N == 1 ):
		for i in range(1,len(polygon)):
			plt.plot( polygon[i][0], polygon[i][1], 'b.', markersize = 2 )

	plt.savefig(run_name + '_map.png')

	if( N > 1 ):

		plt.figure(2)
		plt.subplot(121)
		plt.hist(height_vector)
		plt.xlabel('Initial height [m]')
		plt.subplot(122)
		plt.hist(hl_vector)
		plt.xlabel('H/L')
		plt.savefig(run_name + '_histogram.png')

	plt.show()
