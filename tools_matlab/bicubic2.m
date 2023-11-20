%% bicubic2.m
%
% Shawn Allgeier - shawn@periselenium.org
%
%% Summary:
% bicubic2.m performs bicubic interpolation on a matrix to obtain the
% value of the function approximated by gridded data.  The location to be
% interpolated to must lie within the extents of the matrix. 
% 
% Syntax is: f = bicubic2(x,y, grid, dimensions, range)
%
%% Inputs:
%
% * x: horizontal coordinate in real units.
% 
% * y: vertical coordinate in real units.
%
% * grid: an nxm matrix of grid values.
%
% * dimensions: a 1x2 matrix containing [n,m], where [n,m] = size(grid).
%
% * range: a 2x2 matrix defining the extents of the horizontal and vertical
% directions:
%
% # range(1,1) = minimum x-value.
% # range(1,2) = maximum x-value.
% # range(2,1) = minimum y-value.
% # range(2,2) = maximum y-value.
%
%% Output:
% f: the interpolated value f(x,y) approximating the function generating
% the values in the matrix 'grid'.  
%
%% Description:
% The grid matrix is assumed to represent a rectangular region of uniformly
% spaced samples of an unknown function or surface.  The column position
% indicates a node between [xmin, xmax] and the row position indicates a
% node between [ymin ymax], so that the row index corresponds to increasing
% y-values.  
%
% The bicubic interpolation is performed by fitting a cubic function over
% the area bounded by the four nearest neighbors to the interpolated point.
% The cubic function f(x,y) is 
%%
% 
% $$f(x,y) = \displaystyle\sum_{i=0}^{3}\sum_{j=0}^{3}c_{ij}t^{j}u^{i},$$
% 
% where
% 
% $$\begin{array}{rl} t =& \displaystyle\frac{x-x_j}{x_{j+1}-x_j}\\ u
% =&\displaystyle\frac{y-y_i}{y_{i+1}-y_i}\end{array}$$
%
%
% The quantities $t,u\in[0,1]$ are the horizontal and vertical distances of
% the interpolation point from the upper left neighbor. 
%
% The desired position is used with the grid extents and number of nodes to
% determine the upper left neighbor $(i,j)$, which is one x-value and one y-value 
% less than $(x,y)$ respectively.  The interpolated point is surrounded by
% four nearest neighbors, the values of which are used in the determination
% of the coefficients. The derivatives in the horizontal and vertical 
% directions are estimated using center finite differences.  The second
% order mixed derivative %\frac{\partia^2 f}{\partial x\partialy}$ for a
% given point are estimated using its diagonal neighbors.  As a result of
% these derivative estimates, the valid domain for interpolation is
% asymmetric.  The left boundary is one column in from the left edge of the
% grid (inclusive).  The right boundary is one column in from the right
% edge of the grid (exclusive).  The top boundary is one row down from the
% edge of the grid (inclusive).  The bottom boundary is one row up from the
% edge of the grid (exclusive).  The horizonta, vertical, and mixed
% derivatives are calculated for the four neighbors and a linear system of
% 16 equations is solved for the cubic function coefficients $c_{ij}$ which
% are then used to evaluate $f$ at the interpolation point $(x,y)$.  
%
% The algorithm is equivalent to that given in
% <html>Press, W. H., Teukolsky, S. A., Vetterling, W. T., and Flannery, B. P., <u>Numerical Recipes</u>, Cambidge University Press, New York, 2007.</html>
%
% Note: This algorithm expects the rows of the grid to correspond to
% increasing y-values.  If a grid M is populated so that it is appropriate
% for use in the function surf(M), then M may be supplied
% as the grid argument.
%
% created November 6, 2012.




function f = bicubic2(x,y, grid, dimensions, range)
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
vraw = ( ((y - ymin) / deltaY) + 1); % raw vertical index (downward = increasing y-values).

% upper left
i1 = fix(vraw);
j1 = fix(hraw);
% upper right
i2 = i1;
j2 = j1+1;
% lower left
i3 = i1+1;
j3 = j1;
% lower right
i4 = i1+1;
j4 = j1+1;

xrange = linspace(xmin, xmax, m);
yrange = linspace(ymin, ymax, n);

% Desired point is (t,u) from (x(j),y(i))
t = (x - xrange(j1)) / (xrange(j1+1) - xrange(j1));
u = (y - yrange(i1)) / (yrange(i1+1) - yrange(i1));
% disp(['t = ', num2str(t), '  u = ', num2str(u)])
% disp(['i = ', num2str(i1), '  j = ', num2str(j1)])


%% Retrieve function values at inner nodes:
f1 = grid(i1,j1); % upper left.
f2 = grid(i2,j2); % upper right.
f3 = grid(i3,j3); % lower left.
f4 = grid(i4,j4); % lower right.


