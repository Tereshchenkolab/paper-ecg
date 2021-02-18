import cv2
import matplotlib.pyplot as plt
from cv2 import imread as loadImage
from cv2 import imwrite as writeImage

from src.main.python.extraction import Binarization


def showGreyscaleImage(image):
    plt.imshow(image, cmap='gray')
    plt.show()

def showColorImage(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

path = "leadPictures/slighty-noisey-aVL-small.png"
# path = "leadPictures/slighty-noisey-aVL.png"
# path = "data/1480/1480_Page1.jpg"

testImage = loadImage(path)

binaryImage = Binarization.mallawaarachchiBasic(testImage)

showGreyscaleImage(binaryImage)
