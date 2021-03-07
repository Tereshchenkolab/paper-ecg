"""
Common.py
Created February 17, 2021

Holds helper functions and types used by all modules.
"""

from collections import Counter
import functools
from typing import Callable, Iterable, Optional, Tuple, TypeVar, Union

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

A = TypeVar("A")
B = TypeVar("B")
Numeric = Union[Float, Int]


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