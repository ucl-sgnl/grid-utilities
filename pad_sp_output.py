#! /Library/Frameworks/Python.framework/Versions/Current/bin/python
# spiralPointPadding2.py
#
# This script is used to pad a domain of spiral points.
# Spiral points are uniformly distributed in S2 over a unit sphere and non-uniformly distributed in cartesian space.
# The cartesian domain {longitude x latitude} is obtained by interpolating the spiral points (datums) in the software packaged Surfer.
# The edges of the cartesian domain (longitude = +/- 180 degrees and latitude = +/- 90 degrees) are sparsely populated in S2.
# Spiral points are duplicated and converted to their equivalent locations for latitudes > 90 deg and < -90 deg, and for longitudes > 180 deg and <-180 deg.
# --------------------------------------------------
# The script may be supplied with filename arguments up front by invoking:
# python spiralPointPadding.py <input file> <output file>
# or interactively by invoking simply
# python spiralPointPadding.py
# and the user will be prompted for the filenames.  If an output filename exists in the current directory the option to overwrite will be given.
# --------------------------------------------------
# created November 1, 2012 - from spiralPointsPadding1.py
# updated November 6, 2012 - longitudes updated from [-180,180] to [-181,182] to accommodate bicubic interpolation.
# Shawn Allgeier - s.allgeier@ucl.ac.uk

paddingVersion = 2
if __name__ == '__main__':
	print 
	print "spiralPointPadding2.py -version %s" % paddingVersion
	print 
	print "This script is used to pad a domain of spiral points."
	print "Spiral points are uniformly distributed in S2 over a unit sphere and non-uniformly distributed in cartesian space."
	print "The cartesian domain {longitude x latitude} is obtained by interpolating the spiral points (datums) in the software packaged Surfer."
	print "The edges of the cartesian domain (longitude = +/- 180 degrees and latitude = +/- 90 degrees) are sparsely populated in S2."
	print "Spiral points are duplicated and converted to their equivalent locations for latitudes > 90 deg and < -90 deg, and for longitudes > 180 deg and <-180 deg."
	print "In addition the north and south pole values are replicated along many longitude values."
	print 
	print "The script may be supplied with filename arguments up front by invoking:"
	print "python spiralPointPadding.py <input file> <output file>"
	print "or interactively by invoking simply"
	print "python spiralPointPadding.py"
	print "and the user will be prompted for the filenames.  If an output filename exists in the current directory the option to overwrite will be given."
	print 
	print "created November 1, 2012 - version 1"
	print "Shawn Allgeier - s.allgeier@ucl.ac.uk"
	print 
	
	
# Command line argument provision
# --------------------------------------------------
import os # for directory information.
localFiles = os.listdir(os.getcwd()) # list of files in current working directory.
import sys # for input arguments.
arguments = sys.argv
nargs = len(sys.argv) # number or input arguments.  First argument is always the script name and is included in the count.  
if nargs < 3:
	print
	print "File argumets missing:"
	print "Usage: python spiralPointPadding.py <input file> <output file>"
	inputFile = raw_input('Enter input filename: ') # give user option to enter input file.
	while inputFile not in localFiles:
		print "Filename entered was not located in current directory."
		inputFile = raw_input('Enter input filename: ') # repeat until valid filename is entered.
	outputFile= raw_input('Enter output filename: ') # give user option to enter output file.
elif nargs == 3:
	inputFile = sys.argv[1] # spiral points data {latitude, longitude, x, y, z}
	outputFile = sys.argv[2] # text file to be created and padded {longitude, latitude, x, y, z}.
# This block should force the user to supply a valid input filename.

# Check for existing files
# --------------------------------------------------
if inputFile in localFiles:
	pass # source file is there, good on you!
else:
	while inputFile not in localFiles:
		print "Input file %s entered was not located in current directory." % inputFile
		inputFile = raw_input('Enter input filename: ') # repeat until valid filename is entered.
if outputFile in localFiles:
	print 
	outputOverwrite = raw_input('Output file already exists.  Overwrite: [(y)es/(n)o] ? ')
	if outputOverwrite == 'y' or outputOverwrite == 'yes':
		pass
	elif outputOverwrite == 'n' or outputOverwrite == 'no':
		outputFile = raw_input('Enter filename: ') # define new output filename.
	
	
	
	
# First parse input file data into a matrix.
# --------------------------------------------------
fin = open(inputFile, 'r')
print
# Count number of data records:
N = 0 # initialize counter.
dataStart = fin.tell() # cursor position of beginning of data.
for k in fin:
	N = N + 1
print '%s spiral points detected in %s.' % (N,inputFile)
sPoints = [] # initialize list variable.
# Parse data records:
fin.seek(dataStart) # return cursor to start of data.
for k in range(N):
	line = fin.readline() # one line of data as a string.
	lat = float(line.split(" ")[0]) # numerical version of latitude.
	lon = float(line.split(" ")[1]) # numerical version of longitude.
	x = line.split(" ")[2] # retain x,y,z values as strings.
	y = line.split(" ")[3]
	z = line.split(" ")[4]
	sPoints.append([lat,lon, x, y, z]) # store in list.
