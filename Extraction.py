import cv2
import matplotlib.pyplot as plt
from cv2 import imread as loadImage
from functools import partial

from src.main.python.ECGToolkit import Common, GridDetection, Process, SignalDetection, SignalExtraction, Vision, Visualization
from src.main.python.model.LeadModel import Lead
from src.main.python.model.EcgModel import *
from src.main.python.Processing import *


def showGreyscaleImage(image):
    plt.imshow(image, cmap='Greys')
    # plt.show()


def showColorImage(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.show()

ecgData = EcgModel()
ecgData.leads['aVL'] = Lead('aVL', loadImage("leadPictures/slighty-noisey-aVL.png"))
ecgData.leads['II'] = Lead('II', loadImage("leadPictures/II.png"))
ecgData.gridTimeScale = 25
ecgData.gridVoltageScale = 10

leadSignals = convertECGLeads(ecgData)

# signal = leadSignals['aVL']
# plt.figure(figsize=(14,6))
# showColorImage(loadImage("leadPictures/slighty-noisey-aVL.png"))
# plt.plot(signal, c="limegreen")
# plt.show()
# print("max:", max(signal), "min:", min(signal), "mean:", Common.mean(signal))

exportSignals(leadSignals, Path("./test.txt"))