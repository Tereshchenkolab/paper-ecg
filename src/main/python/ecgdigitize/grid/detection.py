"""
detection.py
Created May 23, 2021

Converts a color image to binary mask of the grid.
"""
import cv2
import numpy as np

from ..image import BinaryImage, ColorImage
from .. import vision


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
    greyscaleImage = colorImage.toGrayscale()
    binaryImage = greyscaleImage.toBinary(threshold=220)

    signalImage = colorImage.toGrayscale().toBinary() # Mallawaarchi method
    dilatedSignal = cv2.dilate(
        signalImage,
        cv2.getStructuringElement(cv2.MORPH_DILATE, (5,5))
    )

    subtracted: np.ndarray = cv2.subtract(binaryImage, dilatedSignal)

    # <- DEBUG ->
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


def allDarkPixels(colorImage: ColorImage, belowThreshold: int = 230) -> BinaryImage:
    grayscale = colorImage.toGrayscale()

    # Adjusts the exposure of the image so that the most common pixel is pure white
    # This helps to normalize for variation in the greyness of the paper
    adjusted = grayscale.whitePointAdjusted()

    # Now that we have applied some normalization,
    binary = adjusted.toBinary(belowThreshold)

    return binary