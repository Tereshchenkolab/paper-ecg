import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
import random

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

class Kernel:
    # Static
    @staticmethod
    def guassian(size):
        return np.ones((size,size),np.float32) / (size**2)

def experimentWithBlur():
    image = cv2.imread('image.png', 1)

    imagesToPlot = []

    # Guassian blur
    blurredImage = cv2.filter2D(image, -1, Kernel.guassian(2))
    imagesToPlot.append((blurredImage, Color.BGR, "Guassian Blur @2x2"))

    blurredImage = cv2.filter2D(image, -1, Kernel.guassian(3))
    imagesToPlot.append((blurredImage, Color.BGR, "Guassian Blur @3x3"))

    blurredImage = cv2.filter2D(image, -1, Kernel.guassian(4))
    imagesToPlot.append((blurredImage, Color.BGR, "Guassian Blur @4x4"))

    blurredImage = cv2.filter2D(image, -1, Kernel.guassian(10))
    imagesToPlot.append((blurredImage, Color.BGR, "Guassian Blur @10x10"))

    displayImages(imagesToPlot)


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


def extractGridUsingKernels(binaryImage):
    opened = openImage(binaryImage)

    # Subtract the opened image from the binary image
    final = cv2.subtract(binaryImage, opened)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2))
    final = cv2.erode(final, element)

    displayGreyscaleImage(final, title="final")

    return final


def traceGridlines(colorImage):
    # Convert to grayscale
    gray = cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY) # Uses equation (2) from `2014 - ECG dig IEEE (Mallawaarachchi)`
    # displayImages([(gray, Color.greyscale, "Gray")])

    _, binary = cv2.threshold(gray, 120, 256, cv2.THRESH_BINARY_INV)
    displayImages([(binary, Color.greyscale, "Binary")])

    # Find the lines in the background grid
    gridBinary = extractGridUsingKernels(binary)

    lines = houghLines(gridBinary)
    overlayImage = overlayLines(lines, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))

    # displayColorImage(overlayImage)

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

def cropToGridAndIsolateLinesDemo():
    # path = "../Test Images/ECG Sample Images From Cleveland Clinic/Screen Shot 2020-03-21 at 12.00.50 PM.png"
    # path = "../Test Images/ECG Sample Images From Cleveland Clinic/Screen Shot 2020-03-21 at 12.00.19 PM.png"
    # imagePath = 'fullScan.png'
    # path = 'image.png'

    # Load in image in color
    image = cv2.imread(imagePath, 1)

    gridPartOfImage = cropImageToGrid(image, image)

    # Convert to grayscale
    gray = cv2.cvtColor(gridPartOfImage, cv2.COLOR_BGR2GRAY) # Uses equation (2) from `2014 - ECG dig IEEE (Mallawaarachchi)`
    # displayImages([(gray, Color.greyscale, "Gray")])

    _, binary = cv2.threshold(gray, 100, 256, cv2.THRESH_BINARY_INV)
    # displayImages([(binary, Color.greyscale, "Binary")])

    element = cv2.getStructuringElement(cv2.MORPH_ERODE, (2,2))
    binary = cv2.erode(binary, element)

    # lines = traceGridlines(gridPartOfImage)

    # overlayImage = overlayLines(lines, cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR))
    displayImages([(binary, Color.BGR, "Grid and signal")])

