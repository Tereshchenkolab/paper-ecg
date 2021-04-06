import cv2
import matplotlib.pyplot as plt
from cv2 import imread as loadImage
from functools import partial

from src.main.python.ECGToolkit import Common, GridDetection, Process, SignalDetection, SignalExtraction, Vision, Visualization


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

hSpace, vSpace = Process.extractGridFromImage(testImage, GridDetection.kernelApproach)

rawSignal = Process.extractSignalFromImage(testImage, partial(SignalDetection.mallawaarachchi, useBlur=True), SignalExtraction.naïveHorizontalScan)

plt.figure(figsize=(14,6))
showColorImage(testImage)
plt.plot(rawSignal, c="limegreen")
plt.show()

signal = Process.zeroECGSignal(rawSignal)
print("max:", max(signal), "min:", min(signal), "mean:", Common.mean(signal))