from . import Common
from . import GridDetection
from . import Vision


def estimateRotationAngle(image, houghThreshold=80):
    binaryImage = GridDetection.kernelApproach(image)
    lines = Vision.houghLines(binaryImage, houghThreshold)
    angles = Common.mapList(lines, Vision.houghLineToAngle)
    offsets = Common.mapList(angles, lambda angle: angle % 90)
    candidates = Common.filterList(offsets, lambda offset: abs(offset) < 30)

    if len(candidates) > 1:
        return Common.mean(candidates)
    else:
        return None


def extractSignalFromImage(image, detectionMethod, extractionMethod):
    signalBinary = detectionMethod(image)
    signal = extractionMethod(signalBinary)

    return signal


def extractGridFromImage(image, detectionMethod, spacingReductionMethod=Common.mode):
    """Takes a cropped image of a single lead and returns the grid scaling in pixels

    Args:
        image (??): 2d color image of the lead
        detectionMethod (??): Function that converts a 2d color image into a binary image where the grid is highlighted.
        spacingReductionMethod (??, optional):Takes a list of distances between detected grid lines and estimates
                the grid size (note that some lines may be missing). Defaults to Common.mode.
    """
    def getSpacingInDirection(lines, direction: int):
        """Takes all of the lines in an image, filters to those oriented in the specified direction, and estimates
        the most likely underlying spacing (some or many lines may be missing so mean is not necessarily suitable)"""

        if Common.emptyOrNone(lines): return None

        orientedLines = Vision.getLinesInDirection(lines, direction)
        if Common.emptyOrNone(orientedLines): return None

        distances = Common.calculateDistancesBetweenValues(sorted(orientedLines))
        if Common.emptyOrNone(distances): return None

        # TODO: Implement an autocorrelation approach or something else to do a better job of this (median?)...
        gridSpacing = spacingReductionMethod(distances)

        return gridSpacing

    gridBinary = detectionMethod(image)

    # TODO: Modularize the line extraction process.
    lines = Vision.houghLines(gridBinary, threshold=80)

    horizontalGridSpacing = getSpacingInDirection(lines, 0)
    verticalGridSpacing   = getSpacingInDirection(lines, 90)

    return (horizontalGridSpacing, verticalGridSpacing)


def verticallyScaleECGSignal(signal, gridSizeInPixels: float, millimetersPerMilliVolt: float = 10.0, gridSizeInMillimeters: float = 1.0):
    """Scales an extract signal vertically.

    Args:
        signal (np.ndarray): Extracted ECG signal.
        gridSizeInPixels (float): The vertical distance between grid lines in pixels.
        millimetersPerMilliVolt (float, optional): The mm/mV factor. Defaults to 10.0.
        gridSize (float, optional): The size of the grid in mm (typically 1mm or 5mm). Defaults to 1.0.

    Returns:
        np.ndarray: Scaled signal.
    """
    gridsPerPixel = 1 / gridSizeInPixels
    millimetersPerGrid = gridSizeInMillimeters
    milliVoltsPerMillimeter = 1 / millimetersPerMilliVolt
    milliVoltsPerPixel = gridsPerPixel * millimetersPerGrid * milliVoltsPerMillimeter

    return signal * milliVoltsPerPixel


def ecgSignalSamplingPeriod(gridSizeInPixels: float, millimetersPerSecond: float = 25.0, gridSizeInMillimeters: float = 1.0):
    gridsPerPixel = 1 / gridSizeInPixels
    millimetersPerGrid = gridSizeInMillimeters
    secondsPerMillimeter = 1 / millimetersPerSecond
    secondsPerPixel = gridsPerPixel * millimetersPerGrid * secondsPerMillimeter

    return secondsPerPixel


def zeroECGSignal(signal, zeroingMethod=Common.mode):
    zeroPoint = zeroingMethod(signal)

    return signal - zeroPoint
