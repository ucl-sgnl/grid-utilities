%% surfer6toMatlab.m
%
% Shawn Allgeier - s.allgeier@ucl.ac.uk
%
%% Summary:
% This function parses text data from grid files produced by Surfer and
% saved in the version 6 text format.
%
% Syntax is: [A, indices, bounds] = surfer6toMatlab(filename)
%
%% Inputs:
% The filename should be a string of a surfer6 text file.
%
%% Outputs:
% * A is the data matrix, with horizontal values lying in [xlo, xhi],
% vertical vaues in [ylo, yhi], and functional values in [zlo, zhi].  
% * indices is an optional second output argument to return [nx,ny], where
% nx is the numbe of horizontal grid lines and ny is the number of vertical
% grid lines.  
% * bounds is an optional third output argument to return [xlo, xhi; ylo,
% yhi; zlo, zhi]. 
%
%% Description:
% The Surfer6 text format for uniformly space grid files contains 5 headers
% lines:
%
% # The designation DSAA
% # The number of horizontal and vertical grid lines.
% # The minimum and maximum x values.
% # The minimum and maximum y values.
% # The minimum and maximum z values.
%
% The Surfer6 file format lists the z values only, in paragraphs, with each
% paragraph corresponding to one horizontal row.  The rows start at the
% bottom of the grid data, read from left to right, and proceed to the top
% row of the grid data as the file contents are read downwards.  This
% script determines the size of the grid data, and populates the matrix 'A'
% from bottom to top, so that the grid data is in the proper order, a Mercator orientation. 
%
% created October 9, 2012.
% updated December 10, 2012 - added comments.


function [A, indices, bounds] = surfer6toMatlab(filename)

fid = fopen(filename, 'r');
if not(fid == -1)
    %% Parse Header Information:
    fileDesignator = fgetl(fid); % line 1, should contain 'DSAA'.
    disp(' ')
    disp(['Parsing ', filename, '...'])
    disp(['File format is ', fileDesignator])
    
    gridDimensions = str2num(fgetl(fid)); % line 2, grid dimensions.   
    xRange = str2num(fgetl(fid)); % line 3, x bounds.
    yRange = str2num(fgetl(fid)); % line 4, y bounds.
    zRange = str2num(fgetl(fid)); % line 5, z bounds.
    
    nx = gridDimensions(1); % number of horizontal grid nodes.
    ny = gridDimensions(2); % number of vertical grid nodes.
    A = zeros(ny, nx); % initialize matrix for storage.

    xlo = xRange(1); % minimum x boundary.
    xhi = xRange(2); % maximum x boundary.
    ylo = yRange(1); % minimum y boundary.
    yhi = yRange(2); % maximum y boundary.
    zlo = zRange(1); % minimum z boundary.
    zhi = zRange(2); % maximum z boundary.
    
    disp(['Grid is ', num2str(ny), ' by ',num2str(nx),'.'])
    disp(['Horizontal values are in range [',num2str(xlo),',', num2str(xhi),'].'])
    disp(['Vertical values are in range [',num2str(ylo),',', num2str(yhi),'].'])
    disp(['Grid values are elements of [',num2str(zlo),',', num2str(zhi),'].'])
    
    dataStart = ftell(fid); % start of data paragraphs.

    %% Paragraph Test:
    dummy = fgetl(fid);
    k = 0;
    while not(strcmp(dummy,'') )
        k = k + 1;
        dummy = fgetl(fid); % read a line and check for content. 
    end % end while.
    pLines = k; % number of lines in a paragraph.
    disp(['Paragraphs consist of ', num2str(pLines), ' lines.'])    
    fseek(fid, dataStart, 'bof'); % return to start of data for parsing. 

    %% Data Parse:
    
    for k = 1 : ny % index for rows.
        lineString = ''; % intialize row string.
        for j = 1 : pLines
            piece = fgetl(fid); % read next line.
            lineString = cat(2, lineString, piece); % concatenate string together
        end % end for. 
        A(ny - k + 1, 1:nx) = str2num(lineString);
        fgetl(fid); % read blank line.
    end % end for. 

    %% Close Out:
    if fclose(fid)
        disp(['File ', filename, ' closed.'])
    end
else
    disp(['Error opening specified file ', filename])
end % end if.
    
if nargout > 1
    indices = [nx, ny]; % return grid dimensions.  
end

if nargout > 2
    bounds = [xlo, xhi; ylo, yhi; zlo, zhi]; % return ranges of values.
end
   
end % end of function.  


