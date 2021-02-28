import cv2
import matplotlib.pyplot as plt
from cv2 import imread as loadImage
from cv2 import imwrite as writeImage
import numpy as np

from src.main.python.extraction import Binarization, SignalExtraction
from ImageManipulation import *

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


# binaryImage = Binarization.mallawaarachchiBasic(testImage, useBlur=False)

# showGreyscaleImage(testImage)
extractGridUsingKernels(testImage)
# plt.show()

# signal = SignalExtraction.traceLines(binaryImage)

# plt.plot(signal, c='blueviolet', linewidth=2)
# plt.show()