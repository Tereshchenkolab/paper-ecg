import cv2
import matplotlib.pyplot as plt
from cv2 import imread as loadImage

from src.main.python.model.LeadModel import Lead
from src.main.python.model.EcgModel import *
from src.main.python.Conversion import *


def showGreyscaleImage(image):
    plt.imshow(image, cmap='Greys')
    # plt.show()


def showColorImage(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.show()

ecgData = Ecg()
ecgData.leads['aVL'] = Lead('aVL', loadImage("leadPictures/slighty-noisey-aVL.png"))
ecgData.leads['II'] = Lead('II', loadImage("leadPictures/II.png"))
ecgData.gridTimeScale = 25
ecgData.gridVoltageScale = 10

leadSignals, images = convertECGLeads(ecgData)

# signal = leadSignals['aVL']
# plt.figure(figsize=(14,6))
# showColorImage(loadImage("leadPictures/slighty-noisey-aVL.png"))
# plt.plot(signal, c="limegreen")
# plt.show()
# print("max:", max(signal), "min:", min(signal), "mean:", Common.mean(signal))

exportSignals(leadSignals, Path("./test.txt"))