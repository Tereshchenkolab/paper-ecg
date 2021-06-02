"""
naive.py
Created June 1, 2021

Naïve method for extracting digital signal from lead image using "center of mass".
"""
from typing import Iterator, Optional, Tuple
import numpy as np

from ... import common


def findFirstLastNonZeroPixels(oneDimImage: np.ndarray) ->Tuple[Optional[int], Optional[int]]:

    def reverseEnumerate(array: np.ndarray) -> Iterator[Tuple[int, int]]:
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


def extract(image: np.ndarray) -> np.ndarray:
    columns = np.swapaxes(image, 0, 1)
    output  = np.zeros(len(columns))

    for index, column in enumerate(columns):
        top, bottom = findFirstLastNonZeroPixels(column)

        if top is not None and bottom is not None:
            output[index] = (top + bottom) / 2

    return output