fin.close

	
# Write original spiral points to output file
# --------------------------------------------------
fout = open(outputFile,'w')
print
for k in range(N):
	#line = str(sPoints[k,0]) + ' ' + str(sPoints[k,1]) + ' ' + str(sPoints[k,2]) + ' ' + str(sPoints[k,3]) + ' ' + str(sPoints[k,4]) + '\n' 
	#fout.write('%.15f %.15f %1.15g %1.15g %1.15g\n' % (sPoints[k,0],sPoints[k,1],sPoints[k,2],sPoints[k,3],sPoints[k,4]))
	#fout.write(line)
	sLat = "%.15f" % sPoints[k][0] # string version of latitude.
	sLon = "%.15f" % sPoints[k][1] # string version of longitude.
	fout.write(sLat + ' ' + sLon + ' ' + sPoints[k][2] + ' ' + sPoints[k][3] + ' ' + sPoints[k][4] )	
fout.close
print "Original spiral points written to %s." % outputFile
	

# Top padding
# Padded values for latitude > 90 deg.
topPoints = []
for k in range(N):
	lat = sPoints[k][0]
	lon = sPoints[k][1]
	#topPoints[k][0] = 90.0 + (90.0 - lat) # assign new latitude.
	if lon >= 0.0:
		topPoints.append([90.0 + (90.0 - lat), lon - 180.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])		
	elif lon < 0.0:
		topPoints.append([90.0 + (90.0 - lat), lon + 180.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])
Ntop = len(topPoints)

# Bottom padding
# Padded values for latitude < 90 deg.
bottomPoints = []
for k in range(N):
	lat = sPoints[k][0]
	lon = sPoints[k][1]
	if lon >= 0.0:
		bottomPoints.append([-90.0 - (lat + 90.0), lon - 180.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])
	elif lon < 0.0:
		bottomPoints.append([-90.0 - (lat + 90.0), lon + 180.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])
Nbottom = len(bottomPoints)

# Left padding
# Padded values for longitude < 180 deg.
leftPoints = []
for k in range(N):
	lat = sPoints[k][0]
	lon = sPoints[k][1]
	leftPoints.append([lat, lon - 360.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])
Nleft = len(leftPoints)
	
# Right padding
# Padded values for longitude > 180 deg.
rightPoints = []
for k in range(N):
	lat = sPoints[k][0]
	lon = sPoints[k][1]
	rightPoints.append([lat, lon + 360.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])
Nright = len(rightPoints)


# Corner padding
# --------------------------------------------------
# North East padding
# Padded values for longitude > 180 and latitude > 0 deg. (NE)
nePoints = []
for k in range(N):
	lat = sPoints[k][0]
	lon = sPoints[k][1]
	if lon >= 0.0:
		nePoints.append([180.0 - lat, lon + 180.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])
Nne = len(nePoints)


# North West padding
# Padded values for longitude < 180 and latitude > 0 deg. (NW)
nwPoints = []
for k in range(N):
	lat = sPoints[k][0]
	lon = sPoints[k][1]
	if lon <= 0.0:
		nwPoints.append([180.0 - lat, lon - 180.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])
Nnw = len(nwPoints)



# South East padding
# Padded values for longitude > 180 and latitude < 0 deg. (SE)
sePoints = []
for k in range(N):
	lat = sPoints[k][0]
	lon = sPoints[k][1]
	if lon >= 0.0:
		sePoints.append([-1.0*lat - 180.0, lon + 180.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])
Nse = len(sePoints)


# South West padding
# Padded values for longitude < 180 and latitude < 0 deg. (SW)
swPoints = []
for k in range(N):
	lat = sPoints[k][0]
	lon = sPoints[k][1]
	if lon <= 0.0:
		swPoints.append([-1.0*lat - 180.0, lon - 180.0, sPoints[k][2], sPoints[k][3], sPoints[k][4] ])
Nsw = len(swPoints)



# Pole Replication
# --------------------------------------------------
# Insert north and south pole values at regularly spaced intervals in longitude.  
northGrid = [] # initialize north pole list.
southGrid = [] # initialize south pole list.
import scipy as sp
gridLongitude = sp.linspace(-181, 182, 364) # 1 degree spacing of longitude values.
for i in range(len(gridLongitude)):
	northGrid.append([sPoints[0][0], gridLongitude[i], sPoints[0][2], sPoints[0][3], sPoints[0][4] ])
	southGrid.append([sPoints[N-1][0], gridLongitude[i], sPoints[N-1][2], sPoints[N-1][3], sPoints[N-1][4] ])
Nnorth = len(northGrid)
Nsouth = len(southGrid)



# --------------------------------------------------
# Update output file
# --------------------------------------------------
print "Appending padded spiral points to %s." % outputFile

