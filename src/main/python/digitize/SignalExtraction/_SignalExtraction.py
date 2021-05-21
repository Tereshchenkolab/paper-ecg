"""
SignalExtraction.py
Created February 17, 2021

Provides methods for converting binary image of signal into signal data.
"""


from typing import Any, Callable, Generator, Iterable, Optional, Tuple, TypeVar, Union
import numpy as np
from math import sqrt, asin, pi
from heapq import heapify, heappop, heappush, heapreplace

from ..Common import *


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


def euclideanDistance(x: int, y: int) -> int:
    return sqrt((x**2) + (y**2))

hypotenuse = euclideanDistance

def distanceBetweenPoints(firstPoint: Tuple[int, int], secondPoint: Tuple[int, int]) -> int:
    return euclideanDistance(firstPoint[0] - secondPoint[0], firstPoint[1] - secondPoint[1])


def angleFromOffsets(x: int, y: int) -> float:
    return asin(y/hypotenuse(x,y)) / pi * 180


def angleBetweenPoints(firstPoint: Tuple[int, int], secondPoint: Tuple[int, int]) -> float:
    deltaX = secondPoint[0] - firstPoint[0]
    deltaY = secondPoint[1] - firstPoint[1]
    return angleFromOffsets(deltaX, deltaY)


def angleSimilarity(firstAngle: float, secondAngle: float) -> float:
    return (180 - abs(secondAngle - firstAngle)) / 180


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

    pointLocations = []

    # Scan horizontally across the image
    for column, pixels in enumerate(columns):
        # Get all points that could be part of a signal
        rows = findContiguousRegionCenters(pixels)
        points = mapList(rows, lambda row: (row, column))

        pointLocations.append(points)

    return pointLocations


class SignalBuilder():
    DEFAULT_ORIENTATION: float = 0.0
    DISTANCE_WEIGHT: float = 0.2

    assert DISTANCE_WEIGHT <= 1 and DISTANCE_WEIGHT >= 0

    def __init__(self, radius, orientationSmoothing) -> None:
        self.points: Iterable[Tuple[int,int]] = []
        self.orientations: Iterable[float] = []
        self.orientationSmoothing: int = orientationSmoothing
        self.radius: int = radius

        self.cacheValidationFinalOrientation: float = None # This tells us if the cache is valid
        self.cachedAveragedOrientation: float = None

    @classmethod
    def startingAt(thisClass, x: int, y: int, radius: int, orientationSmoothing: int = 0):
        newInstance = thisClass(radius, orientationSmoothing)
        point = (x,y)
        newInstance.addPoint(point)
        return newInstance

    @property
    def cacheIsValid(self):
        return self.orientations[-1] == self.cacheValidationFinalOrientation

    def calculateAverageOrientation(self) -> Optional[float]:
        count = len(self.orientations)
        if count == 0: return None

        span = upperClamp(self.orientationSmoothing, count)
        return np.mean(self.orientations[neg(span + 1):])

    @property
    def currentOrientation(self):
        if not self.cacheIsValid:
            self.cachedAveragedOrientation = self.calculateAverageOrientation()

        self.cacheValidationFinalOrientation = self.orientations[-1]
        return self.cachedAveragedOrientation

    def likelihoodOfBeingInSignal(self, point: Tuple[int,int]):
        angle = angleBetweenPoints(self.lastPoint, point)
        angleValue = angleSimilarity(angle, self.currentOrientation)
        distanceValue = (self.radius - distanceBetweenPoints(self.lastPoint, point)) / self.radius
        return (distanceValue * self.DISTANCE_WEIGHT) + (angleValue * (1 - self.DISTANCE_WEIGHT))

    @property
    def lastPoint(self) -> Optional[Tuple[Int, Int]]:
        return self.points[-1] if len(self.points) else None

    def addPoint(self, newPoint: Tuple[int,int]):
        if len(self.points) == 0:
            self.orientations.append(self.DEFAULT_ORIENTATION)
        else:
            newOrientation = angleBetweenPoints(self.points[-1], newPoint)
            self.orientations.append(newOrientation)

        self.points.append(newPoint)


