"""
Common.py
Created February 17, 2021

-
"""

import cv2
import numpy as np


# Guassian blur
def blur(greyImage, kernelSize: int = 2):
    def guassianKernel(size):
        return np.ones((size,size),np.float32) / (size**2)

    return cv2.filter2D(greyImage, -1, guassianKernel(kernelSize))


def standardGreyscaleConversion(image: np.ndarray):
    """Uses:
        `grey = 0.299 * red + 0.587 * green, 0.114 * blue`

    The "standard method" given in equation (2) by Mallawaarachchi.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def histogram(greyImage: np.ndarray):
    bins = 256
    lightnesses = greyImage.ravel()
    histogram = np.array(
        [
            (lightnesses == i).sum() for i in range(bins)
        ]
    )
    return histogram


def normalizeGreyscale(image: np.ndarray):
    return image / 255
