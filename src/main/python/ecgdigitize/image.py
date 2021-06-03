from pathlib import Path
from typing import Optional, Tuple, Union
import dataclasses

import cv2
import numpy as np
from numpy.lib.arraysetops import isin
import scipy.stats as stats


@dataclasses.dataclass(frozen=True)
class Image:
    data: np.ndarray

    @property
    def height(self):
        return self.data.shape[0]

    @property
    def width(self):
        return self.data.shape[1]


class ColorImage(Image):

    def __post_init__(self) -> None:
        assert isinstance(self.data, np.ndarray)
        assert len(self.data.shape) == 3 and self.data.shape[2] == 3

    def toGrayscale(self):  # -> GrayscaleImage
        """Uses:
            `grey = 0.299 * red + 0.587 * green, 0.114 * blue`

        The "standard method" given in equation (2) by Mallawaarachchi.
        """
        return GrayscaleImage(
            cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        )


class GrayscaleImage(Image):

    def __post_init__(self) -> None:
        assert isinstance(self.data, np.ndarray)
        assert len(self.data.shape) == 2

    def toColor(self) -> ColorImage:
        return ColorImage(cv2.cvtColor(self.data, cv2.COLOR_GRAY2BGR))

    def toBinary(self, threshold: Optional[int] = None, inverse: bool =True):  # -> BinaryImage
        if threshold is None:
            if inverse:
                binaryData: np.ndarray
                _, binaryData = cv2.threshold(self.data, 0, 1, cv2.THRESH_OTSU)
                # Convert from uint8 -> bool, invert truth values, then convert bool -> uint8
                binaryData = np.invert(binaryData.astype('bool')).astype('uint8')
            else:
                _, binaryData = cv2.threshold(self.data, 0, 1, cv2.THRESH_OTSU)
        else:
            if inverse:
                _, binaryData = cv2.threshold(self.data, threshold, 1, cv2.THRESH_BINARY_INV)
            else:
                _, binaryData = cv2.threshold(self.data, threshold, 1, cv2.THRESH_BINARY)

        return BinaryImage(binaryData)

    def normalized(self):  # -> GrayscaleImage:
        # Maps the image to the range [0,1]
        assert self.data.dtype is np.dtype('uint8')
        return GrayscaleImage(self.data / 255)

    def whitePointAdjusted(self, strength: float = 1.0):  # -> GrayscaleImage:
        hist = self.histogram()
        whitePoint = np.argmax(hist)
        whiteScaleFactor = 255 / whitePoint * strength
        return GrayscaleImage(cv2.addWeighted(self.data, whiteScaleFactor, self.data, 0, 0))

    def histogram(self) -> np.ndarray:
        counts, _ = np.histogram(self.data, 255, range=(0,255))
        return counts


class BinaryImage(Image):

    def __post_init__(self) -> None:
        assert isinstance(self.data, np.ndarray)
        assert len(self.data.shape) == 2

    def toColor(self) -> ColorImage:
        return ColorImage(cv2.cvtColor(self.data * 255, cv2.COLOR_GRAY2BGR))

    def toGrayscale(self) -> GrayscaleImage:
        return GrayscaleImage(self.data * 255)


#########################
# Input / Output
#########################


def openImage(path: Path) -> ColorImage:
    assert isinstance(path, Path)
    assert path.exists()

    data = cv2.imread(str(path))
    assert data is not None

    return ColorImage(data)


def saveImage(image: Image, path: Path) -> None:
    assert isinstance(image, (ColorImage, GrayscaleImage, BinaryImage))

    if isinstance(image, ColorImage):
        outputImage = image
    elif isinstance(image, GrayscaleImage):
        outputImage = image.toColor()
    elif isinstance(image, BinaryImage):
        outputImage = image.toColor()
    else:
        raise AssertionError

    return cv2.imwrite(str(path), outputImage.data)


# TODO: This takes waaayyy to long for practical use
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


def cropped(inputImage: Image, crop: Union[Rectangle, Boundaries]) -> Image:
    if isinstance(crop, Rectangle):
        x, y, w, h = crop.x, crop.y, crop.width, crop.height
        crop = Boundaries(x, x+w, y, y+h)

    outputData = inputImage.data.copy()
    croppedData = outputData[crop.fromY:crop.toY, crop.fromX:crop.toX]

    if isinstance(inputImage, ColorImage):
        return ColorImage(croppedData)
    elif isinstance(inputImage, GrayscaleImage):
        return GrayscaleImage(croppedData)
    elif isinstance(inputImage, BinaryImage):
        return BinaryImage(croppedData)
    else:
        raise ValueError


def rotated(inputImage: Image, angle: float, border: Tuple[int, int, int] = (255,255,255)) -> Image:
    center = (inputImage.width // 2, inputImage.height // 2)
    rotationMatrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotatedData = cv2.warpAffine(
        inputImage.data,
        rotationMatrix,
        (inputImage.width, inputImage.height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border,
    )

    if isinstance(inputImage, ColorImage):
        return ColorImage(rotatedData)
    elif isinstance(inputImage, GrayscaleImage):
        return GrayscaleImage(rotatedData)
    elif isinstance(inputImage, BinaryImage):
        return BinaryImage(rotatedData)
    else:
        raise ValueError
