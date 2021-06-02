
from PyQt5 import QtCore, QtGui, QtWidgets
from QtWrapper import *
from ImageUtilities import opencvImageToPixmap

class ImagePreviewDialog(QtWidgets.QDialog):

    def __init__(self, image, leadId):
        super().__init__()
        self.pixmap = opencvImageToPixmap(image)
        self.leadId = leadId
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lead " + str(self.leadId))

        self.layout = QVBoxLayout()
        self.margins = QtCore.QMargins(4, 4, 4, 4)

        self.pixmapLabel = QLabel()
        self.pixmapLabel.setContentsMargins(self.margins)
        self.pixmapLabel.setPixmap(self.pixmap)
        self.pixmapLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.pixmapLabel.setMinimumSize(1, 1)

        self.layout.addWidget(self.pixmapLabel)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def resizeEvent(self, event):
        self.pixmapLabel.resize(self.width()-(self.margins.right()-self.margins.left()), self.height()-(self.margins.top()-self.margins.bottom()))
        self.pixmapLabel.setPixmap(self.pixmap.scaled(self.pixmapLabel.width(), self.pixmapLabel.height(), QtCore.Qt.KeepAspectRatio))
