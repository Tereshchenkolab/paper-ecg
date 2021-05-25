"""
detection.py
Created May 23, 2021

Converts a color image to binary mask of the lead's curve.
"""
from .. import vision


def mallawaarachchi(image, useBlur: bool = False, invert: bool = True):
    """The most straightforward implementation of binarization from Mallawaarachchi et. al., 2014"""

    # "The first [this] method tends to preserve significantly more information than the second does. For traces with minimal
    #  information, the first method will be more suitable. For newer traces, the second method [CIE-LAB color space] gives
    #  better results."
    greyscaleImage = vision.greyscale(image)

    # TODO: Implement CIE-LAB color space approach

    # Apply blur to reduce noise (⚠️ not in the paper)
    if useBlur:
        blurredImage = vision.blur(greyscaleImage, kernelSize=3)
    else:
        blurredImage = greyscaleImage

    # Get the threshold using the method from Otsu
    threshold = vision.otsuThresholdSelection(blurredImage)

    binaryImage = vision.binarize(blurredImage, threshold, invert)
    return binaryImage
