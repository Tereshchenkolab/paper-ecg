"""
digitize.py

High-level API.
"""
from math import pi
from . import common
from .grid import detection as grid_detection
from . import vision


def estimateRotationAngle(image, houghThresholdFraction=0.25):
    binaryImage = grid_detection.thresholdApproach(image)

    _, width = image.shape[:2] if len(image.shape) == 3 else image.shape
    houghThreshold = int(width * houghThresholdFraction)
    lines = vision.houghLines(binaryImage, houghThreshold)

    angles = common.mapList(lines, vision.houghLineToAngle)
    offsets = common.mapList(angles, lambda angle: angle % 90)
    candidates = common.filterList(offsets, lambda offset: abs(offset) < 30)

    if len(candidates) > 1:
        estimatedAngle = common.mean(candidates)
        return estimatedAngle
    else:
        return None
