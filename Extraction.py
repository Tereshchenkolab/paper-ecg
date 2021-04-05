import cv2
import matplotlib.pyplot as plt
from cv2 import imread as loadImage
from cv2 import imwrite as writeImage
import numpy as np

from src.main.python.ECGToolkit import Common, GridDetection, SignalDetection, SignalExtraction, Vision, Visualization


def showGreyscaleImage(image):
    plt.imshow(image, cmap='Greys')
    # plt.show()


def showColorImage(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.show()


# path = "leadPictures/slighty-noisey-aVL-small.png"
path = "leadPictures/slighty-noisey-aVL.png"
# path = "leadPictures/fullscan-I.png"
# path = "data/1480/1480_Page1.jpg"

# path = "../Test Images/Mocks/test2.png"
# path = "../Test Images/Larisa/ZEL297(9).jpg"
# path = "data/700px-AMI_inferior_2.jpg"

testImage = loadImage(path)

gridBinary = GridDetection.kernelApproach(testImage)
lines = Vision.houghLines(gridBinary, threshold=80)

overlayImage = Visualization.overlayLines(lines, testImage)


verticalLines = sorted(Vision.getLinesInDirection(lines, 90))
horizontalLines = sorted(Vision.getLinesInDirection(lines, 0))

distances = Common.calculateDistancesBetweenValues(horizontalLines)
gridSpacing = Common.mode(distances) # Could use median or mode...
print(gridSpacing)

distances = Common.calculateDistancesBetweenValues(verticalLines)
gridSpacing = Common.mode(distances) # Could use median or mode...
print(gridSpacing)

signalBinary = SignalDetection.mallawaarachchi(testImage, useBlur=True)
plt.figure(figsize=(14,6))
showGreyscaleImage(signalBinary)
plt.show()

signal = SignalExtraction.naïveHorizontalScan(signalBinary)

plt.figure(figsize=(14,6))
showColorImage(overlayImage)
plt.plot(signal, c="limegreen")
plt.show()
