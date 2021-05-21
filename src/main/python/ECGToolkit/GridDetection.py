"""
Common.py
Created March 2, 2021

Converts a color image to binary mask of the grid.
"""
from .Common import *
from .Vision import *
from .SignalDetection import *


def kernelApproach(colorImage):
    binaryImage = binarize(greyscale(colorImage), 240)

    opened = openImage(binaryImage)
    opened = openImage(opened)

    # Subtract the opened image from the binary image
    subtracted = cv2.subtract(binaryImage, opened)

    final = cv2.erode(
        subtracted,
        cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2))
    )

    from .Visualization import Color, displayImages
    displayImages([
        (binaryImage, Color.greyscale, "Binary"),
        (opened, Color.greyscale, "Opened"),
        (subtracted, Color.greyscale, "Subtracted"),
        (final, Color.greyscale, "Final")
    ])

    return final

def thresholdApproach(colorImage, erode=False):
    greyscaleImage = greyscale(colorImage)
    binaryImage = binarize(greyscaleImage, 220)

    signalImage = mallawaarachchi(colorImage, useBlur=True, invert=True)
    dilatedSignal = cv2.dilate(
        signalImage,
        cv2.getStructuringElement(cv2.MORPH_DILATE, (5,5))
    )

    subtracted = cv2.subtract(binaryImage, dilatedSignal)

    # from .Visualization import Color, displayImages
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