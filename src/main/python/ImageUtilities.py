"""
ImageUtilities.py
Created November 9, 2020

-
"""
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
from PyQt5 import QtGui
import scipy.stats as stats


def readImage(path: Path) -> np.ndarray:
    return cv2.imread(str(path.absolute()))


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
