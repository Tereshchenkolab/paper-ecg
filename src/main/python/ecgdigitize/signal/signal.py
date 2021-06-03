"""
signal.py
Created February 17, 2021

Provides methods for converting images of leads into signal data.
"""
from typing import Callable
from ecgdigitize.image import BinaryImage, ColorImage
from .. import common

import numpy as np


def extractSignalFromImage(
    image: ColorImage,
    detectionMethod: Callable[[ColorImage], BinaryImage],
    extractionMethod: Callable[[BinaryImage], np.ndarray]
) -> np.ndarray:
    # Note that the signal is mirrored across the x-axis due to the coordinate system of images.
    signalBinary = detectionMethod(image)
    signal = extractionMethod(signalBinary)

    return signal


def verticallyScaleECGSignal(
    signal: np.ndarray,
    gridSizeInPixels: float,
    millimetersPerMilliVolt: float = 10.0,
    gridSizeInMillimeters: float = 1.0
) -> np.ndarray:
    """Scales an extract signal vertically.

    Args:
        signal (np.ndarray): Extracted ECG signal.
        gridSizeInPixels (float): The vertical distance between grid lines in pixels.
        millimetersPerMilliVolt (float, optional): The mm/mV factor. Defaults to 10.0.
        gridSizeInMillimeters (float, optional): The size of the grid lines in mm (typically 1mm or 5mm). NOTE: May be deprecated by the autocorrelation method

    Returns:
        np.ndarray: Scaled signal.
    """
    gridsPerPixel = 1 / gridSizeInPixels                   # Converts size in pixels to size in grid
    millimetersPerGrid = gridSizeInMillimeters             # Converts size in grid to size in mm
    milliVoltsPerMillimeter = 1 / millimetersPerMilliVolt  # Converts size in mm to size in mV
    microVoltsPerMilliVolt = 1000                          # Converts size in mV to size in μV
    microVoltsPerPixel = gridsPerPixel * millimetersPerGrid * milliVoltsPerMillimeter * microVoltsPerMilliVolt
    return signal * microVoltsPerPixel * -1  # Pixels are 0 at the top of the image


def ecgSignalSamplingPeriod(gridSizeInPixels: float, millimetersPerSecond: float = 25.0, gridSizeInMillimeters: float = 1.0) -> float:
    gridsPerPixel = 1 / gridSizeInPixels
    millimetersPerGrid = gridSizeInMillimeters
    secondsPerMillimeter = 1 / millimetersPerSecond
    secondsPerPixel = gridsPerPixel * millimetersPerGrid * secondsPerMillimeter

    return secondsPerPixel


def zeroECGSignal(signal: np.ndarray, zeroingMethod: Callable[[np.ndarray], float]=common.mode) -> np.ndarray:
    zeroPoint = zeroingMethod(signal)

    return signal - zeroPoint
