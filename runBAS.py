# runBas.py

# This python script uses Bas files to create grid files.
# The script calls the Scripter program to execute each Bas file in the directory this script is located in.
# Scripter must be included in the Windows path variable.
# Bas files are identified as those with the .BAS extension.
# Two implementations are available:

#
# python runBas.py <filename>
# will call Scripter to execute the specified Bas file.

# 
# python runBas.py
# will call Scripter to execute all Bas files in the current directory. 

#
# This version does not provide for any status or feedback of Scripter executions.
# Bas files which fail to execute will cause Scripter to halt.  The file may be corrected
# in Scripter and run, or closed.  After this instance of Scripter has been closed the 
# script will continue calling instances of Scripter to execute the remaining Bas files.
#

# created November 18, 2012 - Shawn Allgeier
import sys # for input arguments.
arguments = sys.argv

from subprocess import call # for executing in terminal.
import os

nargs = len(arguments) # number or input arguments.  First argument is always the script name and is included in the count.

if nargs == 2: # one input parameter supplied.
	basFile = arguments[1]
	command = 'scripter -x ' + str(basFile)
	call(command)

else: # run all bas files in directory. 
	cwd = os.getcwd() # current working directory.
	fileList = os.listdir(cwd) # list of files in cwd.

	print("Running Bas files in %s" % cwd)

	k = len(fileList)
	for i in range(k):
		if '.BAS' in fileList[i]:
			command = 'scripter -x ' + str(fileList[i])
			print(command)

			x = call(command)
			#if x != 0:

			#	print "Error running %s" % fileList[i]
# End of script.