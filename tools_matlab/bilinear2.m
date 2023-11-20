%% bilinear2.m
%
% Shawn Allgeier - s.allgeier@ucl.ac.uk
%
%% Summary:
% bilinear2.m performs bilinear interpolation on a matrix to obtain the
% value of the function approximated by gridded data.  The location to be
% interpolated to must lie within the extents of the matrix. 
% 
% Syntax is: z = bilinear2(x,y, grid, dimensions, range)
%
%% Inputs:
%
% x: horizontal coordinate in real units.
% 
% y: vertical coordinate in real units.
%
% grid: an nxm matrix of grid values.
%
% dimensions: a 1x2 matrix containing [n,m], where [n,m]=size(grid).
%
% range: a 2x2 matrix defining the extents of the horizontal and vertical
%
% directions:
%
% # range(1,1) = minimum x-value.
% # range(1,2) = maximum x-value.
% # range(2,1) = minimum y-value.
% # range(2,2) = maximum y-value.
%
%% Output:
% z: the interpolated value f(x,y) approximating the function generating
% the values in the matrix 'grid'.  
%
%% Description:
% The grid matrix is assumed to represent a rectangular region of uniformly
% spaced samples of an unknown function or surface.  The column position
% indicates a node between [xmin, xmax] and the row position indicates a
% node between [ymin ymax], so that the row index corresponds to increasing
% y-values.  
%
% The desired position is used with the grid extents and number of nodes to
% determine the four nearest neighbors.  If the point falls on a grid line,
% then 1d interpolation is performed, in either the horizontal or vertical
% direction, as appropriate.  If the desired position falls directly on a
% node, then the grid value is returned.  In general the desired position
% will have four neighbors, and the grid values at these neighboring points
% are used to estimate a value at the desired point.  Horizontal
% interpolation (left to right) is performed along the grid lines below and above the
% desired point.  Then vertical interpolation (downward) is performed between
% the two horizontal points to obtain the estimate.  
%
% Note: This algorithm expects the rows of the grid to correspond to
% increasing y-values.  If a grid M is populated so that it is appropriate
% for use in the function surf(M), then M may be supplied
% as the grid argument, in contrast with the function bilinear1.m.
%
%
% created October 17, 2012



function z = bilinear2(x,y, grid, dimensions, range)
%% Dimensions of Gridded Data:
n = dimensions(1); % number of grid nodes in vertical (y) direction.
m = dimensions(2); % number of grid nodes in horizontal (x) direction.
%% Range of Gridded Data:
xmin = range(1,1); % minimum x value.
xmax = range(1,2); % maximum x value.
ymin = range(2,1); % minimum y value.
ymax = range(2,2); % maximum y value.
%% Grid Spacing:
deltaX = (xmax - xmin) / (m-1); % horizontal spacing.
deltaY = (ymax - ymin) / (n-1); % vertical spacing.

%% Indices:
hraw = ( (x - xmin) / deltaX) + 1; % raw horizontal index (rightward = increasing x-values).
vraw = ( (y - ymin) / deltaY) + 1; % raw vertical index (downward = increasing y-values).

%% Select Interpolation (exact, horizontal, vertical, four point)
if (rem(hraw,1) == 0) && (rem(vraw,1)) == 0
    z = grid(vraw, hraw); % use grid point.
%     disp(['both (',num2str(vraw),',',num2str(hraw),')'])
elseif rem(vraw,1) == 0 % point falls on horizontal grid line.
    % 1D horizontal interpolation
    j1 = fix(hraw); % smaller index (closer to left of array).
    j2 = j1 + 1; % larger index (closer to right of array).
    x1 = xmin + (j1-1)*deltaX; % left neighbor.
    x2 = xmin + (j2-1)*deltaX; % right neighbor.
    f1 = grid(vraw,j1);
    f2 = grid(vraw,j2);
    z = ( (f2 - f1)/(x2-x1) )*(x-x1) + f1; % 1d rightward interpolation.
%     disp(['horizontal interp (',num2str(vraw),':',num2str(j1),',',num2str(j2),')'])
elseif rem(hraw,1) == 0 % point falls on vertical grid line.
    % 1D vertical interpolation
    i1 = fix(vraw); % smaller index (closer to top of array).
    i2 = i1 + 1; % larger index (closer to bottom of array).
    y1 = ymin + (i1-1)*deltaY; % upper neighbor.
    y2 = ymin + (i2-1)*deltaY; % lower neighbor.
    f1 = grid(i1,hraw);
    f2 = grid(i2,hraw);
    z = ( (f2 - f1)/(y2-y1) )*(y-y1) + f1; % 1d downward interpolation.
%     disp(['vertical interp (',num2str(i1),',',num2str(i2),':',num2str(hraw),')'])
else % 4point bilinear interpolation
%     disp('4-point')
    % Horizontal indices and values
    j1 = fix(hraw); % left index.
    j2 = j1 + 1; % right index.
    x1 = xmin + (j1-1)*deltaX; 
    x2 = xmin + (j2-1)*deltaX;
    % Vertical indices and values
    i1 = fix(vraw); % lower index (smaller y-value, higher in matrix).
    i2 = i1 + 1; % higher index (greater y-value, lower in matrix).
    y1 = ymin + (i1-1)*deltaY;
    y2 = ymin + (i2-1)*deltaY;
    % Corner values
    fll = grid(i2,j1); % lower left value.
    flr = grid(i2,j2); % lower right value.
    ful = grid(i1,j1); % upper left value.
    fur = grid(i1,j2); % upper right value.
    % Linear interpolations
    R2 = ( (flr - fll)/(x2 - x1) )*(x - x1) + fll; % horizontal interpolation along lower border.
    R1 = ( (fur - ful)/(x2 - x1) )*(x - x1) + ful; % horizontal interpolation along upper border.
    z = ( (R2 - R1)/(y2 - y1) )*(y - y1) + R1; % vertical interpolation (downward) in middle of rectangle.
end % end if

end % end of function.
    
    



