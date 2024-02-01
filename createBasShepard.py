# createBasShepard.py
# Updated to generate BAS files with specified content

import os

def main(arguments):
    # Assuming the last argument is always the folder when called directly for simplicity
    folder = arguments[-1] if arguments[-1] in ['xfiles', 'yfiles', 'zfiles'] else 'xfiles'
    # Remove the folder argument from the list if it's there
    arguments = arguments[:-1] if arguments[-1] in ['xfiles', 'yfiles', 'zfiles'] else arguments

    # Default values and initialization
    outputDisplay = 'no'
    algorithm = 'srfShepards'
    qNeighbors = '13'  # Default to 13 if not specified
    wNeighbors = '19'  # Default to 19 if not specified
    shepardSmooth = '0'
    R = '100'
    Theta = '0'
    component = 'X'  # Default component
    dataFile = "combi_padded.txt"  # Path to your data file

    # Parse the arguments list
    for arg in arguments:
        key, value = arg.split('=')
        if key == 'quadratic':
            qNeighbors = value
        elif key == 'weight':
            wNeighbors = value
        elif key == 'component':
            component = value  # Set component based on input

    # Construct file and directory names based on arguments
    fname = f"noref_GPSIIF_v06{component}-R{R}-Q{qNeighbors}W{wNeighbors}S{shepardSmooth}"
    # Ensure the directory exists
    # basePath = os.path.join(os.getcwd(), folder)
    # Or, as a raw string (note the 'r' prefix)
    basePath = os.path.join(os.getcwd(), folder) 
    os.makedirs(basePath, exist_ok=True)
    basFile = os.path.join(basePath, fname + '.BAS')

    # Ensure the directory exists
    os.makedirs(basePath, exist_ok=True)


    basContent = f"""' Generated by createBasShepard.py
Sub Main
    Dim SurferApp As Object
    Set SurferApp = CreateObject("Surfer.Application")
    SurferApp.Visible = False
    SurferApp.GridData2(DataFile:="c:\\Users\\sgnl\\Downloads\\{dataFile}", _
        xCol:=2, yCol:=1, zCol:=3, _
        NumCols:=361, NumRows:=181, _
        xMin:=-180, xMax:=180, yMin:=-90, yMax:=90, _
        DupMethod:=srfDupAll, _
        ShepRange1:=100, ShepRange2:=100, _
        SearchAngle:=0, _
        Algorithm:="{algorithm}", _
        ShepQuadraticNeighbors:={qNeighbors}, _
        ShepWeightingNeighbors:={wNeighbors}, _
        ShepSmoothFactor:=0, _
        ShowReport:={outputDisplay}, _
        OutGrid:="c:\\Users\\sgnl\\Downloads\\binary.grd")
    SurferApp.GridConvert("c:\\Users\\sgnl\\Downloads\\binary.grd", "c:\\Users\\sgnl\\Downloads\\{fname}.grd", OutFmt:=srfGridFmtAscii)
End Sub
"""


    # Write the BAS file
    with open(basFile, 'w') as file:
        file.write(basContent)

    print(f"BAS file generated for {component} in {basFile}")

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
