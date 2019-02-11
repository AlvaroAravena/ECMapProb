clear all
close all

[probability, pathname_probability] = uigetfile( '*.vtk','Pick Probability File');
[topography, pathname_topography] = uigetfile( '*.vtk','Pick Topography File');
[collapse, pathname_collapse] = uigetfile( '*.txt','Pick Collapse Position');

file = strcat(pathname_probability, probability);
file_t = strcat(pathname_topography, topography);
file_c = strcat(pathname_collapse, collapse);
fileid = fopen(file);

while true
	aux = fgetl(fileid);
	if(aux == -1)
		break
	end
	aux_2 = strsplit(aux);
	if(strcmp(aux_2{1},'DIMENSIONS'))
		dimx = str2num(aux_2{2});
		dimy = str2num(aux_2{3});
	end
	if(strcmp(aux_2{1},'ORIGIN'))
		orix = str2num(aux_2{2});
		oriy = str2num(aux_2{3});
	end
	if(strcmp(aux_2{1},'SPACING'))
		spax = str2num(aux_2{2});
		spay = str2num(aux_2{3});
	end
	if(length(aux_2) > 4)
		D = str2num(aux);
	end	
end

fileid = fopen(file_t);
while true
	aux = fgetl(fileid);
	if(aux == -1)
		break
	end
	aux_2 = strsplit(aux);
	if(length(aux_2) > 4)
		T = str2num(aux);
	end	
end

fileid = fopen(file_c);
aux = fgetl(fileid);
aux_2 = strsplit(aux);
aspect_ratio = str2num(aux_2{2});
aux = fgetl(fileid);
boolean_l = 0;
if(aux(1) == 'L')
	boolean_l = 1;
end

counter = 1;
while true
	aux = fgetl(fileid);
	if(aux == -1)
		break
	end
	if(length(aux) > 1)
		collapse_data(counter,1:2) = str2num(aux);
		counter = counter + 1;
	end
end

Probability = reshape(D,[dimx, dimy]);
Topography = reshape(T,[dimx, dimy]);

x = orix:spax:orix+spax*(dimx-1);
y = oriy:spay:oriy+spay*(dimy-1);

[X,Y] = meshgrid(y,x);
pas = 1 + floor(dimx / 300);
select_x = 1:pas:dimx;
if( max(select_x) < dimx)
	select_x(length(select_x)+1) = dimx;
end

pas = 1 + floor(dimy / 300);
select_y = 1:pas:dimy;
if( max(select_y) < dimy)
	select_y(length(select_y)+1) = dimy;
end

[C,h] = contourf(Y(select_x,select_y),X(select_x,select_y),Topography(select_x,select_y),100, 'HandleVisibility','off');
colormap gray
set(h,'LineColor','none')
hold on;
plot(collapse_data(:,1),collapse_data(:,2),'b.', 'HandleVisibility','off');

if(boolean_l == 1)
	xlabel('Longitude [º]');
	ylabel('Longitude [º]');
else
	xlabel('East [m]');
	ylabel('North [m]');
end

colorbar;

val = [0.8, 0.4, 0.1];
contour(Y,X,Probability,[val(1),val(1)],'Color',[0.5 0 0]); hold on;
contour(Y,X,Probability,[val(2),val(2)],'Color',[1 0.0 0]); hold on;
contour(Y,X,Probability,[val(3),val(3)],'Color',[1 1 0]);
pbaspect([aspect_ratio 1.0 1.0]);

legend({['Probability: ' num2str(val(1))], ['Probability: ' num2str(val(2))], ['Probability: ' num2str(val(3))]});