# Append top padded spiral points to output file.
fout = open(outputFile, 'a')
for k in range(Ntop):
	sLat = "%.15f" % topPoints[k][0] # string version of latitude.
	sLon = "%.15f" % topPoints[k][1] # string version of longitude.
	fout.write(sLat + ' ' + sLon + ' ' + topPoints[k][2] + ' ' + topPoints[k][3] + ' ' + topPoints[k][4] )	
fout.close
print "%s points written for top padding." % Ntop
	

# Append bottom padded spiral points to output file.
fout = open(outputFile, 'a')
for k in range(Nbottom):
	sLat = "%.15f" % bottomPoints[k][0] # string version of latitude.
	sLon = "%.15f" % bottomPoints[k][1] # string version of longitude.
	fout.write(sLat + ' ' + sLon + ' ' + bottomPoints[k][2] + ' ' + bottomPoints[k][3] + ' ' + bottomPoints[k][4] )	
fout.close
print "%s points written for bottom padding." % Nbottom


# Append left padded spiral points to output file.
fout = open(outputFile, 'a')
for k in range(Nleft):
	sLat = "%.15f" % leftPoints[k][0] # string version of latitude.
	sLon = "%.15f" % leftPoints[k][1] # string version of longitude.
	fout.write(sLat + ' ' + sLon + ' ' + leftPoints[k][2] + ' ' + leftPoints[k][3] + ' ' + leftPoints[k][4] )	
fout.close
print "%s points written for left padding." % Nleft


# Append right padded spiral points to output file.
fout = open(outputFile, 'a')
for k in range(Nright):
	sLat = "%.15f" % rightPoints[k][0] # string version of latitude.
	sLon = "%.15f" % rightPoints[k][1] # string version of longitude.
	fout.write(sLat + ' ' + sLon + ' ' + rightPoints[k][2] + ' ' + rightPoints[k][3] + ' ' + rightPoints[k][4] )	
fout.close
print "%s points written for right padding." % Nright



# Append northeast padded spiral points to output file.
fout = open(outputFile, 'a')
print
for k in range(Nne):
	sLat = "%.15f" % nePoints[k][0] # string version of latitude.
	sLon = "%.15f" % nePoints[k][1] # string version of longitude.
	fout.write(sLat + ' ' + sLon + ' ' + nePoints[k][2] + ' ' + nePoints[k][3] + ' ' + nePoints[k][4] )	
fout.close
print "%s points written for northeast padding." % Nne


# Append southeast padded spiral points to output file.
fout = open(outputFile, 'a')
for k in range(Nse):
	sLat = "%.15f" % sePoints[k][0] # string version of latitude.
	sLon = "%.15f" % sePoints[k][1] # string version of longitude.
	fout.write(sLat + ' ' + sLon + ' ' + sePoints[k][2] + ' ' + sePoints[k][3] + ' ' + sePoints[k][4] )	
fout.close
print "%s points written for southeast padding." % Nse


# Append northwest padded spiral points to output file.
fout = open(outputFile, 'a')
for k in range(Nnw):
	sLat = "%.15f" % nwPoints[k][0] # string version of latitude.
	sLon = "%.15f" % nwPoints[k][1] # string version of longitude.
	fout.write(sLat + ' ' + sLon + ' ' + nwPoints[k][2] + ' ' + nwPoints[k][3] + ' ' + nwPoints[k][4] )	
fout.close
print "%s points written for northwest padding." % Nnw


# Append southwest padded spiral points to output file.
fout = open(outputFile, 'a')
for k in range(Nsw):
	sLat = "%.15f" % swPoints[k][0] # string version of latitude.
	sLon = "%.15f" % swPoints[k][1] # string version of longitude.
	fout.write(sLat + ' ' + sLon + ' ' + swPoints[k][2] + ' ' + swPoints[k][3] + ' ' + swPoints[k][4] )	
fout.close
print "%s points written for southwest padding." % Nsw


# Append pole insertion points to output file.
fout = open(outputFile, 'a')
for k in range(Nnorth):
	sLat = "%.15f" % sPoints[0][0] # string verson of north pole.
	sLon = "%.15f" % gridLongitude[k]
	fout.write(sLat + ' ' + sLon + ' ' + northGrid[k][2] + ' ' + northGrid[k][3] + ' ' + northGrid[k][4] )
fout.close
print
print "%s points written for north pole padding." % Nnorth

fout = open(outputFile, 'a')
for k in range(Nsouth):
	sLat = "%.15f" % sPoints[N-1][0] # string verson of north pole.
	sLon = "%.15f" % gridLongitude[k]
	fout.write(sLat + ' ' + sLon + ' ' + southGrid[k][2] + ' ' + southGrid[k][3] + ' ' + southGrid[k][4] )
fout.close
print "%s points written for south pole padding." % Nsouth


print "--------------------------------------"
Ntotal = N + Ntop + Nbottom + Nleft + Nright + Nne + Nnw + Nse + Nsw + Nnorth + Nsouth
print "%s total spiral points." % Ntotal
# End of script.