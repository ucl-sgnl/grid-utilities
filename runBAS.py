
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