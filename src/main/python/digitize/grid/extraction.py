"""
extraction.py
Created February 17, 2021

Provides methods for extracting grid data from images of leads.
"""
from typing import Optional, Union

import numpy as np
import scipy.signal
import scipy.interpolate

from .. import common
from .. import vision


def traceGridlines(binaryImage, houghThreshold=80):
    lines = vision.houghLines(binaryImage, houghThreshold)

    def getDistancesBetween(lines, inDirection=0):
        orientedLines = sorted(vision.getLinesInDirection(lines, inDirection))
        return common.calculateDistancesBetweenValues(orientedLines)

    verticalDistances = getDistancesBetween(lines=lines, inDirection=90)
    horizontalDistances = getDistancesBetween(lines=lines, inDirection=0)

    verticalGridSpacing, horizontalGridSpacing = common.mode(verticalDistances), common.mode(horizontalDistances)

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

    def findFirstPeak(signal: np.ndarray, minHeight: float = 0.3, prominence: float = 0.05) -> Optional[int]:
        peaks, _ = scipy.signal.find_peaks(signal, prominence=prominence, height=minHeight)
        if len(peaks) == 0:
            return None
        else:
            return peaks[0]

    def estimateFirstPeakLocation(signal: np.ndarray, interpolationRadius: int = 2, interpolationGranularity: float = 0.01):
        assert interpolationRadius >= 1

        index = findFirstPeak(signal)
        if index is None:
            return None

        # Squeeze out a little more accuracy by fitting a quadratic to the points around the peak then finding the maximum
        start, end = index - interpolationRadius, index + interpolationRadius
        func = scipy.interpolate.interp1d(range(start, end + 1), signal[start:end + 1], kind='quadratic')
        newX = np.arange(start, end, interpolationGranularity)
        newY = func(newX)

        newPeak = newX[np.argmax(newY)]

        # <-- DEBUG -->
        # import matplotlib.pyplot as plt
        # plt.plot(range(start, end + 1), signal[start:end + 1])
        # plt.plot(newX, newY)
        # plt.show()

        return newPeak

    columnDensity = np.sum(binaryImage, axis=0)
    rowDensity = np.sum(binaryImage, axis=1)

    columnFrequencyStrengths = common.autocorrelation(columnDensity)
    rowFrequencyStrengths = common.autocorrelation(rowDensity)

    # <-- DEBUG -->
    # from . import Visualization
    # import matplotlib.pyplot as plt
    # plt.plot(columnDensity)
    # Visualization.displayGreyscaleImage(binaryImage)
    # plt.plot(columnFrequencyStrengths)
    # plt.plot(rowFrequencyStrengths)
    # plt.show()

    columnFrequency = estimateFirstPeakLocation(columnFrequencyStrengths)
    rowFrequency = estimateFirstPeakLocation(rowFrequencyStrengths)

    if columnFrequency and rowFrequency:
        # TODO: Make this configurable or remove:
        # return common.mean([columnFrequency, rowFrequency])
        # return columnFrequency
        return rowFrequency
    elif columnFrequency is None:
        return rowFrequency
    elif rowFrequency is None:
        return columnFrequency
    else:
        return common.Failure("Unable to estimate the frequency of the grid in either directions.")

