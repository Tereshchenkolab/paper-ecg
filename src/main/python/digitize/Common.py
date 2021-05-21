"""
Common.py
Created February 17, 2021

Holds helper functions and types used by all modules.
"""
from collections import Counter
import functools
from typing import Any, Callable, Iterable, Tuple, TypeVar, Union

import numpy as np
from numpy.lib.function_base import median


# Pass through
partial = functools.partial
mean = np.mean
median = np.median

# Types
List = list
Int = int
Float = float
Numeric = Union[Float, Int]

A = TypeVar("A")
B = TypeVar("B")


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
    return flatten(mapList(elements, func))

def filterList(elements: Iterable[A], func: Callable[[A], A]) -> Iterable[A]:
    return list(filter(func, elements))

def sorted(unsortedList):
    unsortedList.sort()
    return unsortedList

def calculateDistancesBetweenValues(sortedList):
    spacings = [y-x for (x, _), (y, _) in zip(sortedList[0:-1], sortedList[1:])]
    return spacings

def mode(data) -> Numeric:
    value, _ = Counter(data).most_common(1)[0]  # returns a list of n most common (i.e., `[(value, count), ...]`)
    return value

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
