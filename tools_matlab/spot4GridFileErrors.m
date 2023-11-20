%% GPSbestGrid.m
%
% Shawn Allgeier - s.allgeier@ucl.ac.uk
%
%% Summary:
% This script processes grid files for an acceleration component of SRP bus
% acceleration vector and compares them against results obtained from the
% UCL SRP/TRR software.  The gridding method used is Shepard's modified
% method (Surfer version 10 implementation).  The true values are EPS data
% points.  
%
%% Description:
% The two Shepard parameters varied are the number of quadratic neighbors
% and the weighting factor.  Grid files were generated using Surfer via
% Scripter automation, using Bas files written by the Python script
% createBasShepard.py. The quantites calculated for each grid file are
%
% # RMS error of residuals
% # Max error of residuals (absolute value)
% # Residuals
% # Bias of residuals (mean)
% # Standard deviation of residuals
%
% Five plots are produced and the metrics 1,2,4,5 above are saved to a CSV
% file.  
%
%% Variable Information:
% To use this script on another satelite or component the following items
% must be updated:
%
% # truth file of independent spiral points (prime or meridian).
% # grid file name prefix in error evaluation loop.
% # acceleration component {x,y,z} in error evaluation loop.
% # interpolation {bilinear,bicubic}.
% # CSV filename of results.
% # MAT filename of calculations.
% # Plot titles and labels. (this should be made to be autonomous based on
% one entry). 
%
%% Revision History:
% created January 14, 2013
% updated January 21, 2013
% updated January 30, 2013 - minor comments and save workspace to MAT file.
% updated January 31, 2013 - added histogram of best residuals.
% updated May 28, 2013 - added comments about which information changes
% from satellite to satellite.
% updated 13-Oct-2014 - made script generic for x,y,z components so that plots are automatically updated.

%% Initialization
clear
clc
fontsize = 12;
font = 'Times New Roman';
component = 'x';

%% Initialize Storage Matrices
neighbors = 8 : 50;
weights = 11 : 50;
Nneighbors = length(neighbors);
Nweights = length(weights);
N = Nneighbors * Nweights; % number of grid files.

xNodes = 361;
yNodes = 181;

rmsErrors = zeros(Nneighbors, Nweights);
maxErrors = zeros(Nneighbors, Nweights);
bias = zeros(Nneighbors, Nweights);
stdDev = zeros(Nneighbors, Nweights);

tableData = zeros(N,6);

%% Truth Data (EPS points):
truth = load('/Users/ucessbh/Dropbox/vm_win8_1/legion_files/galileo_foc_srp_trr_eps_1mm_3960.txt');
latitude = truth(:,1);
longitude = truth(:,2);
Nresiduals = length(truth); % generated from 3960 EPS parameter files.
residuals = zeros(Nresiduals, N);

%% Calculate Grid Metrics:

for i = 1 : Nneighbors % loop over quadratic neighbor values.
    for j = 1 : Nweights % loop over neighbor weighting values.
        gridFileName = cat(2,'S',component,'-R100-Q', num2str(i+neighbors(1)-1), 'W', num2str(j+weights(1)-1), 'S0.grd');
        disp(['Gridding ', gridFileName, ' ...'])
        [rmsErrors(i,j), maxErrors(i,j), scrap, bias(i,j), stdDev(i,j)] = gridError(gridFileName, truth, component, 'bilinear');
        residuals(1:Nresiduals, Nweights*(i-1) + j) = scrap(:,3);
        % store results in matrix for export to csv file.  
        tableData(Nweights*(i-1)+j, 1) = i + neighbors(1) - 1; % number of neighbors.
        tableData(Nweights*(i-1)+j, 2) = j + weights(1) - 1; % quadratic weights.
        tableData(Nweights*(i-1)+j, 3) = rmsErrors(i,j); % rms error for combination of neighbors and weights.
        tableData(Nweights*(i-1)+j, 4) = maxErrors(i,j); % max error for combination of neighbors and weights.
        tableData(Nweights*(i-1)+j, 5) = bias(i,j); % bias for combination of neighbors and weights.
        tableData(Nweights*(i-1)+j, 6) = stdDev(i,j); % std deviation for combination of neighbors and weights.  
        
    end
end

dlmwrite(cat(2,'Spot4Errors',component,'.csv'), tableData, ',') % write results to csv file.
% CSV file:
% A = neighbors
% B = weights
% C = rms
% D = max residual
% E = mean residual
% F = std dev of residuals
save(cat(2,'Spot4Errors',component,'Workspace.mat')) % save workspace.


