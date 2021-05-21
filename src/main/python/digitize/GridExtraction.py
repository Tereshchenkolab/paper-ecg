"""
GridExtraction.py
Created February 17, 2021

-
"""
from .Common import *
from . import Vision


def traceGridlines(binaryImage, houghThreshold=80):
    lines = Vision.houghLines(binaryImage, houghThreshold)

    def getDistancesBetween(lines, inDirection=0):
        orientedLines = sorted(Vision.getLinesInDirection(lines, inDirection))
        return calculateDistancesBetweenValues(orientedLines)

    verticalDistances = getDistancesBetween(lines=lines, inDirection=90)
    horizontalDistances = getDistancesBetween(lines=lines, inDirection=0)

    verticalGridSpacing, horizontalGridSpacing = mode(verticalDistances), mode(horizontalDistances)

    if verticalGridSpacing is None:
        return horizontalGridSpacing
    elif horizontalGridSpacing is None:
        return verticalGridSpacing
    else:
        return min([verticalGridSpacing, horizontalGridSpacing])


# TODO: Use median?

# TODO: Try using some sort of clustering and picking the smallest cluster below a threshold
