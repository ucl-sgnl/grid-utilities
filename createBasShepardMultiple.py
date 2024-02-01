# createBasShepardMultiple.py
# Updated to automatically run for X, Y, and Z components and save in specified folders

import sys
import createBasShepard  # Ensure this script is in the same directory or in the Python path

def main():
    # Check for the presence of input arguments
    if len(sys.argv) == 1:
        print("Usage: python createBasShepardMultiple.py <keyword=value> ...")
        sys.exit()

    # Parsing input arguments
    arguments = sys.argv[1:]  # Exclude the script name itself
    params = {}
    for argument in arguments:
        key, value = argument.split('=')
        params[key] = value

    # Required parameters with example defaults if not provided
    qMin = int(params.get('minquadratic', 10))
    qMax = int(params.get('maxquadratic', 20))
    wMin = int(params.get('minweight', 1))
    wMax = int(params.get('maxweight', 5))

    # Components to iterate over
    components = ['X', 'Y', 'Z']
    folders = {'X': 'xfiles', 'Y': 'yfiles', 'Z': 'zfiles'}

    for component in components:
        folder = folders[component]
        for neighbor in range(qMin, qMax + 1):
            for weight in range(wMin, wMax + 1):
                modifiedArguments = [
                    'component=' + component,
                    'quadratic=' + str(neighbor),
                    'weight=' + str(weight),
                    folder  # Directly pass folder as the last argument
                ]
                createBasShepard.main(modifiedArguments)

    print(f"Generated BAS files for neighbors={list(range(qMin, qMax + 1))} and weights={list(range(wMin, wMax + 1))} in {components}")

if __name__ == "__main__":
    main()
