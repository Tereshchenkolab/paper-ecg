"""
Image.py
Created November 9, 2020

-
"""
import ImageUtilities
import cv2
import numpy as np
import scipy.stats as stats

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

        # Rudimentary caching of the rotated image
        self.rotatedImage = None

        self.edits = self.Edits()
        self.priorEdits = None

        self.mode = self.getMode()

    def getMode(self):
        """Gets the mode (most common) pixel color value in the image. Used to fill borders when rotating."""
        firstModes = stats.mode(self.image, axis=0)
        modeResults = stats.mode(firstModes.mode, axis=1)
        modePixel = np.array(modeResults.mode)
        modeValues = ImageUtilities.pixelToTuple(modePixel)

        return modeValues

    def getPixmap(self):
        return ImageUtilities.opencvImageToPixmap(self.image)

    def withBrightness(self, brightness):
        self.edits.brightness = brightness
        return self.applyColorAlteration()

    def withContrast(self, contrast):
        self.edits.contrast = contrast
        return self.applyColorAlteration()

    def withRotation(self, rotation):
        self.edits.rotation = rotation
        return self.applyRotation()

    def applyColorAlteration(self):
        image = self.image if self.rotatedImage is None else self.rotatedImage

        brightenedImage = ImageUtilities.applyBrightness(image, self.edits.brightness)
        coloredImage = ImageUtilities.applyContrast(brightenedImage, self.edits.contrast)

        return coloredImage

    def applyRotation(self):
        rotatedImage = ImageUtilities.applyRotation(self.image, self.edits.rotation, border=self.mode)

        # Update the cache with the current rotation
        self.rotatedImage = rotatedImage

        # Apply the coloration edits on top of the rotation adjustment
        brightenedImage = ImageUtilities.applyBrightness(rotatedImage, self.edits.brightness)
        coloredImage = ImageUtilities.applyContrast(brightenedImage, self.edits.contrast)

        return coloredImage
