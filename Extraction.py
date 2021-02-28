import cv2
import matplotlib.pyplot as plt
from cv2 import imread as loadImage
from cv2 import imwrite as writeImage
import numpy as np

from src.main.python.extraction import Binarization, SignalExtraction


def showGreyscaleImage(image):
    plt.imshow(image, cmap='Greys')
    # plt.show()


def showColorImage(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.show()

def openImage(binaryImage):
    # Open the image
    element = cv2.getStructuringElement(cv2.MORPH_OPEN, (3,3))
    eroded = cv2.erode(binaryImage, element)
    eroded = cv2.erode(eroded, element)
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    opened = cv2.dilate(eroded, element)

    return opened

def smoothEdges(binaryImage):
    element = cv2.getStructuringElement(cv2.MORPH_DILATE, (3,3))
    smoothed = cv2.erode(binaryImage, element)

    return smoothed

path = "leadPictures/slighty-noisey-aVL-small.png"
# path = "leadPictures/slighty-noisey-aVL.png"
# path = "leadPictures/fullscan-I.png"
# path = "data/1480/1480_Page1.jpg"

path = "../Test Images/Mocks/test2.png"
# path = "../Test Images/Larisa/ZEL297(9).jpg"
# path = "data/700px-AMI_inferior_2.jpg"

testImage = loadImage(path)

binaryImage = Binarization.mallawaarachchiBasic(testImage, useBlur=True)

# plt.show()

# processedImage = openImage(binaryImage)

showGreyscaleImage(binaryImage)

signal = SignalExtraction.traceLines(binaryImage)

# plt.imshow(signal, cmap='spring')
# plt.show()

# print(signal)

plt.plot(signal, c='blueviolet', linewidth=2)
plt.show()