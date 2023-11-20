%% SPtoMatlab.m
%
% Shawn Allgeier - s.allgeier@ucl.ac.uk
%
%% Summary:
% This function parses a text file of spiral points and loads the data into a matrix.
%
% Syntax is: sPoints = SPtoMatlab(filename)
%
%% Input:
% filename is a string of a valid file containing spiral points data from the UCL SRP/TRR software. 
% The expected format is {latitude longitude acc_X acc_Y acc_Z} with a single space as the field separator, and no header line.
%
%% Output:
% sPoints is an Nx5 matrix, where N is the number of lines in the text file.
%
%% Description:
% The text file of spiral points is expected to have been generated on the Condor cluster. 
% The returned data files are processed, sorted, and appended together using various BASH scripts.
% This function makes the data readily accessible in Matlab.  
%
% created October 24, 2012.
% updated December 10, 2012 - added comments. 


function sPoints = SPtoMatlab(filename)
%% Access File:
fid = fopen(filename, 'r');
if not(fid == -1)
    
    %% Determine Size of Data:
    k = 0;
    while not(feof(fid))
        fgetl(fid);
        k = k + 1;
    end
    N = k;
    sPoints = zeros(N,5); % initialize matrix.  
    
    %% Data Parse:
    frewind(fid); % return to start for reading data.
    for i = 1 : N
        tline = str2num(fgetl(fid)); % read a line.
        sPoints(i, :) = tline; % data separated by space is easily read as a row matrix and assigned to sPoints matrix.
    end
    
    %% Close Out:
    if fclose(fid)
        disp(['File ', filename, ' closed.'])
    end
    
else
    disp(['Error opening specified file ', filename])
    sPoints = NaN; % return value when file cannot be opened. 
end % end if.

end % end of function.  

