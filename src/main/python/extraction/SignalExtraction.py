"""
SignalExtraction.py
Created February 17, 2021

-
"""


from typing import Any, Generator, Optional, Tuple
import numpy as np


def findFirstLastNonZeroPixels(oneDimImage: np.ndarray) -> Tuple[int, int]:

    def reversedRange(stop):
        return range(stop-1, -1, -1)

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
    # signal = np.zeros(len(columns))

    return np.array(
        [np.mean(
            list(findFirstLastNonZeroPixels(column))
         ) for column in columns]
    )

    # return signal


def horizontalScanLookBehind(image: np.ndarray):
    columns = np.swapaxes(image, 0, 1)
    signal = np.zeros(len(columns))

    for column in columns:
        print(column)

    return signal