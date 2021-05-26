"""
common.py
Created February 17, 2021

Holds helper functions and types used throughout.
"""
from collections import Counter
from functools import partial
from typing import Any, Callable, Iterable, Optional, Tuple, TypeVar, Union
from cv2 import data

from dataclasses import dataclass
import numpy as np
from numpy import mean, median


# Types
List = list
Int = int
Float = float
Numeric = Union[Float, Int]

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class Failure():
    reason: str


def reversedRange(stop):
    return range(stop-1, -1, -1)


def inclusiveRange(start, stop):
    return range(start, stop+1)


def neg(inputValue: Int) -> Int:
    return -1 * inputValue


def upperClamp(value: Numeric, limit: Numeric) -> Numeric:
    return value if (value < limit) else limit


def lowerClamp(value: Numeric, limit: Numeric) -> Numeric:
    return value if (value > limit) else limit


def mapList(elements: Iterable[A], func: Callable[[A], B]) -> Iterable[B]:
    return list(map(func, elements))


def flatten(listOfLists: Iterable[Iterable[A]]) -> Iterable[A]:
    return [e for _list in listOfLists for e in _list]


def flatMap(elements: Iterable[A], func: Callable[[A], Iterable[Iterable[B]]]) -> Iterable[B]:
    # TODO: Fix types
    return flatten(mapList(elements, func))


def filterList(elements: Iterable[A], func: Callable[[A], A]) -> Iterable[A]:
    return list(filter(func, elements))


def calculateDistancesBetweenValues(sortedList):
    spacings = [y-x for (x, _), (y, _) in zip(sortedList[0:-1], sortedList[1:])]
    return spacings


def mode(data) -> Numeric:
    # TODO: Fix types
    value, _ = Counter(data).most_common(1)[0]  # returns a list of n most common (i.e., `[(value, count), ...]`)
    return value


def shiftedPairs(signal, limit: Optional[int] = None):
    limit = len(signal) // 2 if limit is None else limit

    if limit > len(signal) // 2:
        print("Warning: `limit` provide greater than 1/2 length of signal; clamping...")
        limit = len(signal) // 2

    for offset in range(limit):
        if offset == 0:
            yield signal, signal
        else:
            yield signal[:-offset], signal[offset:]


def autocorrelation(signal, limit: int = None):
    return np.array([np.corrcoef(x, y)[0][1] for x, y in shiftedPairs(signal, limit)])


def zipDict(dictionary) -> Iterable[Tuple[Any, Any]]:
    """Zips the (key, value)s of a dict into a list. Can be reversed with the `dict` constructor."""
    return [(key, value) for key,value in dictionary.items()]


def padLeft(elements, count, fillValue=0):
    if type(elements) is np.ndarray:
        return np.pad(elements, (count, 0), constant_values=fillValue)
    else:
        return ([fillValue] * count) + elements


def padRight(elements, count, fillValue=0):
    if type(elements) is np.ndarray:
        return np.pad(elements, (0, count), constant_values=fillValue)
    else:
        return elements + ([fillValue] * count)


def emptyOrNone(elements):
    return len(elements) == 0 or elements is None
