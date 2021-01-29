"""
Image.py
Created November 9, 2020

-
"""
import ImageUtilities
import cv2
import numpy as np

from pathlib import Path

class EditableImage:

    # Container to organize properties
    class Edits:
        brightness = 0
        contrast = 0
        rotation = 0


    def __init__(self, path: Path):
        self.path = path
        self.image = cv2.imread(str(path))
        self.pixmap = ImageUtilities.opencvImageToPixmap(self.image)

        self.edits = self.Edits()


    def updatePixmap(self, image):
        self.pixmap = ImageUtilities.opencvImageToPixmap(image)


    def applyEdits(self):
        """Applies all edits simultaneously"""

        newImage = ImageUtilities.applyBrightness(self.image, self.edits.brightness)
        newImage = ImageUtilities.applyContrast(newImage, self.edits.contrast)
        newImage = ImageUtilities.applyRotation(newImage, self.edits.rotation)

        self.updatePixmap(newImage)



# if __name__ == "__main__":
