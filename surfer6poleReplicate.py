import math
import os
import sys

if __name__ == '__main__':
    localFiles = os.listdir(os.getcwd())
    arguments = sys.argv
    nargs = len(sys.argv)

    if nargs < 3:
        print("\nFile arguments missing:\nUsage: python surfer6poleReplicate.py <input file> <output file>")
        inputFile = input('Enter input filename: ')
        while inputFile not in localFiles:
            print("Filename entered was not located in current directory.")
            inputFile = input('Enter input filename: ')
        outputFile = input('Enter output filename: ')
    elif nargs == 3:
        inputFile, outputFile = sys.argv[1], sys.argv[2]

    if inputFile not in localFiles:
        inputFile = input(f'Input file {inputFile} was not located in current directory. Enter input filename: ')
        while inputFile not in localFiles:
            inputFile = input('Enter input filename: ')
    if outputFile in localFiles:
        outputOverwrite = input('Output file already exists. Overwrite: [(y)es/(n)o] ? ')
        if outputOverwrite.lower() not in ['y', 'yes']:
            outputFile = input('Enter filename: ')

    with open(inputFile, 'r') as fin:
        N = sum(1 for _ in fin)
        fin.seek(0)  # return cursor to start of file
        header = fin.readline()
        nodes = fin.readline()
        xnodes, ynodes = map(int, nodes.split())
        xmin, xmax = map(float, fin.readline().split())
        ymin, ymax = map(float, fin.readline().split())
        zmin, zmax = fin.readline().split()
        print(f'{inputFile}:')
        print(f'{xnodes} xnodes and {ynodes} ynodes')
        print(f'X values are [{xmin}, {xmax}]')
        print(f'Y values are [{ymin}, {ymax}]')
        print(f'Z values are [{zmin}, {zmax}]')

        latitudeCheck = ymax == 90.0 and ymin == -90.0
        deltaX = (xmax - xmin) / (xnodes - 1.0)
        m = int((-1 * xmin / deltaX) + 1)
        longitudeCheck = m == math.floor(m) and xmin < 0.0 and xmax > 0.0

        if not latitudeCheck or not longitudeCheck:
            print("North and South poles are not included in this grid file.")
            print("This tool cannot be used - choose your grid file parameters wisely!")
            print("Exiting script.")
            sys.exit()

        partialLine = xnodes % 10
        if partialLine == 0:
            print("No partial lines in this grid file.")
        else:
            print(f"Partial lines have {partialLine} value(s) on them.")
        print(f"Each latitude occupies {m//10 + partialLine} lines in the file.")

        fin.seek(0)  # return cursor to start of file.
        for i in range(5):  # Skip header info
            fin.readline()

        southPole, northPole = None, None
        if m % 10 == 0:
            completeRows = (m // 10)
            for i in range(completeRows - 1):
                fin.readline()
            line = fin.readline()
            southPole = float(line.split()[9])
        else:
            dummyRows = m // 10
            for i in range(dummyRows):
                fin.readline()
            line = fin.readline()
            southPole = float(line.split()[m % 10 - 1])

        fin.seek(0)
        all_lines = fin.readlines()
        northPole = float(all_lines[-1].split()[m % 10 - 1 if partialLine != 0 else 9])

    with open(outputFile, 'w') as fout:
        fout.writelines(all_lines[:5])  # Write header and grid parameter information

        spLine = " ".join([str(southPole)] * 10) + " \n"
        for i in range(xnodes // 10):
            fout.write(spLine)
        if partialLine != 0:
            fout.write(" ".join([str(southPole)] * partialLine) + "\n")
        fout.write("\n")

        fout.writelines(all_lines[5 + (xnodes // 10 + (1 if partialLine != 0 else 0)):])

        npLine = " ".join([str(northPole)] * 10) + " \n"
        for i in range(xnodes // 10):
            fout.write(npLine)
        if partialLine != 0:
            fout.write(" ".join([str(northPole)] * partialLine) + "\n")
        fout.write("\n")