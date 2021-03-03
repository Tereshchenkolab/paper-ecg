import cv2
import numpy as np

# Super janky but makes backwards compatibility easier
from src.main.python.ECGToolkit.Vision import getLinesInDirection
from src.main.python.ECGToolkit.Visualization import *
from src.main.python.ECGToolkit.Common import *
from src.main.python.ECGToolkit.GridDetection import *


def removeNonGridLines(lines, threshold):

    def removeNonGridLinesInDirection(lines, directionInDegrees, threshold):
        gridLines = []

        linesInDirection = sorted(getLinesInDirection(lines, directionInDegrees))

        distances = calculateDistancesBetweenValues(linesInDirection)
        gridSpacing = np.median(distances) # Could use mode...

        # Find lines not aligned to grid
        for (linePosition, theta), spaceBefore, spaceAfter in zip(linesInDirection, [None] + distances, distances + [None]):
            agreementWithAllLines = sum([abs(linePosition-otherLinePosition) % gridSpacing for otherLinePosition, _ in linesInDirection])/(len(linesInDirection))

            agreementWithBefore = float("inf")
            agreementWithAfter  = float("inf")

            if spaceBefore is not None:
                agreementWithBefore = spaceBefore % gridSpacing

            if spaceAfter is not None:
                agreementWithAfter = spaceAfter % gridSpacing

            if min(agreementWithBefore, agreementWithAfter, agreementWithAllLines) < threshold:
                gridLines.append((linePosition, theta))

        return gridLines

    # Remove horizontal lines and vertical lines
    return removeNonGridLinesInDirection(lines, 0, threshold) + removeNonGridLinesInDirection(lines, 90, threshold)


def cropImageToGrid(colorImage, imageToCrop):
    lines = traceGridlines(colorImage)

    gridLines = removeNonGridLines(lines, 2)

    horizontalLines = sorted(getLinesInDirection(gridLines, 90))
    verticalLines = sorted(getLinesInDirection(gridLines, 0))

    gridTop, _ = horizontalLines[0]
    gridBottom, _ = horizontalLines[-1]
    gridLeft, _ = verticalLines[0]
    gridRight, _ = verticalLines[-1]

    print(gridTop, gridBottom, gridLeft, gridRight)

    croppedImage = imageToCrop.copy()[int(gridTop):int(gridBottom), int(gridLeft):int(gridRight)]

    # Load in image in color
    # displayColorImage(croppedImage)

    return croppedImage


def cropToGridAndIsolateLinesDemo(image):
    # path = "../Test Images/ECG Sample Images From Cleveland Clinic/Screen Shot 2020-03-21 at 12.00.50 PM.png"
    # path = "../Test Images/ECG Sample Images From Cleveland Clinic/Screen Shot 2020-03-21 at 12.00.19 PM.png"
    # imagePath = 'fullScan.png'
    # path = 'image.png'

    # gridPartOfImage = cropImageToGrid(image, image)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Uses equation (2) from `2014 - ECG dig IEEE (Mallawaarachchi)`
    # displayImages([(gray, Color.greyscale, "Gray")])

    _, binary = cv2.threshold(gray, 20, 256, cv2.THRESH_BINARY_INV)
    # # displayImages([(binary, Color.greyscale, "Binary")])

    element = cv2.getStructuringElement(cv2.MORPH_ERODE, (2,2))
    binary = cv2.erode(binary, element)

    lines = traceGridlines(image)

    # overlayImage = overlayLines(lines, cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR))
    # displayImages([(binary, Color.BGR, "Grid and signal")]) # , (overlayImage, Color.BGR, "overlayImage")])
