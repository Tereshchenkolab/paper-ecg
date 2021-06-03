"""
viterbi.py
Created June 1, 2021

...
"""
from collections import defaultdict
from functools import partial

from dataclasses import dataclass
from ecgdigitize import signal
from math import isnan, sqrt, asin, pi
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

import numpy as np
import matplotlib.pyplot as plt

from ... import common
from ...common import Numeric
from ...image import BinaryImage


@dataclass(frozen=True)
class Point:
    x: Numeric
    y: Numeric

    @property
    def index(self) -> int:
        if isinstance(self.x, int):
            return self.x
        else:
            return round(self.x)

    @property
    def values(self) -> Tuple[Numeric, Numeric]:
        return (self.x, self.y)


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


def euclideanDistance(x: Numeric, y: Numeric) -> float:
    return sqrt((x**2) + (y**2))


def distanceBetweenPoints(firstPoint: Point, secondPoint: Point) -> float:
    return euclideanDistance(firstPoint.x - secondPoint.x, firstPoint.y - secondPoint.y)


def angleFromOffsets(x: Numeric, y: Numeric) -> float:
    return asin(y/euclideanDistance(x,y)) / pi * 180


def angleBetweenPoints(firstPoint: Point, secondPoint: Point) -> float:
    deltaX = secondPoint.x - firstPoint.x
    deltaY = secondPoint.y - firstPoint.y
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


def getPointLocations(image: np.ndarray) -> List[List[Point]]:
    columns = np.swapaxes(image, 0, 1)

    pointLocations = []

    # Scan horizontally across the image
    for column, pixels in enumerate(columns):
        # Get all points that could be part of a signal
        rows = findContiguousRegionCenters(pixels)
        points = common.mapList(rows, lambda row: Point(column, row))

        pointLocations.append(points)

    return pointLocations


# TODO: Make score multiply, or normalize the score by the length of the path
def score(currentPoint: Point, candidatePoint: Point, candidateAngle: float) -> float:
    DISTANCE_WEIGHT = .5

    currentAngle = angleBetweenPoints(candidatePoint, currentPoint)
    angleValue = 1 - angleSimilarity(currentAngle, candidateAngle)
    distanceValue = distanceBetweenPoints(currentPoint, candidatePoint)

    # print(currentAngle, candidateAngle, angleValue)
    # print(distanceValue)

    return (distanceValue * DISTANCE_WEIGHT) + (angleValue * (1 - DISTANCE_WEIGHT))


def getAdjacent(pointsByColumn, bestPathToPoint, startingColumn: int, minimumLookBack: int):
    rightColumnIndex = startingColumn
    leftColumnIndex = int(common.lowerClamp(startingColumn-minimumLookBack, 0))

    result = list(common.flatten(pointsByColumn[leftColumnIndex:rightColumnIndex]))

    while len(result) == 0 and leftColumnIndex >= 0:
        leftColumnIndex -= 1
        result = list(common.flatten(pointsByColumn[leftColumnIndex:rightColumnIndex])) # TODO: Make this more efficient?

    for point in result:
        assert point in bestPathToPoint, "Found point that hasn't yet been frozen"
        pointScore, _, pointAngle = bestPathToPoint[point]
        yield pointScore, point, pointAngle


def interpolate(fromPoint: Point, toPoint: Point) -> Iterator[Point]:
    slope = (toPoint.y - fromPoint.y) / (toPoint.x - fromPoint.x)
    f = lambda x: slope * (x - toPoint.x) + toPoint.y

    for x in range(fromPoint.index + 1, toPoint.index):
        yield Point(x, f(x))


def convertPointsToSignal(points: List[Point], width: Optional[int] = None) -> np.ndarray:
    assert len(points) > 0

    firstPoint = points[0]  # farthest from y-axis (recall we `back`-tracked earlier so paths are reversed)
    lastPoint = points[-1]  # closest to y-axis

    arraySize = width or (firstPoint.x + 1)
    signal = np.full(arraySize, np.nan, dtype=float)

    signal[firstPoint.index] = firstPoint.y
    priorPoint = firstPoint

    for point in points[1:]:
        if isnan(signal[point.index + 1]):
            for interpolatedPoint in interpolate(point, priorPoint):
                signal[interpolatedPoint.index] = interpolatedPoint.y

        signal[point.index] = point.y
        priorPoint = point

    return signal


def extractSignal(binary: BinaryImage) -> Optional[np.ndarray]:
    pointsByColumn = getPointLocations(binary.data)
    points = list(common.flatten(pointsByColumn))

    if len(points) == 0:
        return None

    minimumLookBack = 1

    bestPathToPoint: Dict[Point, Tuple[float, Optional[Point], float]] = {}

    # TODO: Allow some leeway either (1) Initialize the first N columns with 0s or (2) Search until some threshold for seeding is met

    # Initialize the DP table with base cases (far left side)
    # TODO: Is this even needed? See below. Currently causes error with `getAdjacent` if removed.
    for column in pointsByColumn[:1]:
        for point in column:
            bestPathToPoint[point] = (0, None, 0)

    # Build the table
    for column in pointsByColumn[1:]:
        for point in column:
            # Gather all other points in the perview of search for the current point
            adjacent = list(getAdjacent(pointsByColumn, bestPathToPoint, point.index, minimumLookBack))

            if len(adjacent) == 0:
                print(f"None adjacent to {point}")
                bestPathToPoint[point] = (0, None, 0)
            else:
                bestScore: float
                bestPoint: Point
                bestScore, bestPoint = min(
                    [(score(point, candidatePoint, candidateAngle) + cadidateScore, candidatePoint)
                    for cadidateScore, candidatePoint, candidateAngle in adjacent],
                    key=lambda triplet: triplet[0] # Just minimize by the score
                )
                bestPathToPoint[point] = (bestScore, bestPoint, angleBetweenPoints(bestPoint, point))

    # print(bestPathToPoint)

    # TODO: Search backward in some 2D area for the best path ?
    OPTIMAL_ENDING_WIDTH = 20
    optimalCandidates = list(getAdjacent(pointsByColumn, bestPathToPoint, startingColumn=binary.width, minimumLookBack=OPTIMAL_ENDING_WIDTH))

    # if len(optimalCandidates) == 0:

    _, current = min(
        [(totalScore, point) for totalScore, point, _ in optimalCandidates],
        key=lambda pair: pair[0] # Just minimize by the score
    )

    bestPath = []

    while current is not None:
        bestPath.append(current)
        _, current, _ = bestPathToPoint[current]

    signal = convertPointsToSignal(bestPath) #, width=binary.width)

    # scores = [bestPathToPoint[point][0] ** .5 for point in points]
    # plt.imshow(binary.toColor().data, cmap='Greys')
    # plt.scatter([point.x for point in points], [point.y for point in points], c=scores)
    # # plt.plot(signal, c='purple')
    # plt.show()

    return signal
