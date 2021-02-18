"""
Binarization.py
Created February 17, 2021

-
"""

import cv2
import numpy as np
from .Common import blur, histogram, standardGreyscaleConversion
from .Optimization import climb1dHill


def binarize(image, threshold):
    _, binaryImage = cv2.threshold(image, threshold, 1, cv2.THRESH_BINARY_INV)
    return binaryImage


def otsuThresholdSelection(image: np.ndarray):
    """
    A Threshold Selection Method from Gray-Level Histograms - Nobuyuki Otsu
    http://web-ext.u-aizu.ac.jp/course/bmclass/documents/otsu1979.pdf
    """

    # assert image.dtype in set(np.uint, uint8, int), f"Expects only integers, not '{image.dtype}'"
    L = 256
    height, width = image.shape
    N = height * width
    n = histogram(image)
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

    k = climb1dHill(range(L), σ_B)

    return k


def mallawaarachchiBasic(image):
    """The most straightforward implementation of binarization from Mallawaarachchi et. al., 2014"""

    # "The first [this] method tends to preserve significantly more information than the second does. For traces with minimal
    # information, the first method will be more suitable. For newer traces, the second method [CIE-LAB color space] gives
    # better results."
    greyscaleImage = standardGreyscaleConversion(image)

    # Apply blur to reduce noise (⚠️ not in the paper)
    blurredImage = blur(greyscaleImage, kernelSize=3)

    # Get the threshold using the method from Otsu
    # TODO: What about using greyscale for threshold?
    threshold = otsuThresholdSelection(blurredImage)

    binaryImage = binarize(blurredImage, threshold)
    return binaryImage



