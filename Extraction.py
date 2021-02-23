import cv2
import matplotlib.pyplot as plt
from cv2 import imread as loadImage
from cv2 import imwrite as writeImage

from src.main.python.extraction import Binarization, SignalExtraction


def showGreyscaleImage(image):
    plt.imshow(image, cmap='Greys')
    # plt.show()


def showColorImage(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.show()

path = "leadPictures/slighty-noisey-aVL-small.png"
# path = "leadPictures/slighty-noisey-aVL.png"
# path = "data/1480/1480_Page1.jpg"

# path = "../Test Images/Mocks/test2.png"
# path = "../Test Images/Larisa/ZEL297(9).jpg"
# path = "data/700px-AMI_inferior_2.jpg"

testImage = loadImage(path)

binaryImage = Binarization.mallawaarachchiBasic(testImage, useBlur=True)

showGreyscaleImage(binaryImage)
# plt.show()

#signal = SignalExtraction.horizontalScanLookBehind(binaryImage)
signal = SignalExtraction.horizontalScanLookBehind(binaryImage)

plt.imshow(signal, cmap='spring')
plt.show()

# print(signal)

# plt.plot(signal, c='blueviolet', linewidth=2)
# plt.show()