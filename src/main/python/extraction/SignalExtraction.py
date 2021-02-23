"""
SignalExtraction.py
Created February 17, 2021

-
"""


from typing import Any, Callable, Generator, Iterable, Optional, Tuple
import numpy as np
from math import sqrt, asin, pi
from collections import namedtuple

def reversedRange(stop):
        return range(stop-1, -1, -1)

def inclusiveRange(start, stop):
    return range(start, stop+1)

def neg(inputValue: int) -> int:
    return -1 * inputValue


def findFirstLastNonZeroPixels(oneDimImage: np.ndarray) -> Tuple[int, int]:

    def reverseEnumerate(array: np.ndarray):
        for index in reversedRange(len(array)):
            yield index, array[index]

    def findFirstNonZero(oneDimImage: np.ndarray, reversed: bool = False) -> Optional[int]:
        iterator = reverseEnumerate(oneDimImage) if reversed else enumerate(oneDimImage)
        for index, pixel in iterator:
            if pixel > 0:
                return index

        return None

    return findFirstNonZero(oneDimImage), findFirstNonZero(oneDimImage, reversed=True)


def naïveHorizontalScan(image: np.ndarray):
    columns = np.swapaxes(image, 0, 1)

    return np.array(
        [np.mean(
            list(findFirstLastNonZeroPixels(column))
         ) for column in columns]
    )


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


def euclideanDistance(x: int, y: int) -> int:
    return sqrt((x**2) + (y**2))

hypotenuse: Callable[[int,int], int] = euclideanDistance

def distanceBetweenPoints(firstPoint: Tuple[int, int], secondPoint: Tuple[int, int]) -> int:
    return euclideanDistance(firstPoint[0] - secondPoint[0], firstPoint[1] - secondPoint[1])


def angleFromOffsets(x: int, y: int) -> float:
    return asin(y/hypotenuse(x,y)) / pi * 180


def angleBetweenPoints(firstPoint: Tuple[int, int], secondPoint: Tuple[int, int]) -> float:
    deltaX = secondPoint[0] - firstPoint[0]
    deltaY = secondPoint[1] - firstPoint[1]
    return angleFromOffsets(deltaX, deltaY)


def angleSimilarity(firstAngle: float, secondAngle: float) -> float:
    return abs(secondAngle - firstAngle)


def searchArea(initialRow: Tuple[int, int], radius: int) -> Iterable[Tuple[int]]:
    area = []
    for column in range(1, radius+1):
        verticalOffset = 0
        while euclideanDistance(column, verticalOffset + 1) <= float(radius):
            verticalOffset += 1
        area.append((initialRow - verticalOffset, initialRow + verticalOffset))

    return area


def getPointLocations(image: np.ndarray) -> np.ndarray:
    columns = np.swapaxes(image, 0, 1)

    pointLocations = np.full(image.shape, np.nan)

    # Scan horizontally across the image
    for columnIndex, column in enumerate(columns):
        # Get all points that could be part of a signal
        points = findContiguousRegionCenters(column)

        for point in points:
            pointLocations[point, columnIndex] = 1

    return pointLocations


class SignalPoint():

    def __init__(self, x: int, y: int, orientation: float) -> None:
        pass


class SignalBuilder():

    def __init__(self) -> None:
        self.pointList = []

    @classmethod
    def startingAt(thisClass, point: Tuple[int,int]):
        x, y = point

    @staticmethod
    def evaluate(first: SignalPoint, second: SignalPoint):
        pass


def horizontalScanLookBehind(image: np.ndarray, radius: int = 12, orientationSmoothing: int = 0):
    columns = np.swapaxes(image, 0, 1)

    pointLocations = getPointLocations(image)

    return pointLocations


# TODO

# * Implement function for determining likelihood of point being in signal (weight proximity higher)
# * Implement line tracing function
#   - Use the 2d array showing potential point locations
#   - Figure out how to start lines (any unclaimed point after running through all signals?)
#   - Iterate over all signals
#      - Find all points in search space
#      - Evaluate likelihood of each point being part of the line
#      - Put all the (likelihood, point) pairs in a maxheap
#      - Create method to spit out points the signal "wants" in order of likelihood
#   - Keep track of claimed points
#   - Put all (likelihood of best point, signal) pairs in maxheap
#   - Start allocating points to signals
#   - If a signal tries to claim a claimed point, ask it for it's next favorite point and changekey in the maxheap

# * Implement function for creating a 2d default dict for tracking claimed points (overkill?)