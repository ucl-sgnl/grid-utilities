%% gridError.m
%
% Shawn Allgeier - s.allgeier@ucl.ac.uk
%
%% Summary:
% This function quantifies the interpolation error of a grid file produced
% from a spiral points data file. 
%
% Syntax is: [rmsError, maxError, Errors, bias, stDev] = gridError(gridFile, spiralPoints, component, algorithm, plotFlag, figNumbers)
%
%% Inputs:
% 
% * gridFile = a string containing a valid grid file in text format (Surfer version 6).
% * spiralPoints = a string containing a valid text file of spiral points data. 
% * spiralPoints = a matrix containing [latitude, longitude, x, y, z]
% spiral points data.  This overloaded input argument is more efficient
% when the spiral points file is used to quantify the error for multiple
% grids.  
% * component = a string, either 'x', 'y', or 'z' to indicate which component (or surface) of the spiral points data is to be analyzed.
% * algorithm = a string, either 'bilienar' or 'bicubic' to indicate which interpolation method is to be used on the grid file.  
% * plotFlag = a flag, if set to 1 then the histogram, residuals, and percent error are
% plotted.
% * figNumbers = a three element matrix (optional argument) to open specific
% figure numbers. If plotFlag = 1 and no argument for figNumbers is supplied
% then new figures are created.  
%
%% Outputs:
% 
% * rmsError = the root, mean, squared error of difference between sprial point value and the interpolated grid value.  
% * maxError = the maximum value of the absolute value of the difference between spiral point value and the interpolated grid value.
% * Errors = an Nx3 matrix of {latitude, longitude, error}, where error is
% the difference between the true value minus the interpolated value. 
% * bias = the mean of the interpolated errors.
% * stDev = the standard deviation of the interpolated errors.
%
% In addition, three plots are generated.  One is a histogram of the errors.  
% The second is a plot of the interpolation residuals as a function of longitude and latitude. 
% The third is the percent error at each interpolation point.
%
%% Description:
% This function accepts a text based grid file in the Surfer6 format of
% uniformly spaced data and a text based data file of spiral points.  
% The grid is interpolated using either bilinear or bicubic interpolation
% to find the values at the locations of the spiral points.  The
% differences are taken and the root mean square(RMS) of the differenes are
% calculated, as well as the maximum of the absolute value of the
% differenes.  Each grid file is for an acceleration component and a spiral
% points file contains points for all three comonents.  The component input
% argument indicates which column of the spiral points file is being
% compared with the interpolated grid file.  
%
% created October 24, 2012.
%
% updated October 26, 2012.
% updated October 30, 2012.
% updated November 6, 2012 (added bias and std. dev.).
% updated November 7, 2012 (annotated figures).
% updated December 10, 2012 (overloaded to allow matrix of correct datums
% to be pased in instead of character string for text file parsing. 
% updated December 13, 2012 (percent error plot annotation).

function [rmsError, maxError, Errors, bias, stDev] = gridError(gridFile, spiralPoints, component, algorithm, plotFlag, figNumbers)

%% Load Spiral Points Data:
if ischar(spiralPoints) % parse text file of datums.
    SP = SPtoMatlab(spiralPoints); % parse spiral points text file. 
    N = length(SP); % number of spiral points. 
    latitude = SP(:,1);
    longitude = SP(:,2);
elseif strcmp(class(spiralPoints),'double') % matrix passed in, no need to parse.
    SP = spiralPoints;
    N = length(SP); % number of spiral points. 
    latitude = SP(:,1);
    longitude = SP(:,2);    
end
    
    
%% Load Gridded Data:
[G, indices, bounds] = surfer6toMatlab(gridFile); % parse Surfer6 ascii grid file.
% G is a matrix of grid node values, where columns correspond to
% (increasing) longitude and rows correspond to (decreasing) latitude, as
% in a Mercator projection.
n = indices(2);
m = indices(1);

leftLimit = bounds(1,1);
rightLimit = bounds(1,2);
lowerLimit = bounds(2,1);
upperLimit = bounds(2,2);


%% Interpolate Grid Data to Spiral Point Locations:
interpPoints = zeros(N,3);
interpPoints(:,1) = latitude;
interpPoints(:,2) = longitude;


if strcmp(algorithm, 'bilinear') || strcmp(algorithm, 'Bilinear')    
    disp('Bilinear interpolation')
    for i = 1 : N
        interpPoints(i,3) = bilinear1(longitude(i), latitude(i), G, [n m], [leftLimit, rightLimit;lowerLimit, upperLimit]);
    end            
end % end of bilinear.


if strcmp(algorithm, 'bicubic') || strcmp(algorithm, 'Bicubic')
    disp('Bicubic interpolation')
    Gud = flipud(G); % flip grid matrix upside down for bicubic interpolation.
%     x = linspace(leftLimit, rightLimit, m);
%     y = linspace(lowerLimit, upperLimit, n);
%     [X,Y] = meshgrid(x,y);
    % This is not the most efficient implementation of Matlab's 2D
    % interpolation, but the desired interpolation points are not uniformly
    % spaced, so the function must be invoked one point at a time.  
    for i = 1 : N
%         interpPoints(i,3) = interp2(X,Y,flipud(G), longitude(i), latitude(i), 'cubic');
        interpPoints(i,3) = bicubic2(longitude(i), latitude(i), Gud, [n m], [leftLimit, rightLimit;lowerLimit, upperLimit]);
    end
end % end of bicubic.

    
%% Calculate Error Metrics:

if strcmp(component, 'X') % compare with column 3 of SP.
    interpError = SP(:,3) - interpPoints(:,3); % residuals.
    percentError = interpError ./ SP(:,3);
end % end x interpolation.
    
if strcmp(component, 'Y') % compare with column 4 of SP.
    interpError = SP(:,4) - interpPoints(:,3); % residuals.
    percentError = interpError ./ SP(:,4);
end % end y interpolation.

if strcmp(component, 'Z') % compare with column 5 of SP.
    interpError = SP(:,5) - interpPoints(:,3); % residuals.
    percentError = interpError ./ SP(:,5);
end % end z interpolation.
    
rmsError = sqrt(sum(interpError.^2) / N);
maxError = max(abs(interpError));
Errors = cat(2, latitude, longitude, interpError); 
bias = mean(interpError);
stDev = std(interpError);




%% Plots:

if nargin > 4
    if plotFlag == 1
        fontsize = 12;
        font = 'Times New Roman';
        az = -40;
        el = 30;

        %% Histogram:
        if nargin > 5
            figure(figNumbers(1))
        else
            figure
        end
        clf
        set(gcf, 'color' ,'white')
        hist(interpError, 100)
        xlabel([component, ' Residuals (ms^{-2})'], 'FontSize', fontsize, 'FontName', font)
        ylabel([num2str(N), ' Spiral Points'], 'FontSize', fontsize, 'FontName', font)
        title([algorithm, ' Interpolation'], 'FontSize', fontsize, 'FontName', font)
        set(gca, 'GridLineStyle', '-.')
        set(gca, 'FontSize', fontsize, 'FontName', font)
        text(0,1000,{['Bias = ', num2str(bias)];['Std Dev = ', num2str(stDev)];['Max Error = ', num2str(maxError)]}, 'FontSize', fontsize, 'FontName', font, 'BackGroundColor', 'white')
        grid on

        %% Error Cloud:
        if nargin > 5
            figure(figNumbers(2))
        else
            figure
        end
        clf
        set(gcf, 'color', 'white')
        plot3(longitude, latitude, interpError, 'o')
        set(gca, 'FontSize', fontsize, 'FontName', font)
        set(gca, 'GridLineStyle', '-.')
        grid on
        xlabel('Longitude (deg)', 'FontSize', fontsize, 'FontName', font)
        ylabel('Latitude (deg)', 'FontSize', fontsize, 'FontName', font)
        zlabel('Residuals (ms^{-2})', 'FontSize', fontsize, 'FontName', font)
%         set(legend(component), 'FontSize', fontsize, 'FontName', font)
        title({[component, ' ', algorithm, ' Interpolation Error'];['RMS Error = ', num2str(rmsError)];['Max Error = ', num2str(maxError)]}, 'FontSize', fontsize, 'FontName', font)
        view(az,el)
        
        %% Percent Error Surface:
        if nargin > 5
            figure(figNumbers(3))
        else
            figure
        end
        clf
        set(gcf, 'color', 'white')
        plot3(longitude, latitude, percentError, 'o')
        set(gca, 'FontSize', fontsize, 'FontName', font)
        set(gca, 'GridLineStyle', '-.')
        grid on
        xlabel('Longitude (deg)', 'FontSize', fontsize, 'FontName', font)
        ylabel('Latitude (deg)', 'FontSize', fontsize, 'FontName', font)
        zlabel('Percent Error', 'FontSize', fontsize, 'FontName', font)
        title({[component, ' ', algorithm, ' Percent Error'];['RMS Error = ', num2str(rmsError)];['Max Error = ', num2str(maxError)]}, 'FontSize', fontsize, 'FontName', font)
        view(az,el)
    end
end

end % end of function.  




