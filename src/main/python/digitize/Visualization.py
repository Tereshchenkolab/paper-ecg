"""
Visualization.py
Created March 2, 2021

Simplifies viewing images (color/greyscale).
"""
import math

import cv2
import matplotlib.pyplot as plt
import numpy as np

from .Common import lowerClamp, mapList, upperClamp


class Color:
    greyscale = 0
    BGR = 1


# Use matplotlib to show an image with BGR color (standard for openCV)
def displayColorImage(image, title=""):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.title(title)
    plt.show()


# Use matplotlib to show an image with greyscale color (2d array)
def displayGreyscaleImage(image, title=""):
    plt.imshow(image, cmap='gray')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.title(title)
    plt.show()


def overlayLines(lines, colorImage):
    newImage = colorImage.copy()
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
        cv2.line(newImage, (x1,y1), (x2,y2), (85, 19, 248))

    return newImage


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


def overlaySignalOnImage(signal, image, color=(85, 19, 248), lineWidth=3):
    output = image.copy()
    quantizedSignal = mapList(signal, int)

    for first, second in zip(enumerate(quantizedSignal[:-1]), enumerate(quantizedSignal[1:], start=1)):
        cv2.line(output, first, second, color, thickness=lineWidth)

    return output