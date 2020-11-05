from typing import Iterable, List, Callable, TypeVar

T = TypeVar('T')


def _acceptableNumber(text: str, negationAllowed=True, periodAllowed=True, containsDigits=False) -> bool:
    """Private helper function to check if a number meets criteria for being a Float/Int.

    Args:
        text (str): The string to check.
        negationAllowed (bool, optional): If a negative sign is ok. Defaults to True.
        periodAllowed (bool, optional): If a period is ok (i.e. float is ok). Defaults to True.
        containsDigits (bool, optional): Do not use. Defaults to False.

    Returns:
        bool: If number meets the criteria.=.
    """
    if text == '':  return containsDigits

    x = text[0]

    if x == '-':
        return negationAllowed and _acceptableNumber(text[1:], False, periodAllowed, containsDigits)
    if x == '.':
        return periodAllowed and _acceptableNumber(text[1:], False, False, containsDigits)
    if x.isdigit():
        return _acceptableNumber(text[1:], False, periodAllowed, True)

    return False


def isFloat(x: str) -> bool:
    return _acceptableNumber(x)


def isInt(x: str) -> bool:
    return _acceptableNumber(x, negationAllowed=True, periodAllowed=False)


def isPositive(x: str) -> bool:
    return _acceptableNumber(x, negationAllowed=False, periodAllowed=False)


def allTrue(elements: List[bool]) -> bool:
    """Checks the truth of an entire list.

    Args:
        elements (List[bool]): A list of boolean values.

    Returns:
        bool: True if all elements are True, otherwise False.
    """
    return elements.count(False) == 0