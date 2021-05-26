"""
extraction.py
Created February 17, 2021

Provides methods for extracting digital signal from lead images.
"""
from typing import Iterable, Optional, Tuple
import numpy as np
from math import sqrt, asin, pi

from .. import common


def findFirstLastNonZeroPixels(oneDimImage: np.ndarray) ->Tuple[Optional[int], Optional[int]]:

    def reverseEnumerate(array: np.ndarray):
        for index in common.reversedRange(len(array)):
            yield index, array[index]

    def findFirstNonZero(oneDimImage: np.ndarray, reversed: bool = False) -> Optional[int]:
        iterator = reverseEnumerate(oneDimImage) if reversed else enumerate(oneDimImage)
        for index, pixel in iterator:
            if pixel > 0:
                return index

        return None

    top, bottom = findFirstNonZero(oneDimImage), findFirstNonZero(oneDimImage, reversed=True)
    return top, bottom


def naïveHorizontalScan(image: np.ndarray):
    columns = np.swapaxes(image, 0, 1)
    output  = np.zeros(len(columns))

    for index, column in enumerate(columns):
        top, bottom = findFirstLastNonZeroPixels(column)

        if top is not None and bottom is not None:
            output[index] = (top + bottom) / 2

    return output


def findContiguousRegions(oneDimImage: np.ndarray) -> Iterable[Tuple[int, int]]:
    """
    ex: |---###--#-----#####|  (where # is on, - is off)
        |0123456789...      |
    returns [(3,5), (8,8), (14,18)]
    """
    locations = []
    start = None
    for index, pixel in enumerate(oneDimImage):
        if pixel > 0 and start is None:
            start = index
        elif pixel == 0 and start is not None:
            locations.append((start, index))
            start = None

    return locations


def findContiguousRegionCenters(oneDimImage: np.ndarray) -> Iterable[int]:
    """
    ex: |---###--#-----#####|  (where # is on, - is off)
        |0123456789...      |
    returns [4, 8, 16]

    Rounds down to the nearest int
    """
    return [int(np.mean(list(locationPair))) for locationPair in findContiguousRegions(oneDimImage)]


def euclideanDistance(x: int, y: int) -> float:
    return sqrt((x**2) + (y**2))


hypotenuse = euclideanDistance


def distanceBetweenPoints(firstPoint: Tuple[int, int], secondPoint: Tuple[int, int]) -> float:
    return euclideanDistance(firstPoint[0] - secondPoint[0], firstPoint[1] - secondPoint[1])


def angleFromOffsets(x: int, y: int) -> float:
    return asin(y/hypotenuse(x,y)) / pi * 180


def angleBetweenPoints(firstPoint: Tuple[int, int], secondPoint: Tuple[int, int]) -> float:
    deltaX = secondPoint[0] - firstPoint[0]
    deltaY = secondPoint[1] - firstPoint[1]
    return angleFromOffsets(deltaX, deltaY)


def angleSimilarity(firstAngle: float, secondAngle: float) -> float:
    return (180 - abs(secondAngle - firstAngle)) / 180


def searchArea(initialRow: int, radius: int) -> Iterable[Tuple[int, int]]:
    area = []
    for column in range(1, radius+1):
        verticalOffset = 0
        while euclideanDistance(column, verticalOffset + 1) <= float(radius):
            verticalOffset += 1
        area.append((initialRow - verticalOffset, initialRow + verticalOffset))

    return area


def getPointLocations(image: np.ndarray) -> np.ndarray:
    columns = np.swapaxes(image, 0, 1)

    pointLocations = []

    # Scan horizontally across the image
    for column, pixels in enumerate(columns):
        # Get all points that could be part of a signal
        rows = findContiguousRegionCenters(pixels)
        points = common.mapList(rows, lambda row: (row, column))

        pointLocations.append(points)

    return pointLocations
