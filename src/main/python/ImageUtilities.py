"""
ImageUtilities.py
Created November 9, 2020

-
"""
from typing import Tuple

import cv2
from PyQt5 import QtCore, QtGui


def opencvImageToPixmap(image):
    # SOURCE: https://stackoverflow.com/a/50800745/7737644 (Creative Commons - Credit, share-alike)

    height, width, channel = image.shape
    bytesPerLine = 3 * width

    pixmap = QtGui.QPixmap(
        QtGui.QImage(
            image.data,
            width,
            height,
            bytesPerLine,
            QtGui.QImage.Format_RGB888
        ).rgbSwapped()
    )

    return pixmap


def applyBrightness(inputImage, brightness: int):
    # Source: https://stackoverflow.com/a/50053219/7737644

    if brightness == 0:
        return inputImage.copy()

    if brightness > 0:
        shadow = brightness
        highlight = 255
    else:
        shadow = 0
        highlight = 255 + brightness

    alpha_b = (highlight - shadow) / 255
    gamma_b = shadow

    return cv2.addWeighted(inputImage, alpha_b, inputImage, 0, gamma_b)


def applyContrast(inputImage, contrast: int):
    # Source: https://stackoverflow.com/a/50053219/7737644

    if contrast == 0:
        return inputImage.copy()

    f = 131 * (contrast + 127) / (127 * (131 - contrast))
    alpha_c = f
    gamma_c = 127 * (1 - f)

    return cv2.addWeighted(inputImage, alpha_c, inputImage, 0, gamma_c)


def applyRotation(inputImage, angle: float, border: Tuple[int] = (255,255,255)):
    height, width = inputImage.shape[:2]
    center = (width // 2, height // 2)

    rotationMatrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    rotated = cv2.warpAffine(
        inputImage,
        rotationMatrix,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border,
    )

    return rotated

def pixelToTuple(pixel):
    return (int(pixel[0][0][0]), int(pixel[0][0][1]), int(pixel[0][0][2]))