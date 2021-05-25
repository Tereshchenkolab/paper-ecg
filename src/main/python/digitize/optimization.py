"""
optimization.py
Created February 17, 2021

Methods related to optimization.
"""
from typing import Callable, List, Optional, Tuple, Union


def climb1dHill(xs: List[int], evaluate: Callable[[int], Union[float, int]]) -> int:
    """[summary]

    Args:
        xs (Iterable[int]): The input values to try (in order) ex: [0,1,2,3,4]
        evaluate (Callable[[int], Union[float, int]]): The evaluation function to decide which x is highest

    Returns:
        int: [description]
    """
    evaluations = {}

    def cachedEvaluate(index: int) -> float:
        if index not in evaluations:
            evaluations[index] = evaluate(index)
        return evaluations[index]

    def neighbors(index: int) -> Tuple[Optional[int], Optional[int]]:
        left, right = None, None
        if index > 0:
            left = index - 1
        if index < len(xs) - 1:
            right = index + 1
        return (left, right)

    startIndex = len(xs) // 2
    currentIndex, currentScore = startIndex, cachedEvaluate(xs[startIndex])

    while True:
        left, right = neighbors(currentIndex)
        if left is None or right is None:
            # TODO: Handle this?
            raise NotImplementedError

        leftScore, rightScore = cachedEvaluate(xs[left]), cachedEvaluate(xs[right])

        # If the left step improves our score, head that way
        if left is not None and leftScore > currentScore:
            currentIndex, currentScore = left, leftScore
            continue

        # If the right step improves our score, head that way
        if right is not None and rightScore > currentScore:
            currentIndex, currentScore = right, rightScore
            continue

        # Either we're at an edge or both directions are worse
        return xs[currentIndex]
