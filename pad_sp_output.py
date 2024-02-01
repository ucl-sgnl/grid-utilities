
if __name__ == '__main__':
    import os
    import sys
    import numpy as np

    # Get the list of files in the current working directory
    localFiles = os.listdir(os.getcwd())

    # Check command line arguments
    nargs = len(sys.argv)
    if nargs < 3:
        print("\nFile arguments missing:\nUsage: python pad_sp_output.py <input file> <output file>")
        inputFile = input('Enter input filename: ')
        while inputFile not in localFiles:
            print("Filename entered was not located in current directory.")
            inputFile = input('Enter input filename: ')
        outputFile = input('Enter output filename: ')
    elif nargs == 3:
        inputFile, outputFile = sys.argv[1], sys.argv[2]

    # Check if input file exists
    if inputFile not in localFiles:
        inputFile = input(f'Input file {inputFile} was not located in current directory. Enter input filename: ')
        while inputFile not in localFiles:
            inputFile = input('Enter input filename: ')

    # Check if output file exists and handle overwrite
    if outputFile in localFiles:
        outputOverwrite = input('Output file already exists. Overwrite: [(y)es/(n)o] ? ')
        if outputOverwrite.lower() not in ['y', 'yes']:
            outputFile = input('Enter filename: ')

    # Read input file and skip header
    with open(inputFile, 'r') as fin:
        next(fin)  # Skip header line
        sPoints = [[float(val) if i < 2 else val.strip() for i, val in enumerate(line.split(','))] for line in fin]
        N = len(sPoints)
        print(f'{N} spiral points detected in {inputFile}.')

    # Write original spiral points to output file
    with open(outputFile, 'w') as fout:
        for lat, lon, x, y, z, *_ in sPoints:
            fout.write(f'{lat:.15f}, {lon:.15f}, {x}, {y}, {z}\n')
        print(f"Original spiral points written to {outputFile}.")

    def pad_points(points, mode):
        padded = []
        for lat, lon, x, y, z in points:
            if mode == "top":
                padded.append([90.0 + (90.0 - lat), lon - 180.0 if lon >= 0.0 else lon + 180.0, x, y, z])
            elif mode == "bottom":
                padded.append([-90.0 - (lat + 90.0), lon - 180.0 if lon >= 0.0 else lon + 180.0, x, y, z])
            elif mode == "left":
                padded.append([lat, lon - 360.0, x, y, z])
            elif mode == "right":
                padded.append([lat, lon + 360.0, x, y, z])
            elif mode in ["ne", "nw", "se", "sw"]:
                new_lat = 180.0 - lat if 'n' in mode else -1.0 * lat - 180.0
                new_lon = lon + 180.0 if lon >= 0.0 else lon - 180.0
                padded.append([new_lat, new_lon, x, y, z])
        return padded

    modes = ["top", "bottom", "left", "right", "ne", "nw", "se", "sw"]
    all_padded_points = {mode: pad_points(sPoints, mode) for mode in modes}

    # Generate north and south grid longitude values
    gridLongitude = np.linspace(-181, 182, 364)  # 1 degree spacing
    northGrid = [[90.0, lon, *sPoints[0][2:]] for lon in gridLongitude]
    southGrid = [[-90.0, lon, *sPoints[-1][2:]] for lon in gridLongitude]

    all_padded_points.update({"north": northGrid, "south": southGrid})

    # Append padded spiral points to output file
    with open(outputFile, 'a') as fout:
        for mode, points in all_padded_points.items():
            for lat, lon, x, y, z in points:
                fout.write(f'{lat:.15f}, {lon:.15f}, {x}, {y}, {z}\n')
            print(f"{len(points)} points written for {mode} padding.")

    Ntotal = N + sum(len(points) for points in all_padded_points.values())
    print(f"{Ntotal} total spiral points.")