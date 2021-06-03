"""
extraction.py
Created February 17, 2021

Provides methods for extracting grid data from images of leads.
"""
from typing import List, Optional, Union

import numpy as np

from . import frequency as grid_frequency
from .. import common
from .. import vision
from ..image import BinaryImage


def traceGridlines(binaryImage: BinaryImage, houghThreshold: int = 80) -> Optional[float]:
    lines = vision.houghLines(binaryImage, houghThreshold)

    # from .. import visualization
    # visualization.displayImage(visualization.overlayLines(lines, binaryImage.toColor()))

    def getDistancesBetween(lines: List[int], inDirection: float = 0) -> List[float]:
        orientedLines = sorted(vision.getLinesInDirection(lines, inDirection))
        return common.calculateDistancesBetweenValues(orientedLines)

    verticalDistances = getDistancesBetween(lines=lines, inDirection=90)
    horizontalDistances = getDistancesBetween(lines=lines, inDirection=0)

    verticalGridSpacing = common.mode(verticalDistances) if len(verticalDistances) > 0 else None
    horizontalGridSpacing = common.mode(horizontalDistances) if len(horizontalDistances) > 0 else None

    if verticalGridSpacing is None:
        return horizontalGridSpacing
    elif horizontalGridSpacing is None:
        return verticalGridSpacing
    else:
        return min([verticalGridSpacing, horizontalGridSpacing])

    # TODO: Use median?
    # TODO: Try using some sort of clustering and picking the smallest cluster below a threshold


def estimateFrequencyViaAutocorrelation(binaryImage: np.ndarray) -> Union[float, common.Failure]:
    # TODO: Assert image is binary. Make typealias for Binary to help?

    columnDensity = np.sum(binaryImage, axis=0)
    rowDensity = np.sum(binaryImage, axis=1)

    columnFrequencyStrengths = common.autocorrelation(columnDensity)
    rowFrequencyStrengths = common.autocorrelation(rowDensity)

    # <-- DEBUG -->
    # from .. import visualization
    # import matplotlib.pyplot as plt
    # plt.plot(columnDensity)
    # visualization.displayGreyscaleImage(binaryImage)
    # plt.plot(columnFrequencyStrengths)
    # plt.plot(rowFrequencyStrengths)
    # plt.show()

    columnFrequency = grid_frequency._estimateFirstPeakLocation(columnFrequencyStrengths)
    rowFrequency = grid_frequency._estimateFirstPeakLocation(rowFrequencyStrengths)

    if columnFrequency and rowFrequency:
        # TODO: Make this configurable or remove:
        # return common.mean([columnFrequency, rowFrequency])
        return columnFrequency
        # return rowFrequency
    elif rowFrequency:
        return rowFrequency
    elif columnFrequency:
        return columnFrequency
    else:
        return common.Failure("Unable to estimate the frequency of the grid in either directions.")

