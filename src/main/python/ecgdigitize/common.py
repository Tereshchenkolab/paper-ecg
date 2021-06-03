"""
common.py
Created February 17, 2021

Holds helper functions and types used throughout.
"""
from collections import Counter
from typing import Any, Callable, Dict, Iterable, Iterator, Optional, Sequence, Tuple, TypeVar, Union

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


def reversedRange(stop: int) -> Sequence[int]:
    return range(stop-1, -1, -1)


def inclusiveRange(start: int, stop: int) -> Sequence[int]:
    return range(start, stop+1)


def neg(inputValue: Int) -> Int:
    return -1 * inputValue


def upperClamp(value: Numeric, limit: Numeric) -> Numeric:
    return value if (value < limit) else limit


def lowerClamp(value: Numeric, limit: Numeric) -> Numeric:
    return value if (value > limit) else limit


def mapList(elements: Iterable[A], func: Callable[[A], B]) -> 'List[B]':
    return list(map(func, elements))


def flatten(listOfLists: Iterable[Iterable[A]]) -> Iterable[A]:
    return (e for _list in listOfLists for e in _list)


def flatMap(elements: Iterable[A], func: Callable[[A], Iterable[Iterable[B]]]) -> Iterable[B]:
    # TODO: Fix types
    return flatten(mapList(elements, func))


def filterList(elements: Iterable[A], func: Callable[[A], A]) -> 'List[A]':
    return list(filter(func, elements))


def calculateDistancesBetweenValues(sortedList: Union[List, np.ndarray]) -> "List[float]":
    spacings = [y-x for (x, _), (y, _) in zip(sortedList[0:-1], sortedList[1:])]
    return spacings


def mode(data: Union[List, np.ndarray]) -> Numeric:
    # TODO: Fix types
    value, _ = Counter(data).most_common(1)[0]  # returns a list of n most common (i.e., `[(value, count), ...]`)
    return value


def shiftedPairs(signal: Union[List, np.ndarray], limit: Optional[int] = None) -> Iterator[Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]]:
    limit = len(signal) // 2 if limit is None else limit

    if limit > len(signal) // 2:
        raise ValueError("'limit' is greater than half the length of 'signal'")

    for offset in range(limit):
        if offset == 0:
            yield signal, signal
        else:
            yield signal[:-offset], signal[offset:]


def autocorrelation(signal: np.ndarray, limit: int = None) -> np.ndarray:
    return np.array([np.corrcoef(x, y)[0][1] for x, y in shiftedPairs(signal, limit)])


def zipDict(dictionary: Dict) -> Iterable[Tuple[Any, Any]]:
    """Zips the (key, value)s of a dict into a list. Can be reversed with the `dict` constructor."""
    return [(key, value) for key,value in dictionary.items()]


def padLeft(elements: Union[List, np.ndarray], count: int, fillValue: float = 0) -> Union[List, np.ndarray]:
    if type(elements) is np.ndarray:
        return np.pad(elements, (count, 0), constant_values=fillValue)
    else:
        return ([fillValue] * count) + elements


def padRight(elements: Union[List, np.ndarray], count: int, fillValue: float = 0) -> Union[List, np.ndarray]:
    if type(elements) is np.ndarray:
        return np.pad(elements, (0, count), constant_values=fillValue)
    else:
        return elements + ([fillValue] * count)


def emptyOrNone(elements: Sequence[Any]) -> bool:
    return len(elements) == 0 or elements is None
