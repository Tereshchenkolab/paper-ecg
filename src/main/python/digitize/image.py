from typing import Tuple, Union
import dataclasses

import cv2
import numpy as np
import scipy.stats as stats


# TODO: This takes way to long to use
def getMode(inputImage: np.ndarray) -> Tuple[int, int, int]:
        """Gets the mode (most common) pixel color value in the image. Used to fill borders when rotating."""
        firstModes = stats.mode(inputImage, axis=0)
        modeResults = stats.mode(firstModes.mode, axis=1).mode[0][0]
        modeValues = tuple(map(int, modeResults))

        return modeValues


@dataclasses.dataclass(frozen=True)
class Rectangle:
    x: int
    y: int
    width: int
    height: int


@dataclasses.dataclass(frozen=True)
class Boundaries:
    fromX: int
    toX: int
    fromY: int
    toY: int


def cropped(inputImage: np.ndarray, crop: Union[Rectangle, Boundaries]):
    if isinstance(crop, Rectangle):
        x, y, w, h = crop.x, crop.y, crop.width, crop.height
        crop = Boundaries(x, x+w, y, y+h)

    return np.copy(inputImage[crop.fromY:crop.toY, crop.fromX:crop.toX])


def rotated(inputImage: np.ndarray, angle: float, border: Tuple[int] = (255,255,255)):
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
