from . import Common
from . import GridDetection
from . import Vision


def emptyOrNone(elements):
    return len(elements) == 0 or elements is None


def extractSignalFromImage(image, extractionMethod, detectionMethod):
    signalBinary = extractionMethod(image)
    signal = detectionMethod(signalBinary)

    return signal


def extractGridFromImage(image, detectionMethod, spacingReductionMethod=Common.mode):
    """
    Takes a cropped image of a single lead and returns the grid scaling in pixels
    """

    def getSpacingInDirection(lines, direction: int):
        """Takes all of the lines in an image, filters to those oriented in the specified direction, and estimates
        the most likely underlying spacing (some or many lines may be missing so mean is not necessarily suitable)"""

        if emptyOrNone(lines): return None

        orientedLines = Vision.getLinesInDirection(lines, direction)
        if emptyOrNone(orientedLines): return None

        distances = Common.calculateDistancesBetweenValues(sorted(orientedLines))
        if emptyOrNone(distances): return None

        # TODO: Implement an autocorrelation approach or something else to do a better job of this...
        # Could use median or mode...
        gridSpacing = spacingReductionMethod(distances)

        return gridSpacing

    gridBinary = detectionMethod(image)

    # The line process is fixed at this time.
    lines = Vision.houghLines(gridBinary, threshold=80)

    horizontalGridSpacing = getSpacingInDirection(lines, 0)
    verticalGridSpacing   = getSpacingInDirection(lines, 90)

    return (horizontalGridSpacing, verticalGridSpacing)


def extractECGLeadFromImage(image, signalDetectionMethod, signalExtractionMethod, gridDetectionMethod, gridSpacingMethod=Common.mode):
    """[summary]

    Args:
        image (??): Cropped image of lead
        signalExtractionMethod (??):
            Function that accepts a color image and produces a binary image highlighting the signal. (SignalExtraction.___)
        signalDetectionMethod (??):
            Function that accepts a binary image and produces an array of signal values at each horizontal pixel column. (SignalDetection.___)
        gridDetectionMethod (??): Function that accepts a color image and produces a binary image highlighting the grid. (GridExtraction.___)
        gridSpacingMethod (Func[Iterable[int] -> int], optional): Defaults to Common.mode.

    Returns:
        Optional[??]: [description]
    """
    signal = extractSignalFromImage(image, signalDetectionMethod, signalExtractionMethod)

    horSpace, vertSpace = extractGridFromImage(image, gridDetectionMethod, gridSpacingMethod)

    if horSpace is None or vertSpace is None:
        return None