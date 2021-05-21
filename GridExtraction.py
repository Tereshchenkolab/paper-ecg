from typing import Optional
import cv2
import matplotlib.pyplot as plt
from cv2 import imread as loadImage

from src.main.python.ECGToolkit.Visualization import *
from src.main.python.ECGToolkit.Vision import *

def shiftedPairs(signal, limit: Optional[int] = None):
    limit = len(signal) // 2 if limit is None else limit

    if limit > len(signal) // 2:
        print("Warning: `limit` provide greater than 1/2 length of signal; clamping...")
        limit = len(signal) // 2

    for offset in range(limit):
        if offset == 0:
            yield signal, signal
        else:
            yield signal[:-offset], signal[offset:]

def autocorrelation(signal, limit: int = None):
    return np.array([np.corrcoef(x, y)[0][1] for x, y in shiftedPairs(signal, limit)])



image = loadImage("leadPictures/slighty-noisey-aVL.png")
# image = loadImage("leadPictures/007-cropped.jpeg")
# image = loadImage("leadPictures/II.png")
# image = loadImage("leadPictures/fullscan-II.png")
greyscale = greyscale(image)
binary = binarize(greyscale, 230)
# binary = invert(image)

horizontalDensity = np.sum(binary, 0)
verticalDensity = np.sum(binary, 1)

plt.plot(horizontalDensity)
# plt.show()


displayImages([
    # (image, Color.BGR, "Image"),
    # (greyscale, Color.greyscale, "Greyscale"),
    (binary, Color.greyscale, "Binary")
])

ac = autocorrelation(horizontalDensity, limit=300)
plt.plot(ac)
plt.show()

plt.plot(verticalDensity)
plt.show()

ac = autocorrelation(verticalDensity)
plt.plot(ac)
plt.show()