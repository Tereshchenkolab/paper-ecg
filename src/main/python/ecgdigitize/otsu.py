"""
optimization.py
Created February 17, 2021

Methods related to optimization.
"""

from typing import Callable, List, Optional, Tuple, Union

from ecgdigitize.image import GrayscaleImage


def otsuThreshold(image: GrayscaleImage) -> float:
    """
    A Threshold Selection Method from Gray-Level Histograms - Nobuyuki Otsu
    http://web-ext.u-aizu.ac.jp/course/bmclass/documents/otsu1979.pdf
    """
    assert isinstance(image, GrayscaleImage)

    L = 256
    height, width = image.data.shape
    N = height * width
    n = image.histogram()
    p = n / N

    def ω(k: int) -> float:
        return sum(p[0:k])

    def μ(k: int) -> float:
        return sum([(i+1) * p_i for i, p_i in enumerate(p[0:k])])

    μ_T = μ(L)

    def σ_B(k: int) -> float: # Technically σ^2_B
        numerator   = (μ_T * ω(k) - μ(k))**2
        denominator =  ω(k) * ( 1 - ω(k) )
        return numerator / denominator

    k = climb1dHill(list(range(L)), σ_B)

    return k


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