%% Display Results:
disp(' ')
best = min(min(rmsErrors)); % lowest rms score.
disp(['Minimum RMS Error is ', num2str(best), ' ms-2'])
disp(['Minimum Max Error is ', num2str(min(min(maxErrors))), ' ms-2'])

[bestRow bestCol] = find(tableData == best);
disp(['Row ', num2str(bestRow) ' of tableData.'])
disp(['Best Grid file has ', num2str(tableData(bestRow,1)), ' neighbors and a weight of ', num2str(tableData(bestRow,2)), '.'])


%% Plots:
az = 34;
el = 8;
colormap jet

%% Plot RMS Errors:
figure(1)
clf
set(gcf, 'color' , 'white', 'Renderer', 'zbuffer')
surf(weights, neighbors, rmsErrors)
xlabel('Weights', 'FontSize', fontsize, 'FontName', font)
ylabel('Neighbors', 'FontSize', fontsize, 'FontName', font)
zlabel('RMS Error', 'FontSize', fontsize, 'FontName', font)
title(cat(2,'Satellite Bus ',component,' Component'), 'FontSize', fontsize, 'FontName', font)
set(gca, 'FontSize', fontsize, 'FontName', font)
set(gca, 'GridLineStyle', '-.')
grid on
view(az,el)


%% Plot Maximum Errors:
figure(2)
clf
set(gcf, 'color' , 'white', 'Renderer', 'zbuffer')
surf(weights, neighbors, maxErrors)
xlabel('Weights', 'FontSize', fontsize, 'FontName', font)
ylabel('Neighbors', 'FontSize', fontsize, 'FontName', font)
zlabel('Max Error', 'FontSize', fontsize, 'FontName', font)
title(cat(2,'Satellite Bus ',component,' Component'), 'FontSize', fontsize, 'FontName', font)
set(gca, 'FontSize', fontsize, 'FontName', font)
set(gca, 'GridLineStyle', '-.')
grid on
view(az,el)


%% Plot Residuals:
figure(3)
clf
set(gcf, 'color' , 'white', 'Renderer', 'zbuffer')
hold on
cmap = hsv(N);
 plot3(longitude, latitude, residuals(:,bestRow), 'o', 'color', cmap(i,:));
hold off
xlabel('Longitude (deg)', 'FontSize', fontsize, 'FontName', font)
ylabel('Latitude (deg)', 'FontSize', fontsize, 'FontName', font)
zlabel('Residuals (ms^{-2})', 'FontSize', fontsize, 'FontName', font)
set(gca, 'GridLineStyle', '-.')
grid on
view(-60,30)


%% Plot Bias:
figure(4)
clf
set(gcf, 'color' , 'white', 'Renderer', 'zbuffer')
surf(weights, neighbors, bias)
xlabel('Weights', 'FontSize', fontsize, 'FontName', font)
ylabel('Neighbors', 'FontSize', fontsize, 'FontName', font)
zlabel('Bias (ms^{-2})', 'FontSize', fontsize, 'FontName', font)
title(cat(2,'Satellite Bus ',component,' Component'), 'FontSize', fontsize, 'FontName', font)
set(gca, 'FontSize', fontsize, 'FontName', font)
set(gca, 'GridLineStyle', '-.')
grid on
view(az,el)


%% Plot Standard Deviation:
figure(5)
clf
set(gcf, 'color' , 'white', 'Renderer', 'zbuffer')
surf(weights, neighbors, stdDev)
xlabel('Weights', 'FontSize', fontsize, 'FontName', font)
ylabel('Neighbors', 'FontSize', fontsize, 'FontName', font)
zlabel('Std. Dev.', 'FontSize', fontsize, 'FontName', font)
title(cat(2,'Satellite Bus ',component, ' Component'), 'FontSize', fontsize, 'FontName', font)
set(gca, 'FontSize', fontsize, 'FontName', font)
set(gca, 'GridLineStyle', '-.')
grid on
view(az,el)

%% Histogram of Residuals:
figure(5)
clf
set(gcf, 'color' , 'white', 'Renderer', 'zbuffer')
hold on
bestHist = hist(residuals(:,bestRow),100);
hist(residuals(:,bestRow),100)
line([tableData(bestRow,5) tableData(bestRow,5)], [0 max(bestHist)], 'color' ,'red')
hold off
set(gca, 'FontSize', fontsize, 'FontName', font)
set(gca, 'GridLineStyle', '-.')
grid on
xlabel('Acceleration Residuals (ms-2)', 'FontSize', fontsize, 'FontName', font)
ylabel(cat(2,'Satellite Bus ',component,' Component'), 'FontSize', fontsize, 'FontName', font)



