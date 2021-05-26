"""
detection.py
Created May 23, 2021

Converts a color image to binary mask of the grid.
"""
import cv2
import numpy as np

from .. import vision
from ..signal import detection as signal_detection


def kernelApproach(colorImage):
    binaryImage = vision.binarize(vision.greyscale(colorImage), 240)

    opened = vision.openImage(binaryImage)
    opened = vision.openImage(opened)

    # Subtract the opened image from the binary image
    subtracted = cv2.subtract(binaryImage, opened)

    final = cv2.erode(
        subtracted,
        cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2))
    )

    from ..visualization import Color, displayImages
    displayImages([
        (binaryImage, Color.greyscale, "Binary"),
        (opened, Color.greyscale, "Opened"),
        (subtracted, Color.greyscale, "Subtracted"),
        (final, Color.greyscale, "Final")
    ])

    return final

def thresholdApproach(colorImage, erode=False):
    greyscaleImage = vision.greyscale(colorImage)
    binaryImage = vision.binarize(greyscaleImage, 220)

    signalImage = signal_detection.mallawaarachchi(colorImage, useBlur=True, invert=True)
    dilatedSignal = cv2.dilate(
        signalImage,
        cv2.getStructuringElement(cv2.MORPH_DILATE, (5,5))
    )

    subtracted = cv2.subtract(binaryImage, dilatedSignal)

    # from ..visualization import Color, displayImages
    # displayImages([
    #     (binaryImage, Color.greyscale, "Binary"),
    #     (dilatedSignal, Color.greyscale, "Signal"),
    #     (subtracted, Color.greyscale, "Subtracted"),
    # ])

    if erode:
        final = cv2.erode(
            subtracted,
            cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2))
        )
        return final
    else:
        return subtracted


def allDarkPixels(colorImage: np.ndarray):
    greyscale = vision.greyscale(colorImage)
    #
    adjusted = vision.adjustWhitePoint(greyscale, strength=1.0)
    binary = vision.binarize(adjusted, 230)
    return binary