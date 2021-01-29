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
from model.EditableImage import EditableImage

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

        Widget(
            owner=self,
            name="globalScrollContents",
            horizontalPolicy=QtWidgets.QSizePolicy.Expanding,
            verticalPolicy=QtWidgets.QSizePolicy.Fixed,
            layout=

            VerticalBoxLayout(
                self,
                "globalLayout",
                contents=[

                GroupBox(
                    owner=self,
                    name="globalGroup1",
                    title="Color Adjustments",
                    layout=

                    VerticalBoxLayout(
                        owner=self,
                        name="globalGroup1Layout",
                        contents=[

                        HorizontalSlider(self, "brightnessSlider"),
                        HorizontalSlider(self, "contrastSlider"),
                        HorizontalSlider(self, "rotationSlider"),
                        PushButton(self, "showBoxButton", text="show bounding box"),
                        PushButton(self, "hideBoxButton", text="hide bounding box")
                    ])
                )
            ])
        )

        globalScrollArea = QtWidgets.QScrollArea()
        globalScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        globalScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        globalScrollArea.setWidgetResizable(True)
        # Contents
        globalScrollArea.setWidget(self.globalScrollContents)

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

        # Image editing controls
        self.brightnessSlider.sliderReleased.connect(self.adjustBrightness)
        self.brightnessSlider.sliderMoved.connect(self.adjustBrightness)
        self.brightnessSlider.setRange(-127,127)

        self.contrastSlider.sliderReleased.connect(self.adjustContrast)
        self.contrastSlider.sliderMoved.connect(self.adjustContrast)
        self.contrastSlider.setRange(-127,127)

        self.rotationSlider.sliderReleased.connect(self.adjustRotation)
        self.rotationSlider.sliderMoved.connect(self.adjustRotation)
        self.rotationSlider.setRange(-15 * 10, 15 * 10)




    def numpyToPixMap(self, image):
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


    def adjustBrightness(self, value = None):
        if value is None:
            value = self.brightnessSlider.value()

        self.image.edits.brightness = value
        self.image.applyEdits()
        self.displayImage()


    def adjustContrast(self, value = None):
        if value is None:
            value = self.contrastSlider.value()

        self.image.edits.contrast = value
        self.image.applyEdits()
        self.displayImage()


    def adjustRotation(self, value = None):
        if value is None:
            value = self.rotationSlider.value()

        value = float(value/10)

        self.image.edits.rotation = value
        self.image.applyEdits()
        self.displayImage()


    def loadImageFromPath(self, path: Path):
        self.image = EditableImage(path)
        self.displayImage()


    def displayImage(self):
        pixmap = self.image.pixmap
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

