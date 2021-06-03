"""
detection.py
Created May 23, 2021

Converts a color image to binary mask of the grid.
"""
import cv2
import numpy as np

from ..image import BinaryImage, ColorImage
from .. import vision
from ..signal.detection import adaptive


def kernelApproach(colorImage: ColorImage) -> BinaryImage:
    binaryImage = colorImage.toGrayscale().toBinary(threshold=240)

    opened: np.ndarray
    opened = vision.openImage(binaryImage.data)
    opened = vision.openImage(opened)

    # Subtract the opened image from the binary image
    subtracted: np.ndarray = cv2.subtract(binaryImage.data, opened)

    final: np.ndarray = cv2.erode(
        subtracted,
        cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2))
    )

    # <- DEBUG ->
    # from ..visualization import Color, displayImages
    # displayImages([
    #     (binaryImage, Color.greyscale, "Binary"),
    #     (opened, Color.greyscale, "Opened"),
    #     (subtracted, Color.greyscale, "Subtracted"),
    #     (final, Color.greyscale, "Final")
    # ])

    return BinaryImage(final)

#
def thresholdApproach(colorImage: ColorImage, erode: bool =False) -> BinaryImage:
    binaryImage = allDarkPixels(colorImage)

    signalImage = adaptive(colorImage)

    dilatedSignal = cv2.dilate(
        signalImage.data,
        cv2.getStructuringElement(cv2.MORPH_DILATE, (5,5))
    )

    subtracted: np.ndarray = cv2.subtract(binaryImage.data, dilatedSignal)

    # <- DEBUG ->
    # from ..visualization import displayImage
    # displayImage(BinaryImage(subtracted).toColor())

    if erode:
        final = cv2.erode(
            subtracted,
            cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2))
        )
        return BinaryImage(final)
    else:
        return BinaryImage(subtracted)


def allDarkPixels(colorImage: ColorImage, belowThreshold: int = 230) -> BinaryImage:
    grayscale = colorImage.toGrayscale()

    # Adjusts the exposure of the image so that the most common pixel is pure white
    # This helps to normalize for variation in the greyness of the paper
    adjusted = grayscale.whitePointAdjusted()

    # Now that we have applied some normalization,
    binary = adjusted.toBinary(belowThreshold)

    return binary