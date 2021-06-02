from typing import Optional, Union
from dataclasses import dataclass
from enum import Enum

import numpy as np

from ecgdigitize.image import ColorImage
from . import common
from .grid import detection as grid_detection
from .grid import extraction as grid_extraction
from .signal import detection as signal_detection
from .signal.extraction import viterbi
from . import vision


def estimateRotationAngle(image: ColorImage, houghThresholdFraction: float = 0.25) -> Optional[float]:
    binaryImage = grid_detection.thresholdApproach(image)

    houghThreshold = int(image.width * houghThresholdFraction)
    lines = vision.houghLines(binaryImage, houghThreshold)

    angles = common.mapList(lines, vision.houghLineToAngle)
    offsets = common.mapList(angles, lambda angle: angle % 90)
    candidates = common.filterList(offsets, lambda offset: abs(offset) < 30)

    if len(candidates) > 1:
        estimatedAngle = common.mean(candidates)
        return estimatedAngle
    else:
        return None


class SignalDetectionMethod(Enum):
    default = 'default'


class SignalExtractionMethod(Enum):
    default = 'default'


def digitizeSignal(
    image: ColorImage,
    detectionMethod: SignalDetectionMethod = SignalDetectionMethod.default,
    extractionMethod: SignalExtractionMethod = SignalExtractionMethod.default
) -> Union[np.ndarray, common.Failure]:
    # First, convert color image to binary image where signal pixels are turned on (1) and other are off (0)
    if detectionMethod == SignalDetectionMethod.default:
        binary = signal_detection.adaptive(image)
    else:
        raise ValueError("Unrecognized SignalDetectionMethod in `digitizeSignal`")

    # Second, analyze the binary image to produce a signal
    if extractionMethod == SignalExtractionMethod.default:
        signal = viterbi.extractSignal(binary)
    else:
        raise ValueError("Unrecognized SignalExtractionMethod in `digitizeSignal`")

    return signal


class GridDetectionMethod(Enum):
    default = 'default'


class GridExtractionMethod(Enum):
    default = 'default'


def digitizeGrid(
    image: ColorImage,
    detectionMethod: GridDetectionMethod = GridDetectionMethod.default,
    extractionMethod: GridExtractionMethod = GridExtractionMethod.default
) -> Union[float, common.Failure]:  # Returns size of grid in pixels
    # First, convert color image to binary image where grid pixels are turned on (1) and all others are off (0)
    if detectionMethod == GridDetectionMethod.default:
        # Nothing intelligent; just gets all non-white pixels
        binary = grid_detection.allDarkPixels(image)
    else:
        raise ValueError("Unrecognized GridDetectionMethod in `digitizeGrid`")

    # Second, analyze the binary image to estimate the grid spacing (period)
    if extractionMethod == GridExtractionMethod.default:
        gridPeriod = grid_extraction.estimateFrequencyViaAutocorrelation(binary.data)
    else:
        raise ValueError("Unrecognized GridExtractionMethod in `digitizeSignal`")

    return gridPeriod

