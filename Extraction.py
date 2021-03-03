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

binary = GridDetection.extractGridUsingKernels(testImage)
lines = Vision.houghLines(binary, threshold=80)

overlayImage = Visualization.overlayLines(lines, testImage)
showColorImage(overlayImage)

verticalLines = sorted(Vision.getLinesInDirection(lines, 90))

horizontalLines = sorted(Vision.getLinesInDirection(lines, 0))

distances = Common.calculateDistancesBetweenValues(horizontalLines)
gridSpacing = Common.mode(distances) # Could use median or mode...
print(gridSpacing)

distances = Common.calculateDistancesBetweenValues(verticalLines)
gridSpacing = Common.mode(distances) # Could use median or mode...
print(gridSpacing)




plt.show()
