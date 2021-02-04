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

        # Hide panel until an image is loaded
        # self.editPanel.hide()


    def initUI(self):

        self.setLayout(
            HorizontalBoxLayout(self, "main", margins=(0,0,0,0), contents=[
                HorizontalSplitter([

                    Custom(
                        owner=self,
                        name="imageViewer",
                        widget=ImageView()
                    ),

                    TabWidget(
                        owner=self,
                        name="editPanel",
                        tabs=[

                        Tab("Image",
                            ScrollArea(
                                owner=self,
                                name="scrollArea",
                                horizontalScrollBarPolicy=QtCore.Qt.ScrollBarAlwaysOff,
                                verticalScrollBarPolicy=QtCore.Qt.ScrollBarAlwaysOn,
                                widgetIsResizable=True,
                                innerWidget=

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
                                            title="Image Adjustments",
                                            layout=

                                            VerticalBoxLayout(
                                                owner=self,
                                                name="globalGroup1Layout",
                                                contents=[

                                                Label("Brightness"),
                                                HorizontalSlider(self, "brightnessSlider"),
                                                Label("Contrast"),
                                                HorizontalSlider(self, "contrastSlider"),
                                                Label("Rotation"),
                                                HorizontalSlider(self, "rotationSlider"),
                                                PushButton(self, "showBoxButton", text="show bounding box"),
                                                PushButton(self, "hideBoxButton", text="hide bounding box")
                                            ])
                                        )
                                    ])
                                )
                            )
                        ),
                        Tab("Leads",
                            Widget(
                                owner=self,
                                name="leadTab",
                                layout=

                                VerticalBoxLayout(
                                    contents=[
                                        ComboBox(["Lead I", "Lead II", "Lead III"])
                                    ]
                                )
                            )
                        )
                    ])
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

        if self.image is not None:
            self.image.edits.brightness = value
            self.image.applyEdits()
            self.displayImage()


    def adjustContrast(self, value = None):
        if value is None:
            value = self.contrastSlider.value()

        if self.image is not None:
            self.image.edits.contrast = value
            self.image.applyEdits()
            self.displayImage()


    def adjustRotation(self, value = None):
        if value is None:
            value = self.rotationSlider.value()

        # This slider is scaled up to give more fine control
        value = float(value/10)

        if self.image is not None:
            self.image.edits.rotation = value
            self.image.applyEdits()
            self.displayImage()


    def resetImageEditControls(self):
        # TODO: Implement this (and call when a new image is loaded ... ?)
        # IDEA: Only show the image editing controls when there is a image loaded?
        pass


    def loadImageFromPath(self, path: Path):
        self.image = EditableImage(path)
        self.displayImage()
        self.onImageAppear()


    def onImageAppear(self):
        """Called when a new image is opened"""
        self.editPanel.show()

        # Adjust zoom to fit image in view
        self.imageViewer.fitInView()


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
        self.box.setPos(0,0)


    def showBoundingBoxButton(self):
        self.box.show()


    def hideBoundingBoxButton(self):
        self.box.hide()

