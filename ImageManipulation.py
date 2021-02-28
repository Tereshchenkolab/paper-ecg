import math
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np


class Color:
    greyscale = 0
    BGR = 1


# Use matplotlib to show an image with BGR color (standard for openCV)
def displayColorImage(image, title=""):
    # plt.subplot(2,2,1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.title(title)
    plt.show()


# Use matplotlib to show an image with greyscale color (2d array)
def displayGreyscaleImage(image, title=""):
    # plt.subplot(2,2,1)
    plt.imshow(image, cmap='gray')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.title(title)
    plt.show()


# Display a list of images [(image, color, title)] where color is Color.greyscale or .BGR.
def displayImages(listOfImages):
    count = len(listOfImages)

    height = math.floor(math.sqrt(count))
    width = math.ceil(count / height)

    for index, (image, color, title) in enumerate(listOfImages):
        plt.subplot(height, width, index+1)
        if color == Color.greyscale:
            plt.imshow(image, cmap='gray')
        if color == Color.BGR:
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        plt.title(title)

    plt.tight_layout()
    plt.show()


def experimentWithKernels():
    imagesToPlot = []

    image = cv2.imread('image.png', 0)

    imagesToPlot.append((image, Color.greyscale, "Original"))

    kernel = np.array([[-1, -1, -1],
                       [ 4, 4,  4],
                       [-1, -1, -1]])

    # Guassian blur
    blurredImage = cv2.filter2D(image, -1, kernel)
    imagesToPlot.append((blurredImage, Color.greyscale, "???"))

    displayImages(imagesToPlot)


def convertToBinary(grayImage):
    # Show the histogram
    # plt.hist(grey.ravel(),256,[0,256]); plt.show()

    # Guassian adaptive threshold
    # binary = cv2.adaptiveThreshold(blurredImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Flat threshold
    binary = cv2.threshold(grayImage, 20, 256, cv2.THRESH_BINARY)

    return binary


def houghLines(binary):
    lines = np.squeeze(cv2.HoughLines(binary, 1, np.pi/180, 150), axis=1)

    return lines


def overlayLines(lines, colorImage):
    for rho,theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 10000*(-b))
        y1 = int(y0 + 10000*(a))
        x2 = int(x0 - 10000*(-b))
        y2 = int(y0 - 10000*(a))

        # Draw line on the image
        cv2.line(colorImage, (x1,y1), (x2,y2), (250,250,150))

    return colorImage


# This could help with extracting the signal from the grid
def openImage(binaryImage):
    # Open the image
    element = cv2.getStructuringElement(cv2.MORPH_OPEN, (3,3))
    eroded = cv2.erode(binaryImage, element)
    opened = cv2.dilate(eroded, element)

    return opened


def extractGridUsingKernels(colorImage):
    gray = cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY) # Uses equation (2) from `2014 - ECG dig IEEE (Mallawaarachchi)`

    _, binaryImage = cv2.threshold(gray, 240, 256, cv2.THRESH_BINARY_INV)

    opened = openImage(binaryImage)
    opened = openImage(opened)

    # Subtract the opened image from the binary image
    subtracted = cv2.subtract(binaryImage, opened)

    final = cv2.erode(
        subtracted,
        cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2))
    )

    displayImages([
        (binaryImage, Color.greyscale, "Binary"),
        (opened, Color.greyscale, "Opened"),
        (subtracted, Color.greyscale, "Subtracted"),
        (final, Color.greyscale, "Final")
    ])

    return final


def traceGridlines(colorImage):
    # Convert to grayscale
    gray = cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY) # Uses equation (2) from `2014 - ECG dig IEEE (Mallawaarachchi)`
    displayImages([(gray, Color.greyscale, "Gray")])

    _, binary = cv2.threshold(gray, 240, 256, cv2.THRESH_BINARY_INV)
    displayImages([(binary, Color.greyscale, "Binary")])

    # Find the lines in the background grid
    gridBinary = extractGridUsingKernels(binary)

    lines = houghLines(binary)
    overlayImage = overlayLines(lines, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))

    displayColorImage(overlayImage)

    return lines


def sorted(unsortedList):
    unsortedList.sort()
    return unsortedList


def calculateDistancesBetweenValues(sortedList):
    spacings = [y-x for (x, _), (y, _) in zip(sortedList[0:-1], sortedList[1:])]
    return spacings


def getLinesInDirection(lines, directionInDegrees):
    # Get only lines in one direction
    return [(rho, theta) for rho, theta in lines if math.isclose(theta * 180/math.pi, directionInDegrees, abs_tol=2)]


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