%% Calculate Horizontal Derivatives
% Center finite differences
fx1 = (grid(i1,j1+1) - grid(i1,j1-1)) / (2*deltaX);
fx2 = (grid(i2,j2+1) - grid(i2,j2-1)) / (2*deltaX);
fx3 = (grid(i3,j3+1) - grid(i3,j3-1)) / (2*deltaX);
fx4 = (grid(i4,j4+1) - grid(i4,j4-1)) / (2*deltaX);

%% Calculate Vertical Derivatives
% Center finite differences
fy1 = (grid(i1+1,j1) - grid(i1-1,j1)) / (2*deltaY);
fy2 = (grid(i2+1,j2) - grid(i2-1,j2)) / (2*deltaY);
fy3 = (grid(i3+1,j3) - grid(i3-1,j3)) / (2*deltaY);
fy4 = (grid(i4+1,j4) - grid(i4-1,j4)) / (2*deltaY);

%% Calculate Mixed Derivatives
% Use diagonal center finite differences
fxy1 = (grid(i1-1,j1+1) - grid(i1+1,j1+1) - grid(i1-1,j1-1) + grid(i1+1,j1-1) ) / ( (xrange(j1+1) - xrange(j1-1))*(yrange(i1+1) - yrange(i1-1)) );
fxy2 = (grid(i2-1,j2+1) - grid(i2+1,j2+1) - grid(i2-1,j2-1) + grid(i2+1,j2-1) ) / ( (xrange(j2+1) - xrange(j2-1))*(yrange(i2+1) - yrange(i2-1)) );
fxy3 = (grid(i3-1,j3+1) - grid(i3+1,j3+1) - grid(i3-1,j3-1) + grid(i3+1,j3-1) ) / ( (xrange(j3+1) - xrange(j3-1))*(yrange(i3+1) - yrange(i3-1)) );
fxy4 = (grid(i4-1,j4+1) - grid(i4+1,j4+1) - grid(i4-1,j4-1) + grid(i4+1,j4-1) ) / ( (xrange(j4+1) - xrange(j4-1))*(yrange(i4+1) - yrange(i4-1)) );


%% Formulate System of Equations
b = [f1;f2;f3;f4;
    fx1*(xrange(j1+1) - xrange(j1));
    fx2*(xrange(j2+1) - xrange(j2));
    fx3*(xrange(j3+1) - xrange(j3));
    fx4*(xrange(j4+1) - xrange(j4));
    fy1*(yrange(i1+1) - yrange(i1));
    fy2*(yrange(i2+1) - yrange(i2));
    fy3*(yrange(i3+1) - yrange(i3));
    fy4*(yrange(i4+1) - yrange(i4));
    fxy1*(xrange(j1+1) - xrange(j1))*(yrange(i1+1) - yrange(i1));
    fxy2*(xrange(j2+1) - xrange(j2))*(yrange(i2+1) - yrange(i2));
    fxy3*(xrange(j3+1) - xrange(j3))*(yrange(i3+1) - yrange(i3));
    fxy4*(xrange(j4+1) - xrange(j4))*(yrange(i4+1) - yrange(i4))];
    
 
% A = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
%     1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
%     1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0;
%     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1;
%     0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
%     0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
%     0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0;
%     0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3;
%     0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
%     0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0;
%     0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0;
%     0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3;
%     0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
%     0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0;
%     0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0;
%     0, 0, 0, 0, 0, 1, 2, 3, 0, 2, 4, 6, 0, 3, 6, 9];
% Ainv = inv(A);

% Inverse of bicubic equation for coefficients is precomputed for speed. 
Ainv = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    -3, 3, 0, 0, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    2, -2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, 0, -2, -1, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, 2, -2, 0, 0, 1, 1, 0, 0;
    
    -3, 0, 3, 0, 0, 0, 0, 0, -2, 0, -1, 0, 0, 0, 0, 0;
    0, 0, 0, 0, -1, 0, 1, 0, -2, 2, 0, 0, -2, -2/3, -1/3, 0;
    9, -9, -9, 9, 2, 3, -2, -3, 10, -10, 3, -3, 4, 10/3, 2/3, 1;
    -6, 6, 6, -6, -1, -3, 1, 3, -6, 6, -2, 2, -2, -8/3, -1/3, -1;
    
    2, 0, -2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, 2, -2, 0 , 0, 1, 2/3, 1/3, 0;
    -6, 6, 6, -6, 0, -2, 0, 2, -7, 7, -3, 3, -2, -7/3, -2/3, -1;
    4, -4, -4, 4, 0, 2, 0, -2, 4, -4, 2, -2, 1, 5/3, 1/3, 1];

beta = Ainv*b; % polynomial coefficients.  

%% Evaluate Bicubic Function 
f = beta(1) + beta(2)*t + beta(3)*t^2 + beta(4)*t^3 + ...
    beta(5)*u + beta(6)*u*t + beta(7)*u*t^2 + beta(8)*u*t^3 + ...
    beta(9)*u^2 + beta(10)*u^2*t + beta(11)*u^2*t^2 + beta(12)*u^2*t^3 + ...
    beta(13)*u^3 + beta(14)*u^3*t + beta(15)*u^3*t^2 + beta(16)*u^3*t^3;

end % End of Function.




