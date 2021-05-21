#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict

import cv2
from cv2 import data
import matplotlib.pyplot as plt
from cv2 import imread as loadImage

from src.main.python.ECGToolkit.SignalExtraction._SignalExtraction import *
from src.main.python.ECGToolkit.SignalDetection import *
from src.main.python.ECGToolkit.Vision import *
from src.main.python.ECGToolkit.Visualization import *



def detectSignal(image, otsuHedging: int = 0.6, kernelSize: int = 3, erosions: int = 1, dilations: int = 1):
    threshold = otsuThresholdSelection(greyscale(image)) * otsuHedging
    _, binary = cv2.threshold(greyscale(image), threshold, 1, cv2.THRESH_BINARY_INV)

    eroded = binary

    for _ in range(erosions):
        eroded = cv2.erode(
            eroded,
            cv2.getStructuringElement(cv2.MORPH_CROSS, (kernelSize, kernelSize))
        )

    dilated = eroded

    for _ in range(dilations):
        dilated = cv2.dilate(
            dilated,
            cv2.getStructuringElement(cv2.MORPH_DILATE, (kernelSize, kernelSize))
        )

    return dilated




# image = loadImage("leadPictures/slighty-noisey-aVL-small.png")
# image = loadImage("leadPictures/007-cropped.jpeg")
# image = loadImage("leadPictures/II.png")
image = loadImage("leadPictures/fullscan-II-cropped.png")

_, width, _ = image.shape

binary = detectSignal(image, otsuHedging=0.6, erosions=0, dilations=0)


# plt.imshow(binary * -1 + np.full_like(binary, 1), cmap='Greys')
# plt.show()


pointsByColumn = getPointLocations(binary)
points = np.array(flatten(pointsByColumn))


# plt.figure(figsize=(20,40))
# plt.imshow(binary * -1 + np.full_like(binary, 1), cmap='Greys')
# plt.scatter(points[:,1], points[:,0], s=1, c='violet')
# plt.show()


# TODO: Make score multiply, or normalize the score by the length of the path

def score(currentPoint: Tuple[int, int], candidatePoint: Tuple[int, int], candidateAngle: float):
    DISTANCE_WEIGHT = 1

    currentAngle = angleBetweenPoints(candidatePoint, currentPoint)
    angleValue = angleSimilarity(currentAngle, candidateAngle)
    distanceValue = distanceBetweenPoints(currentPoint, candidatePoint)

    return (distanceValue * DISTANCE_WEIGHT) + (angleValue * (1 - DISTANCE_WEIGHT))

def getAdjacent(pointsByColumn, bestPathToPoint, startingColumn, minimumLookBack):
    rightColumnIndex = startingColumn
    leftColumnIndex = lowerClamp(startingColumn-minimumLookBack, 0)

    result = flatten(pointsByColumn[leftColumnIndex:rightColumnIndex])

    while len(result) == 0 and leftColumnIndex >= 0:
        leftColumnIndex -= 1
        result = flatten(pointsByColumn[leftColumnIndex:rightColumnIndex])

    for point in result:
        x, y = point
        pointScore, _, pointAngle = bestPathToPoint[y][x]
        yield pointScore, point, pointAngle



minimumLookBack = 1

bestPathToPoint = defaultdict(dict)

# TODO: Allow some leeway either (1) Initialize the first N columns with 0s or (2) Search until some threshold for seeding is met
# Initialize the DP table with base cases (far left side)
for column in pointsByColumn[:1]:
    for x,y in column:
        bestPathToPoint[y][x] = (0, None, 0)

# Build the table
for column in pointsByColumn[1:]:
    # print("Column:", column)
    for x, y in column:
        adjacent = list(getAdjacent(pointsByColumn, bestPathToPoint, y, minimumLookBack))
        if len(adjacent) == 0:
            bestPathToPoint[y][x] = (float('inf'), None, 0)
        else:
            bestScore, bestPoint = min(
                [(score((x,y), candidatePoint, candidateAngle) + cadidateScore, candidatePoint)
                for cadidateScore, candidatePoint, candidateAngle in adjacent]
            )
            bestPathToPoint[y][x] = (bestScore, bestPoint, angleBetweenPoints(bestPoint, (x,y)))

# TODO: Search backward in some 2D area for the best path ?
OPTIMAL_ENDING_WIDTH = 20
optimalCandidates = getAdjacent(pointsByColumn, bestPathToPoint, startingColumn=width, minimumLookBack=OPTIMAL_ENDING_WIDTH)
_, current = min([(totalScore, point) for totalScore, point, _ in optimalCandidates])

print(current)

bestPath = []

while current is not None:
    bestPath.append(current)
    x, y = current
    _, current, _ = bestPathToPoint[y][x]

signal = np.full(width, np.nan)

for row, column in bestPath:
    signal[column] = row

scores = [bestPathToPoint[y][x][0] ** .5 for x,y in points]

plt.imshow((binary * -1 + np.full_like(binary, 1)) * .1, cmap='Greys')
# plt.imshow(greyscale(image), cmap='Greys')
# plt.scatter(points[:,1], points[:,0], c=scores)
plt.plot(signal, c='purple')
plt.show()



# TODO:
# - Treat all pixels as nodes?
# - Add prior weights that incentivize nodes that are in the middle (horizontall and vertically) of other pixels to draw the line to the center of the signal trace