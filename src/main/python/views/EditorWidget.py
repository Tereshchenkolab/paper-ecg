"""
EditorWindow.py
Created November 7, 2020

-
"""

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import sys

from QtWrapper import *
from Utility import *
from views.ImageView import *

class Editor(QtWidgets.QWidget):

    image = None # The openCV image

    def __init__(self):
        super().__init__()
        self.initUI()
        self.connectUI()

        # Initialize a single ROI as a demo
        self.initROI()


    def initUI(self):

        self.imageViewer = ImageView(None)

        VerticalBoxLayout(self, "globalLayout", contents=[
            GroupBox(self, "globalGroup1", title="Color Adjustments", layout=
                VerticalBoxLayout(self, "globalGroup1Layout", contents=[
                    QtWidgets.QSlider(QtCore.Qt.Horizontal),
                    QtWidgets.QSlider(QtCore.Qt.Horizontal),
                    QtWidgets.QSlider(QtCore.Qt.Horizontal),
                    PushButton(self, "showBoxButton", text="show bounding box"),
                    PushButton(self, "hideBoxButton", text="hide bounding box")
                ])
            )
        ])

        globalScrollContents = QtWidgets.QWidget()
        globalScrollContents.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        globalScrollContents.setLayout(self.globalLayout)

        globalScrollArea = QtWidgets.QScrollArea()
        globalScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        globalScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        globalScrollArea.setWidgetResizable(True)
        globalScrollArea.setWidget(globalScrollContents)

        globalTab = globalScrollArea

        leadSelector = QtWidgets.QComboBox()
        leadSelector.addItems(["Lead I", "Lead II", "Lead III"])

        leadTab = QtWidgets.QWidget()

        leadTab.layout = QtWidgets.QVBoxLayout(self)
        leadTab.layout.addWidget(leadSelector)

        leadTab.setLayout(leadTab.layout)

        # Initialize tab screen
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(globalTab,"Image")
        tabs.addTab(leadTab,"Leads")

        self.setLayout(
            HorizontalBoxLayout(self, "main", margins=(0,0,0,0), contents=[
                HorizontalSplitter(self, "splitter", [
                    self.imageViewer,
                    tabs
                ])
            ])
        )


    def connectUI(self):
        self.showBoxButton.clicked.connect(self.showBoundingBoxButton)
        self.hideBoxButton.clicked.connect(self.hideBoundingBoxButton)


    def opencvImageToPixMap(self, image):
        # SOURCE: https://stackoverflow.com/a/50800745/7737644 (Creative Commons - Credit, share-alike)
        height, width, channel = self.image.shape
        bytesPerLine = 3 * width

        pixmap = QtGui.QPixmap(
            QtGui.QImage(
                self.image.data,
                width,
                height,
                bytesPerLine,
                QtGui.QImage.Format_RGB888
            ).rgbSwapped()
        )

        return pixmap


    def loadImageFromPath(self, path: Path):
        self.image = cv2.imread(str(path))
        self.displayImage()


    def displayImage(self):
        pixmap = self.opencvImageToPixMap(self.image)
        self.imageViewer.setImage(pixmap)


    def initROI(self):
        self.box = ROIItem(self.imageViewer._scene)
        self.box.setRect(0, 0, 400, 200)
        self.box.setPos(0,0)
        self.box.setPos(0,0)

        # Hide bounding box initially
        self.box.hide()

        self.imageViewer._scene.addItem(self.box)
        #print(self.box.isSelected())


    def showBoundingBoxButton(self):
        self.box.show()


    def hideBoundingBoxButton(self):
        self.box.hide()

