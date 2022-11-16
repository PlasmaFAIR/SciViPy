from textwrap import dedent
from pathlib import Path
import argparse


def time_reader(path, output, Range=607, start=4000):
    """
    Function which will read a file and return equidistant readings from values within
    the file.

    The main purpose of this is to extract temporal data when equidistant time steps
    weren't initally recorded or were recorded in a nonlinear fashion.

    Take in an input file and a number of points to record and will return a text file
    with the specified number of points split equitemporally. This is useful when trying
    to create gifs from some simulated JOREK data.
    """
    listOfTimesteps = []
    listofnumbers = []
    CleanedOutputs = []
    FileID = []
    File = open(path, "r")

    FLength = len(File.readlines())
    print(FLength)

    for count, x in enumerate(File):
        FullString = x
        print(FullString)
        StringToCut = FullString[0:14]
        # Trims the data into a floating point format to be used in numerical
        # calculations
        FinalString = FullString.replace(StringToCut, "")
        SigFigString = FinalString[0:8]
        StringToConvert = SigFigString.strip()
        NumString = float(StringToConvert)

        if count >= 553:
            # Used to handle the difference in significant figures within the dataset
            # (probably a more general solution)
            NumString = NumString * 10

        CleanedOutputs.append(NumString)

    File.close()
    print(CleanedOutputs)
    startval = CleanedOutputs[1]

    endindex = 607
    endval = CleanedOutputs[endindex]
    noofpoints = 150
    # Used to determine the value of an equitemporal time step over a given number of
    # points
    initialtimestep = (endval - startval) / noofpoints

    # Creates a temporary timestep that then gets added to an array which is added to
    # the initial value
    for i in range(noofpoints):
        DummyTimestep = initialtimestep * i
        listOfTimesteps.append(DummyTimestep)

        listofnumbers.append(startval + listOfTimesteps[i])

    # Finds the value that's closest in the file to the given timestep and gives its val
    for i in range(len(listOfTimesteps)):
        closestval = min(
            enumerate(CleanedOutputs), key=lambda x: abs(x[1] - (listofnumbers[i]))
        )
        FileID.append(4000 + (10 * closestval[0]))

    print(FileID)

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as fp:
        for item in FileID:
            # write each item on a new line
            fp.write("%s\n" % item)
        print("Done")

    fp.close


if __name__ == "__main__":
    # Files originally specified in this script:
    # "C:\\Users\\FWKCa\\OneDrive\\Desktop\\Internship stuff\\jorek_times.txt"
    # "/home/user/Desktop/TEST DATA FOR SCRIPTS/TestText.txt"

    # Define command line interface for this script
    parser = argparse.ArgumentParser(
        prog="SciViPy.time_reader",
        description=(
            dedent(
                """\
                Takes in a .txt file containing a list of timesteps for a given data set
                and ensures that they are linearly replaced so that smooth animations
                can be produced with ease using paraview.
                """
            )
        ),
    )

    parser.add_argument(
        "path",
        help="Path to .txt file.",
        type=Path,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file path.",
        type=Path,
        default="time_reader_out.txt",
    )

    parser.add_argument(
        "--range",
        help="The number of time steps to read from a file.",
        type=int,
        default=607,
    )

    parser.add_argument(
        "--start",
        help="Initial value to read",
        type=int,
        default=607,
    )

    # Get inputs/outputs from the command line
    args = parser.parse_args()

    # Check that input/output dirs are valid
    if not args.path.is_file():
        raise FileNotFoundError(args.path)

    # Run
    time_reader(args.path, args.output, Range=args.range, start=args.start)
