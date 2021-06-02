"""
grid.py
Created February 17, 2021

Provides methods for identifying the size and location of the grid in images of leads.
"""
from .. import common
from .. import vision


def extractGridFromImage(image, spacingReductionMethod=common.mode):
    """Takes a cropped image of a single lead and returns the grid scaling in pixels

    Args:
        image (??): 2d color image of the lead
        spacingReductionMethod (??, optional):Takes a list of distances between detected grid lines and estimates
                the grid size (note that some lines may be missing). Defaults to common.mode.
    """
    def getSpacingInDirection(lines, direction: int):
        """Takes all of the lines in an image, filters to those oriented in the specified direction, and estimates
        the most likely underlying spacing (some or many lines may be missing so mean is not necessarily suitable)"""

        if common.emptyOrNone(lines):
            print("WARNING: No lines available")
            return None

        orientedLines = vision.getLinesInDirection(lines, direction)
        if common.emptyOrNone(orientedLines):
            print("WARNING: No lines in direction")
            return None

        distances = common.calculateDistancesBetweenValues(sorted(orientedLines))
        if common.emptyOrNone(distances):
            print("WARNING: No distances")
            return None

        # TODO: Implement an autocorrelation approach or something else to do a better job of this (median?)...
        gridSpacing = spacingReductionMethod(distances)

        return gridSpacing

    # gridBinary = detectionMethod(image)
    gridBinary = vision.binarize(vision.greyscale(image), 230)

    # TODO: Modularize the line extraction process.
    lines = vision.houghLines(gridBinary, threshold=80)

    horizontalGridSpacing = getSpacingInDirection(lines, 0)
    verticalGridSpacing   = getSpacingInDirection(lines, 90)

    return (horizontalGridSpacing, verticalGridSpacing)
