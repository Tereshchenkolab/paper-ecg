"""
vision.py
Created March 2, 2021

Contains all general methods for image processing. (Try to keep all the ugly cv2 calls in here.)
"""
import math
from typing import Tuple

import cv2
import numpy as np

from . import optimization


def houghLines(binary: np.ndarray, threshold: int = 150):
    output = cv2.HoughLines(binary, 1, np.pi/180, threshold)

    if output is None:
        return []
    else:
        return np.squeeze(output, axis=1)


def getLinesInDirection(lines: np.ndarray, directionInDegrees: float):
    # Get only lines in one direction
    return [(rho, theta) for rho, theta in lines if math.isclose(theta * 180/math.pi, directionInDegrees, abs_tol=2)]


def houghLineToAngle(line: Tuple[float, float]):
    rho, theta = line
    return theta * 180/math.pi


# This could help with extracting the signal from the grid
def openImage(binaryImage: np.ndarray):
    # Open the image
    element = cv2.getStructuringElement(cv2.MORPH_OPEN, (3,3))
    eroded = cv2.erode(binaryImage, element)
    opened = cv2.dilate(eroded, element)

    return opened


# Gaussian blur
def blur(greyImage: np.ndarray, kernelSize: int = 2):
    assert len(greyImage.shape) == 2, "Must be greyscale!"

    def guassianKernel(size):
        return np.ones((size,size),np.float32) / (size**2)

    return cv2.filter2D(greyImage, -1, guassianKernel(kernelSize))


def adjustWhitePoint(greyscaleImage: np.ndarray, strength: float = 1.0):
    hist = histogram(greyscaleImage)
    whitePoint = np.argmax(hist)
    whiteScaleFactor = 255 / whitePoint * strength
    return cv2.addWeighted(greyscaleImage, whiteScaleFactor, greyscaleImage, 0, 0)


def greyscale(colorImage: np.ndarray):
    """Uses:
        `grey = 0.299 * red + 0.587 * green, 0.114 * blue`

    The "standard method" given in equation (2) by Mallawaarachchi.
    """
    return cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY)


def binarize(greyscaleImage, threshold, inverse=True):
    assert len(greyscaleImage.shape) == 2, "Must be greyscale!"

    if inverse:
        _, binaryImage = cv2.threshold(greyscaleImage, threshold, 1, cv2.THRESH_BINARY_INV)
        return binaryImage
    else:
        _, binaryImage = cv2.threshold(greyscaleImage, threshold, 1, cv2.THRESH_BINARY)
        return binaryImage


def invert(greyscaleImage: np.ndarray):
    assert len(greyscaleImage.shape) == 2
    raise NotImplementedError


def histogram(greyImage: np.ndarray):
    counts, values = np.histogram(greyImage, 255, range=(0,255))
    return counts


def normalizeGreyscale(image: np.ndarray):
    return image / 255


def otsuThresholdSelection(image: np.ndarray):
    """
    A Threshold Selection Method from Gray-Level Histograms - Nobuyuki Otsu
    http://web-ext.u-aizu.ac.jp/course/bmclass/documents/otsu1979.pdf
    """

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

    k = optimization.climb1dHill(list(range(L)), σ_B)

    return k