def batch(elements: Iterable[A], batchSize: Int, startAtEveryElement: bool = False, shouldFlatten: bool = True):  # -> Generator[Iterable[A], ???]:
    listLength = len(elements)
    startIndices = range(len(elements) if startAtEveryElement else (len(elements) - batchSize))
    for index in startIndices:
        end = upperClamp(index + batchSize, listLength)
        if shouldFlatten:
            yield flatten(elements[index:end])
        else:
            yield elements[index:end]


def traceLines(image: np.ndarray, radius: int = 12, orientationSmoothing: int = 4):
    pointLocations = getPointLocations(image)
    claimedPoints = set()
    signalBuilders: Iterable[SignalBuilder] = []

    # pointLocationMatrix = np.zeros_like(image)
    # for row, column in flatten(pointLocations):
    #     pointLocationMatrix[row][column] = 1
    # plt.imshow(pointLocationMatrix, cmap='spring')
    # plt.show()

    for column, (points, thisColumnPoints) in enumerate(
        zip(batch(pointLocations, batchSize=radius, startAtEveryElement=True), pointLocations)
    ):
        buildersByPriority = []

        # print(f"=== Column {column} ===")
        # print(points)

        for builderNumber, builder in enumerate(signalBuilders):
            # [print(distanceBetweenPoints(builder.lastPoint, point)) for point in points]

            possiblePoints = filterList(points, lambda point: distanceBetweenPoints(builder.lastPoint, point) <= radius and point[1] == column)

            if len(possiblePoints) == 0:
                continue

            likelihoods = mapList(possiblePoints, builder.likelihoodOfBeingInSignal)

            # Put all the (likelihood, point) pairs in a maxheap
            priorities = mapList(likelihoods, neg)
            bestMatches = list(zip(priorities, possiblePoints))
            heapify(bestMatches)

            # print(builderNumber, bestMatches)

            # If the best match is not the current column, hold off until the next column is processed
            if bestMatches[0][1][1] != column:
                continue

            # `builderNumber` is added as an arbitrary tie-breaker so heapq doesn't try to compare builders with `>`
            heappush(buildersByPriority, (bestMatches[0][0], builderNumber, bestMatches, builder))

        # [print(p) for p in buildersByPriority]

        while len(buildersByPriority) > 0:
            _, builderNumber, bestMatches, builder = buildersByPriority[0]

            # Ignore any builders that are out of points to match with
            if len(bestMatches) == 0:
                heappop(buildersByPriority)
                continue

            _, bestPoint = heappop(bestMatches)

            # Builder's best point is already taken, try the next best
            if bestPoint in claimedPoints:
                # If there is another point and it's still in the current column try that point instead
                if len(bestMatches) > 0 and bestMatches[0][1][1] == column:
                    heapreplace(buildersByPriority, (bestMatches[0][0], builderNumber, bestMatches, builder))
                else:
                    heappop(buildersByPriority)

            if bestPoint not in claimedPoints:
                claimedPoints.add(bestPoint)
                builder.addPoint(bestPoint)

                # This builder has gotten its point for the column
                heappop(buildersByPriority)

        unclaimedPoints = filterList(thisColumnPoints, lambda x: x not in claimedPoints)

        for row, column in unclaimedPoints:
            # print(f"Creating new signal for ({row},{column})")
            signalBuilders.append(SignalBuilder.startingAt(row, column, radius, orientationSmoothing))
            claimedPoints.add((row, column))

    # Select the best signal
    signalSizes = mapList(signalBuilders, lambda b: len(b.points))
    bestSignal = signalBuilders[np.core.fromnumeric.argmax(signalSizes)]

    signal = np.full(image.shape[1], np.nan)

    for row, column in bestSignal.points:
        signal[column] = row

    return signal

