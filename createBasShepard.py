# createBasShepard.py
# Updated to generate BAS files with specified content, using Windows-style paths

import os

def determine_zcol(component):
    """Determine the zCol based on the component"""
    if component == 'X':
        return '3'  # Assuming the 3rd column is for X component values
    elif component == 'Y':
        return '4'  # Assuming the 4th column is for Y component values
    elif component == 'Z':
        return '5'  # Assuming the 5th column is for Z component values
    else:
        raise ValueError(f"Unknown component: {component}")

def main(arguments):
    folder = arguments[-1] if arguments[-1] in ['xfiles', 'yfiles', 'zfiles'] else 'xfiles'
    arguments = arguments[:-1] if arguments[-1] in ['xfiles', 'yfiles', 'zfiles'] else arguments

    outputDisplay = 'no'
    algorithm = 'srfShepards'
    qNeighbors = '13'
    wNeighbors = '19'
    shepardSmooth = '0'
    R = '100'
    component = 'X'  # Default component
    dataFile = "combi_padded.txt"

    for arg in arguments:
        key, value = arg.split('=')
        if key == 'quadratic':
            qNeighbors = value
        elif key == 'weight':
            wNeighbors = value
        elif key == 'component':
            component = value

    zCol = determine_zcol(component)

    # Manually constructing Windows-style paths for Surfer scripting
    dataFilePath = f"c:\\\\Users\\\\sgnl\\\\Downloads\\\\{dataFile}"
    outGridPath = f"c:\\\\Users\\\\sgnl\\\\Downloads\\\\{folder}\\\\binary.grd"
    fname = f"noref_GPSIIF_v06{component}-R{R}-Q{qNeighbors}W{wNeighbors}S{shepardSmooth}.BAS"
    convertedGridPath = outGridPath.replace("binary.grd", fname.replace('.BAS', '.grd'))

    # Directory and BAS file creation for execution environment
    basePath = os.path.join(os.getcwd(), folder)
    os.makedirs(basePath, exist_ok=True)
    basFile = os.path.join(basePath, fname)

    basContent = f"""' Generated by createBasShepard.py
Sub Main
    Dim SurferApp As Object
    Set SurferApp = CreateObject("Surfer.Application")
    SurferApp.Visible = False
    SurferApp.GridData2(DataFile:="{dataFilePath}", _
        xCol:=2, yCol:=1, zCol:={zCol}, _
        NumCols:=361, NumRows:=181, _
        xMin:=-180, xMax:=180, yMin:=-90, yMax:=90, _
        DupMethod:=srfDupNone, _
        ShepRange1:=100, ShepRange2:=100, \
        SearchAngle:=0, \
        Algorithm:="{algorithm}", \
        ShepQuadraticNeighbors:={qNeighbors}, \
        ShepWeightingNeighbors:={wNeighbors}, \
        ShepSmoothFactor:=0, \
        ShowReport:={outputDisplay}, \
        OutGrid:="{outGridPath}")
    SurferApp.GridConvert("{outGridPath}", "{convertedGridPath}", OutFmt:=srfGridFmtAscii)
End Sub
"""

    with open(basFile, 'w') as file:
        file.write(basContent)

    print(f"BAS file generated for {component} in {basFile}")

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
