"""
vision.py
Created March 2, 2021

Contains all general methods for image processing. (Try to keep all the ugly cv2 calls in here.)
"""
from ecgdigitize.image import BinaryImage, GrayscaleImage
import math
from typing import List, Tuple

import cv2
import numpy as np


def houghLines(binary: BinaryImage, threshold: int = 150) -> np.ndarray:
    output = cv2.HoughLines(binary.data, 1, np.pi/180, threshold)

    if output is None:
        return np.array([])
    else:
        return np.squeeze(output, axis=1)


def getLinesInDirection(lines: np.ndarray, directionInDegrees: float) -> List[Tuple[float, float]]:
    # Get only lines in one direction
    return [(rho, theta) for rho, theta in lines if math.isclose(theta * 180/math.pi, directionInDegrees, abs_tol=2)]


def houghLineToAngle(line: Tuple[float, float]):
    rho, theta = line
    return theta * 180/math.pi


# This could help with extracting the signal from the grid
def openImage(binaryImage: BinaryImage):
    # Open the image
    element = cv2.getStructuringElement(cv2.MORPH_OPEN, (3,3))
    eroded = cv2.erode(binaryImage.data, element)
    opened = cv2.dilate(eroded, element)

    return opened


# Gaussian blur
def blur(image: GrayscaleImage, kernelSize: int = 2):

    def guassianKernel(size):
        return np.ones((size,size),np.float32) / (size**2)

    blurred = cv2.filter2D(image.data, -1, guassianKernel(kernelSize))
    return GrayscaleImage(blurred)



