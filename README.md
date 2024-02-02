# grid-utilities
Code used to resample the output of STC classic into a suitable grid format

How to generate the UCL radiation force model grid files using Surfer 10?
 
1. Requirements: Windows OS and the Surfer 10 Software (Windows-only)
 
2. Install Surfer 10 and add the directory where Scripter.exe is found (usually ~\Golden Software\Surfer 10\Scripter) to the PATH
 
3. Make sure the the spiral points files is padded. There is a script for doing this:
pad_sp_output.py
 
4. Run the command:
 
python createBasShepardMultiple.py spoints=C:\path to \spiralpoints.txt name=Mysatellite minquadratic=11 maxquadratic=50 minweight=11 maxweight=50 xnodes=361 ynodes=181 zcol=3
 
This command create a grid files. The name of the file starts with the satellite name that is specified. The default node resolution is 361 for x (longitude) and 181 for y (latitude). This is a 1x1 degree resolution.
 
zcol=3 means use the third column of the force model file (i.e. the third column of output form the spiral points based computation).
 
In this way, zcol=4 would use the y-component and zcol=5 would use the z-component.
 
4b.
 
python runBAS.py
 
5. After the grid files are generated there is an additional script to run: surfer6poleReplicate.py, this is to ensure that the values at the poles are the correct values.