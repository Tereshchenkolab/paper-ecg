"""
EditorWindow.py
Created November 7, 2020

-
"""

from pathlib import Path

from model.EditableImage import EditableImage
from PyQt5 import QtCore, QtGui, QtWidgets
from QtWrapper import *
from Utility import *

from views.ImageView import *
from views.ROIView import *
from views.EditPanelLeadView import *
from views.EditPanelGlobalView import *


class Editor(QtWidgets.QWidget):

    image = None # The openCV image

    def __init__(self):
        super().__init__()
        self.initUI()
        # self.connectUI()

        # Initialize a single ROI as a demo
        # self.initROI()

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

                    ScrollArea(
                        owner=self,
                        name="scrollArea",
                        horizontalScrollBarPolicy=QtCore.Qt.ScrollBarAlwaysOff,
                        verticalScrollBarPolicy=QtCore.Qt.ScrollBarAsNeeded,
                        widgetIsResizable=True,
                        innerWidget=
                            StackedWidget(
                                owner=self,
                                name="editPanel",
                                widgets=[
                                    Custom(
                                        owner=self,
                                        name="EditPanelGlobalView",
                                        widget=EditPanelGlobalView(self)
                                    ),
                                    Custom(
                                        owner=self,
                                        name="EditPanelLeadView",
                                        widget=EditPanelLeadView()
                                    )
                                ]
                            )
                        )
                    ])
                ]
            )
        )
        self.setEditPanel()

    def setEditPanel(self, roi=None, detailView=False):
        if detailView == True:
            self.EditPanelLeadView.setTitle(roi.leadId)
            self.editPanel.setCurrentIndex(1)
        else:
            self.editPanel.setCurrentIndex(0)

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
            value = self.EditPanelGlobalView.brightnessSlider.value()

        if self.image is not None:
            self.displayImage(self.image.withBrightness(value))

    def adjustContrast(self, value = None):
        if value is None:
            value = self.EditPanelGlobalView.contrastSlider.value()

        if self.image is not None:
            self.displayImage(self.image.withContrast(value))

    def adjustRotation(self, value = None):
        if value is None:
            value = self.EditPanelGlobalView.rotationSlider.value()

        # This slider is scaled up to give more fine control
        value = float(value/10)

        if self.image is not None:
            self.displayImage(self.image.withRotation(value))

    def resetImageEditControls(self):
        # TODO: Implement this (and call when a new image is loaded ... ?)
        # IDEA: Only show the image editing controls when there is a image loaded?
        pass

    def loadImageFromPath(self, path: Path):
        self.image = EditableImage(path)
        self.displayImage(self.image.getPixmap())
        self.onImageAppear()

    def onImageAppear(self):
        """Called when a new image is opened"""
        self.editPanel.show()

        # Adjust zoom to fit image in view
        self.imageViewer.fitInView(QtCore.QRectF(self.image.getPixmap().rect()), QtCore.Qt.KeepAspectRatio)

    def displayImage(self, pixmap):
        self.imageViewer.setImage(pixmap)