def contiguousRegionsDemo():
    # path = "../Test Images/ECG Sample Images From Cleveland Clinic/Screen Shot 2020-03-21 at 12.00.50 PM.png"
    # path = "../Test Images/ECG Sample Images From Cleveland Clinic/Screen Shot 2020-03-21 at 12.00.19 PM.png"
    # path = 'fullScan.png'
    path = "../Test Images/Larisa/LAU8 tracé 8.JPG"
    # path = "../Test Images/Mocks/test1.png"
    # path = 'image.png'

    # Load in image in color
    image = cv2.imread(path, 1)

    image = cropImageToGrid(image, image)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Uses equation (2) from `2014 - ECG dig IEEE (Mallawaarachchi)`
    displayImages([(gray, Color.greyscale, "Gray")])

    _, binary = cv2.threshold(gray, 100, 256, cv2.THRESH_BINARY_INV)
    # displayImages([(binary, Color.greyscale, "Binary")])

    element = cv2.getStructuringElement(cv2.MORPH_ERODE, (2,2))
    binary = cv2.erode(binary, element)



    # displayImages([(binary, Color.BGR, "Starting point")])

    explored = set()
    width, height = binary.shape

    regions = []

    for y in range(height):
        for x in range(width):
            if binary[x][y] > 0 and (x, y) not in explored:
                contiguousPixels = []
                frontier = [(x, y)]

                while frontier != []:
                    (x,y) = frontier.pop()

                    printStuff = False

                    if (x, y) == (1129,1115):
                        printStuff = True
                        print("Trouble maker >:(")

                    # Check any reason to discard this pixel:

                    # (1) Outside the image boundaries
                    if (x < 0 or x >= width
                        or y < 0 or y >= height):
                        if printStuff: print("Outside boundaries")
                        continue

                    # (2) Already visited
                    if (x,y) in explored:
                        if printStuff: print("Already Visited")
                        continue

                    # (3) Black pixel
                    if binary[x][y] == 0:
                        if printStuff: print("Black")
                        continue

                    # Add this pixel to the region!

                    contiguousPixels.append((x,y))
                    explored.add((x,y))

                    if printStuff: print("Exploring neighbors...")

                    # Explore all of the neighbors of this pixel:

                    # Explore up
                    frontier.append((x, y-1))
                    # Explore left-up
                    frontier.append((x-1, y-1))
                    # Explore left
                    frontier.append((x-1, y))
                    # Explore left-down
                    frontier.append((x-1, y+1))
                    # Explore down
                    frontier.append((x, y+1))
                    # Explore right-down
                    frontier.append((x+1, y+1))
                    # Explore right
                    frontier.append((x+1, y))
                    # Explore right-up
                    frontier.append((x+1, y-1))

                regions.append(contiguousPixels)

    regionMatrices = []

    for region in regions:
        minX = float('inf')
        minY = float('inf')
        maxX = 0
        maxY = 0

        for (x,y) in region:
            if x < minX:
                minX = x
            if y < minY:
                minY = y
            if x > maxX:
                maxX = x
            if y > maxY:
                maxY = y

        regionMatrix = np.zeros((maxX-minX+1, maxY-minY+1), dtype=np.uint8)

        for (x,y) in region:
            regionMatrix[x-minX][y-minY] = 1

        regionMatrices.append(((minX, minY), regionMatrix))

    displayImages([(binary, Color.BGR, "Starting point")])

    # Make an empty color (3-channel) image the same size as the original
    isolatedRegions = np.array([[[0 for _ in range(3)] for _ in range(image.shape[1])] for _ in range(image.shape[0])], dtype=np.uint8)

    for ((x,y), pixels) in regionMatrices:
        colors = [random.randint(75,255) for _ in range(3)]
        for pixelX, pixelRow in enumerate(pixels):
            for pixelY, pixelValue in enumerate(pixelRow):
                if pixelValue != 0:
                    for index, color in enumerate(colors):
                        isolatedRegions[x + pixelX][y + pixelY][index] = color

    displayImages([(isolatedRegions, Color.BGR, "Extracted")])


def thresholdExperiments():
    # path = "../Test Images/ECG Sample Images From Cleveland Clinic/Screen Shot 2020-03-21 at 12.00.50 PM.png"
    path = "../Test Images/ECG Sample Images From Cleveland Clinic/Screen Shot 2020-03-21 at 12.00.19 PM.png"
    # path = 'fullScan.png'
    # path = "../Test Images/Larisa/LAU8 tracé 8.JPG"
    # path = "../Test Images/Mocks/test1.png"
    # path = 'image.png'

    # Load in image in color
    image = cv2.imread(path, 1)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Uses equation (2) from `2014 - ECG dig IEEE (Mallawaarachchi)`
    displayImages([(gray, Color.greyscale, "Gray")])

    # Show the histogram
    plt.hist(gray.ravel(),256,[0,256]); plt.show()

    _, binary = cv2.threshold(gray, 200, 256, cv2.THRESH_BINARY_INV)
    displayImages([(binary, Color.greyscale, "Binary")])

def main():
    thresholdExperiments()

if __name__ == "__main__":
    main()


# NOTE: IDEA ABOUT CONTIGUOUS REGIONS AND IDENTIFYING THE ECG SIGNALS
# I should try writing an algorithm to isolate all of the contiguous regions on connected pixels in a binary image.
# I can use a hash to store visited pixels. I traverse through the image and when I find an active pixel, use dfs to build a sparse array holding all pixels connect to that first one. The whole way through I will be adding things to the hash so I don't try to run this again later.
# I can then use these contiguous regions to identify the ECG signals, by making some feature-extraction functions, like maxHeight, which finds the max instantaneous height of the region when scanning left to right.
# The ECG signals will span a very large width but are very skinny.
# This could also lead to recognizing text by downsampling the region and checking against som predifined character rasters. Would be complicated to identify nearby letters to join together, but seems doable.
