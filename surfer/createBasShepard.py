#! /bin/bash
# createBasShepard.py
#
# This script is used to generate BAS files for use in Scripter to produce grid files using modified Shepard's method in Surfer. 
# The script accepts command line arguments to set gridding parameters.  The resulting binary grid file is then converted to the Surfer6 ascii text format.
# Usage: python createBasShepard.py <keyword=value> ...
# A list of keywords can be obtained by invoking this script without any input arguments.  
# Gridding parameters revert to a default set in the event if not specified by the user.  The default values are listed when the script is called without any input arguments.  
# The BAS and resulting grid filenames are automatically generated from the gridding parameters.  
# The location (absolute file path) of a datums file must be supplied.  
# Note: The scripts 'createBasShepardSingle.py' and 'createBasShepardMultiple.py' make use of this script. 
#
# 
# updated January 29, 2013 - Shawn Allgeier

import os # for directory information.
#localFiles = os.listdir(os.getcwd()) # list of files in current working directory.

import sys # for input arguments.
arguments = sys.argv

def main(arguments):

	nargs = len(sys.argv) # number or input arguments.  First argument is always the script name and is included in the count.

	# Define Default values:
	# If an argument is not supplied by the user then the missing fields will be populated with those below.
	# --------------------------------------------------
	report = 'False'
	outputDisplay = 'no'
	# Data columns
	xColumn = '2' # longitude.
	yColumn = '1' # latitude.
	zColumn = '3' # acc_X (ms-2).
	# Grid size
	xMin = '-180'
	xMax = '180'
	yMin = '-90'
	yMax = '90'
	# Grid spacing
	xNodes = '361'
	yNodes = '181'
	# Shepard  parameters
	algorithm = 'srfShepards'
	qNeighbors = '13'
	wNeighbors = '19'
	shepardSmooth = '0'
	# Search ellipse parameters
	R = '100' 
	Theta = '0'


	# Help Text:
	# --------------------------------------------------
	if nargs == 1: # no input parameters supplied.
		print('createBasShepard.py:')
		print('This script is used to generate modified Shepard''s method BAS files for automated Surfer operation.')
		print('Usage: ./python createBasShepard.py <keyword=value>')
		print('Keywords are: ')
		print('----------------------')
		print('name: spacecraft name')
		print('spoints: spiral points file')
		print('xmin, xmax, ymin, ymax: size of grid')
		print('xnodes, ynodes: number of horizontal and vertical grid nodes.')
		print('radius: search radius and number of sectors.')
		print('quadratic, weight: Shepard gridding parameters.')
		print('display: display results to screen.')
		print('report: produce Surfer grid report - this causes the Surfer GUI to be made visible.')
		print('----------------------')
		print('Keywords and values are separated by spaces.  The parameter values are used to generate the name of the BAS and the grid file it yields.')
		print('If no parameters beyond a spacecraft name are supplied then the default values used are: ')
		print('X column is %s' % xColumn)
		print('Y column is %s' % yColumn)
		print('Z column is %s' % zColumn)
		print('x min = %s' % xMin)
		print('x max = %s' % xMax)
		print('y min = %s' % yMin)
		print('y max = %s' % yMax)
		print('x Nodes = %s' % xNodes)
		print('y Nodes = %s' % yNodes)
		print('Radius = %s' % R)
		print('Theta = %s' % Theta)
		print('Algorithm = %s' % algorithm)
		print('Quadratic neighbors = %s' % qNeighbors)
		print('Weighting neighbors = %s' % wNeighbors)
		print('Smoothing = %s' % shepardSmooth)
		if report == 'true': # correct for lowercase user input.
			print('Grid report will be generated')
		else: 
			print('Grid report will NOT be generated.')
		print('Display output = %s' % outputDisplay)
		print('----------------------')
		print('When specifying the spiral points file name, the full path should be included:')
		print('example: spoints="C:\\Users\\me\\file.txt" ')
		print('The BAS file will be created in the same directory as this python script.')
		print('The BAS file will include file path directives to the same directory as the python script for the binary and ascii grid files.')
		print('----------------------')
		quit()


	# Parse Input Arguments:
	# --------------------------------------------------
	inputError = 0 # start with input error flag unset.
	for i in range(len(arguments)):
		# Spiral points file:
		if 'spoints=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			datumFile = argString[marker+1:]
	
		# Columns to use in spiral points file:
		if 'xcol=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			xColumn = argString[marker+1:]

		if 'ycol=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			yColumn = argString[marker+1:]

		if 'zcol=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			zColumn = argString[marker+1:]

		# Spacecraft Name:
		if 'name=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			scName = argString[marker+1:]
 
		# Grid Parameters:
		if 'xmin=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			xMin = argString[marker+1:]

		if 'xmax=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			xMax = argString[marker+1:]

		if 'ymin=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			yMin = argString[marker+1:]
	
		if 'ymax=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			yMax = argString[marker+1:]
		
		if 'xnodes=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			xNodes = argString[marker+1:]

		if 'ynodes=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			yNodes = argString[marker+1:]

		# Search Ellipse Parameters:
		if 'radius=' in arguments[i]: # search radius.
			argString = arguments[i][:]
			marker = argString.find('=')
			R = argString[marker+1:]
		
		if 'theta=' in arguments[i]: # search radius.
			argString = arguments[i][:]
			marker = argString.find('=')
			Theta = argString[marker+1:]

		# Modified Shepard's Method Parameters
		if 'quadratic=' in arguments[i]: # quadratic neighbors.
			argString = arguments[i][:]
			marker = argString.find('=')
			qNeighbors = argString[marker+1:]
	
		if 'weight=' in arguments[i]: # quadratic neighbors.
			argString = arguments[i][:]
			marker = argString.find('=')
			wNeighbors = argString[marker+1:]
		
		# Grid File Report:	
		if 'report=' in arguments[i]: # grid file report generation.
			argString = arguments[i][:]
			marker = argString.find('=')
			report = argString[marker+1:]
			if report == 'true': # correct for lowercase user input.
				report = 'True'
			else: 
				report = 'False'
		
		# Display Output:
		if 'display=' in arguments[i]: # display output to screen.
			argString = arguments[i][:]
			marker = argString.find('=')
			outputDisplay = argString[marker+1:]
			if outputDisplay == 'yes' or outputDisplay == 'y':
				outputDisplay = 'yes'
			else:
				outputDisplay = 'no'

	

	# Validate Argument Consistency:
	# --------------------------------------------------

	# Check for column designations of latitude and longitude
	if xColumn == '1' and yColumn == '2':
		pass
	elif xColumn == '2' and yColumn == '1':
		pass
	else:
		print('Error: X and Y data should be drawn from columns 2 and 1.')
		inputError = 1

	# Check for column designations of acceleration values.
	if zColumn == '3' or zColumn == '4' or zColumn == '5':
		pass
	else:
		print('Error: Z data should be drawn from columns 3,4, or 5.')
		inputError = 1


		
	# Construct filenames:
	# --------------------------------------------------
	if inputError == 0: # nothing set the error flag.
		if zColumn == '3': # acceleration in body frame X-axis.
			component = 'X'
		elif zColumn == '4': # acceleration in body frame Y-axis.
			component = 'Y'
		elif zColumn == '5': # acceleration in body frame Z-axis.
			component = 'Z'
		
		fname = os.getcwd() + "\\" + scName + component + '-R' + R + '-Q' + qNeighbors + 'W' + wNeighbors +'S' + shepardSmooth
		BASfile = fname + '.BAS' # Scripter BAS filename.
		#gridBinary = fname + '.grd' # unique filename for binary grid file.
		gridBinary = os.getcwd() + "\\" + 'binary.grd' # generic filename for binary grid file.
		gridAscii = fname + '.grd' # unique filename for ascii grid file. 


	# Print out Parameters:
	# --------------------------------------------------
	if inputError == 0 and outputDisplay == 'yes' : # nothing set the error flag.
		print('Spiral points file = %s' % datumFile)
		print('X column = %s' % xColumn)
		print('Y column is = %s' % yColumn)
		print('Z column is %s' % zColumn)
		print('spacecraft name = %s' % scName)
		print('x min = %s' % xMin)
		print('x max = %s' % xMax)
		print('y min = %s' % yMin)
		print('y max = %s' % yMax)
		print('x Nodes = %s' % xNodes)
		print('y Nodes = %s' % yNodes)
		print('Shepard radius = %s' % R)
		print('Theta = %s' % Theta)
		print('Algorithm = %s' % algorithm)
		print('Quadratic neighbors = %s' % qNeighbors)
		print('Weighting neighbors = %s' % wNeighbors)
		print('Smoothing = %s' % shepardSmooth)
		if report == 'True': # correct for lowercase user input.
			print('Grid report will be generated')
		else: 
			print('Grid report will NOT be generated.')


	# Write BAS File:
	# --------------------------------------------------
	if inputError == 0: # nothing set the error flag.
		w = open(BASfile, 'w') # open output BAS file for writing.
		# Write BAS file comments:
		w.write("' " + BASfile + "\n")
		w.write("'This Surfer script was automatically generated by the Python script createBasShepard.py.\n")
		w.write("'This script produces a grid file using the modified Shepard's method algorithm with the following parameters:\n")
		w.write("' ----------------------------------------\n")
		w.write("'Datum file = " + datumFile + '\n')
		w.write("'Columns used = {" + xColumn + ',' + yColumn + ',' + zColumn + '} ' + component + '-acceleration\n')
		w.write("'Grid size = " + yNodes + ' x ' + xNodes + ' (rows x columns)\n')
		w.write("'Grid domain = [" + xMin + "," + xMax + "]x[" + yMin + "," + yMax + "] (horizontal x vertical)\n")
		w.write("'Duplicate method = keep all \n")
		w.write("'Shepard radius1 = " + R + "\n")
		w.write("'Shepard radius2 = " + R + "\n")
		w.write("'Theta = " + Theta + "\n")
		w.write("'Algorithm = " + algorithm + "\n")
		w.write("'Quadratic neighbors = " + qNeighbors + "\n")
		w.write("'Weighting neighbors = " + wNeighbors + "\n")
		w.write("'Smoothing = " + shepardSmooth + "\n")
		if report == "True":
			w.write("'Grid report will be generated.\n")
		else:
			w.write("'Grid report will NOT be generated.\n")
		w.write("'Grid file name = " + gridAscii + "\n")
	
		# Write BAS file script:
		w.write("\n")
		w.write("\n")
		w.write("'Begin Script:\n")
		w.write("' ----------------------------------------\n")
		w.write('Sub Main\n')
		w.write('Dim SurferApp As Object\n')
		w.write('Set SurferApp = CreateObject("Surfer.Application")\n')
		if report == "True":
			w.write("SurferApp.Visible = True 'Surfer visible only if report requested.\n")
		else:
			w.write("SurferApp.Visible = False 'keep Surfer invisible.\n")
		w.write('SurferApp.GridData2(DataFile:="' + datumFile + '", _' + '\n')
		w.write('	xcol:=' + str(xColumn) + ', ycol:=' + str(yColumn) + ', zcol:=' + str(zColumn) + ', _\n')
		w.write('	NumCols:=' + str(xNodes) + ', NumRows:=' + str(yNodes) + ', _\n')
		w.write('	xMin:=' + str(xMin) + ', xMax:=' + str(xMax) + ', yMin:=' + str(yMin) + ', yMax:=' + str(yMax) + ', _\n')
		w.write('	DupMethod:=srfDupAll, _\n')
		w.write('	ShepRange1:=' + str(R) + ', _\n')
		w.write('	ShepRange2:=' + str(R) + ', _\n')
		w.write('	SearchAngle:=' + str(Theta) + ', _\n')
		w.write('	Algorithm:=' + algorithm + ', _\n')
		w.write('	ShepQuadraticNeighbors:=' + str(qNeighbors) + ', _\n')
		w.write('	ShepWeightingNeighbors:=' + str(wNeighbors) + ', _\n')
		w.write('	ShepSmoothFactor:=' + str(shepardSmooth) + ', _\n')
		w.write('	ShowReport:=' + str(report) + ', _\n')
		w.write('	OutGrid:="' + gridBinary + '")\n')
		w.write('SurferApp.GridConvert("' + gridBinary + '", "' +  gridAscii + '", OutFmt:=srfGridFmtAscii)\n' )
		w.write('End Sub\n')
		w.write("' ----------------------------------------\n")
		w.write("'End of script.")

		w.close()
		print()
		print('%s created.' % BASfile) # BAS file created.
	else:
	 	print('No BAS file generated.')

if __name__=='__main__':
	sys.exit(main(sys.argv))
