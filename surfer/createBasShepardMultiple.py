# createBasShepardMultiple.py
# This script is used to generate BAS files for use in Scripter to produce grid files using modified Shepard's method in Surfer. 
# The script accepts command line arguments to set gridding parameters.  
# The resulting binary grid file is then converted to the Surfer6 ascii text format.
# Usage: python createBasShepardMultiple.py <keyword=value> ...
# A list of keywords can be obtained by invoking this script without any input arguments.  
# Gridding parameters revert to a default set in the event if not specified by the user.  
# The default values are listed when the script is called without any input arguments.  
# The BAS and resulting grid filenames are automatically generated from the gridding parameters.  
# The location (absolute file path) of a datums file must be supplied.  
# Note: The this script relies on 'createBasShepard.py'.
# # This script is used to generate multiple BAS files in a range of values for both the number of quadratic neighbors and weights.
# 
# created January 29, 2013 - Shawn Allgeier

# Configure Modules:
version = 1

import sys # for input arguments.
import createBasShepard # script for writing Shepard Bas files.

arguments = sys.argv
nargs = len(sys.argv) # number or input arguments.  First argument is always the script name and is included in the count.

# Instructions:
if nargs == 1: # no input arguments supplied.
	print("------------------------------")
	print("createBasShepardMultiple.py:")
	print("This script accepts parameters and uses the script 'createBasShepard.py' to generate multiple BAS files for use in Scripter.")
	print("Arguments supplied to 'createBasShepardMultiple.py' are passed to 'createBasShepard.py'. ")
	print("The minimum set of arguments which must be supplied are for:")
	print("File path to datums (spoints).")
	print("Minimum quadratic neighbors (minquad).")
	print("Maximum quadratic neighbors (maxquad).")
	print("Minimum weight (minweight).")
	print("Maximum weight (maxweight).")
	print("Necessary parameters not supplied will assume the default values prescribed in 'createBasShepard.py'. ")
	print("Usage: python createBasShepardMultiple <keyword=value> ...")
	print("------------------------------")

	createBasShepard.main(0) # call this script without arguments so that it displays its help text.
	quit()

if nargs > 1: # input parameters supplied.

	# Parse Input Arguments:
	# --------------------------------------------------
	inputError = 0 # start with input error flag unset.
	for i in range(nargs):
		# Minimum Quadratic Neighbors:
		if 'minquadratic=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			qMin = argString[marker+1:]

		# Maximum Quadratic Neighbors:
		if 'maxquadratic=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			qMax = argString[marker+1:]

		# Minimum Weight:
		if 'minweight=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			wMin = argString[marker+1:]

		# Maximum Weight:
		if 'maxweight=' in arguments[i]:
			argString = arguments[i][:]
			marker = argString.find('=')
			wMax = argString[marker+1:]



	# Validate Input for Graceful Failure:
	# iputError variable not currently implemented. This will be polished at a later date. 
	# Formulate Lists of Parameter Values:
	neighbors = range(int(qMin), int(qMax)+1) # list of quadratic neighbor radius values.
	weights = range(int(wMin), int(wMax)+1) # list of weight radius values.

	m = len(neighbors)
	n = len(weights)

	print("Generating " + str(n*m) + " BAS files using:")
	print("Neighbors = " + str(neighbors))
	print("Weights = " + str(weights))



	# Generate BAS Files:

	for i in range(n):
		for j in range(m):
			modifiedArguments = arguments + ['display=no', 'quadratic='+str(neighbors[j]), 'weight='+str(weights[i])] # select combination of quadratic neighbors and weights.
			createBasShepard.main(modifiedArguments) # call script to generate BAS file.

	#print "BAS scripts generated."



# End of Script.

