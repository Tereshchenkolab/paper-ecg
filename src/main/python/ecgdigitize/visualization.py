"""
Visualization.py
Created March 2, 2021

Simplifies viewing images (color/greyscale).
"""
import math
from typing import List, Optional, Sequence, Tuple, Union

import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.arraysetops import isin

from . import common
from .image import Image, ColorImage, GrayscaleImage, BinaryImage


class Color:
    greyscale = 0
    BGR = 1

# Use matplotlib to show an image with greyscale color (2d array)
def displayImage(image: Image, title: str = "") -> None:
    if isinstance(image, ColorImage):
        displayImage = image
        plt.imshow(displayImage.data)
    elif isinstance(image, (GrayscaleImage, BinaryImage)):
        displayImage = image.toColor()
        plt.imshow(displayImage.data, cmap='gray')

    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.title(title)
    plt.show()


def overlayLines(lines: Union[List, np.ndarray], colorImage: ColorImage) -> ColorImage:
    newImage = colorImage.data.copy()
    for rho,theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 10000*(-b))
        y1 = int(y0 + 10000*(a))
        x2 = int(x0 - 10000*(-b))
        y2 = int(y0 - 10000*(a))

        # Draw line on the image
        cv2.line(newImage, (x1,y1), (x2,y2), (85, 19, 248))

    return ColorImage(newImage)


# Display a list of images [(image, color, title)] where color is Color.greyscale or .BGR.
def displayImages(listOfImages: Sequence[Image]) -> None:
    pass
    # count = len(listOfImages)

    # height = math.floor(math.sqrt(count))
    # width = math.ceil(count / height)

    # for index, (image, color, title) in enumerate(listOfImages):
    #     plt.subplot(height, width, index+1)
    #     if color == Color.greyscale:
    #         plt.imshow(image, cmap='gray')
    #     if color == Color.BGR:
    #         plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    #     plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    #     plt.title(title)

    # plt.tight_layout()
    # plt.show()


def overlaySignalOnImage(
    signal: np.ndarray,
    image: ColorImage,
    color: Tuple[np.uint8, np.uint8, np.uint8] = (85, 19, 248),
    lineWidth: int = 3
) -> ColorImage:
    assert len(signal.shape) == 1
    assert isinstance(image, ColorImage)

    def quantize(element: np.float) -> Optional[int]:
        if not np.isnan(element):
            return int(element)
        else:
            return None

    output = image.data.copy()
    quantizedSignal = common.mapList(signal, quantize)

    for first, second in zip(enumerate(quantizedSignal[:-1]), enumerate(quantizedSignal[1:], start=1)):
        if first[1] is not None and second[1] is not None:
            cv2.line(output, first, second, color, thickness=lineWidth)

    return ColorImage(output)
