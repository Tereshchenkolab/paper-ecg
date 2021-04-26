"""
EditorWindow.py
Created November 7, 2020

-
"""
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from ECGToolkit.Process import estimateRotationAngle
from model.EditableImage import EditableImage
from views.ImageView import *
from views.ROIView import *
from views.EditPanelLeadView import *
from views.EditPanelGlobalView import *
from views.ExportFileDialog import *
from QtWrapper import *


class Editor(QtWidgets.QWidget):

    leadStartTimeChanged = QtCore.pyqtSignal(object, float)
    gridVoltScaleChanged = QtCore.pyqtSignal(float)
    gridTimeScaleChanged = QtCore.pyqtSignal(float)
    digitizeButtonClicked = QtCore.pyqtSignal()
    exportPathChosen = QtCore.pyqtSignal(str, str)
    removeLead = QtCore.pyqtSignal(object)

    image = None # The openCV image

    def __init__(self):
        super().__init__()
        self.exportFileDialog = None
        self.initUI()

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
                                        widget=EditPanelLeadView(self)
                                    )
                                ]
                            )
                        )
                    ])
                ]
            )
        )
        self.editPanel.setCurrentIndex(0)

    def showGlobalView(self, voltScale=0.0, timeScale=0.0):
        self.EditPanelGlobalView.setValues(voltScale, timeScale)
        self.editPanel.setCurrentIndex(0)

    def showLeadDetailView(self, lead):
        self.EditPanelLeadView.setValues(lead)
        self.editPanel.setCurrentIndex(1)

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

    def autoRotate(self):
        if self.image is None: return

        angle = estimateRotationAngle(self.image.image)

        if angle is None:
            errorModal = QtWidgets.QMessageBox()
            errorModal.setWindowTitle("Error")
            errorModal.setText("Unable to detect the angle automatically!")
            errorModal.setInformativeText("Use the slider to adjust the rotation manually")
            errorModal.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            errorModal.exec_()

            return

        # Notice: The slider is scaled up by a factor of 10    \/
        self.EditPanelGlobalView.rotationSlider.setValue(angle*10)
        self.adjustRotation()

    def resetImageEditControls(self):
        # TODO: Implement this (and call when a new image is loaded ... ?)
        # IDEA: Only show the image editing controls when there is a image loaded?

        self.EditPanelGlobalView.brightnessSlider.setValue(0)
        self.EditPanelGlobalView.contrastSlider.setValue(0)
        self.EditPanelGlobalView.rotationSlider.setValue(0)
        self.EditPanelGlobalView.voltScaleSpinBox.setValue(0)
        self.EditPanelGlobalView.timeScaleSpinBox.setValue(0)
        self.showGlobalView()

    def loadImageFromPath(self, path: Path):
        self.image = EditableImage(path)
        self.displayImage(self.image.image)
        self.onImageAppear()

    def onImageAppear(self):
        """Called when a new image is opened"""
        self.editPanel.show()

        # Adjust zoom to fit image in view
        self.imageViewer.fitInView(QtCore.QRectF(self.image.getPixmap().rect()), QtCore.Qt.KeepAspectRatio)

    def displayImage(self, image):
        self.imageViewer.setImage(image)

    def openExportFileDialog(self):
        self.exportFileDialog = ExportFileDialog(self)
        self.exportFileDialog.exec_()

    def removeImage(self):
        self.image = None
        self.imageViewer.removeImage()