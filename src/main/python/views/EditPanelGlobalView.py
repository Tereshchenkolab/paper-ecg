from PyQt5 import QtGui, QtCore, QtWidgets
from QtWrapper import *
import os, sys

class EditPanelGlobalView(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.editorWidget = parent

        self.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)

        self.initUI()
        self.connectUI()

    def initUI(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.addWidget(
            GroupBox(
                owner=self,
                name="adjustmentsGroup",
                title="Image Adjustments",
                layout=

                VerticalBoxLayout(
                    owner=self,
                    name="adjustmentsGroupLayout",
                    contents=[

                    Label("Brightness"),
                    HorizontalSlider(self, "brightnessSlider"),
                    Label("Contrast"),
                    HorizontalSlider(self, "contrastSlider"),
                    Label("Rotation"),
                    HorizontalSlider(self, "rotationSlider")
                ])
            )
        )

        self.controlsLayout = QtWidgets.QFormLayout()
        self.controlsLayout.addRow(
            Label(
                owner=self,
                name="timeScaleLabel",
                text="Time Scale: "
            ),
            DoubleSpinBox(
                owner=self,
                name="timeScaleSpinBox",
                minVal=0.0,
                maxVal=500.0,
                suffix=" mm/s"
            )
        )
        self.controlsLayout.addRow(
            Label(
                owner=self,
                name="voltScaleLabel",
                text="Voltage Scale: "
            ),
            DoubleSpinBox(
                owner=self,
                name="voltScaleSpinBox",
                minVal=0.0,
                maxVal=500.0,
                suffix=" mm/mV"
            )
        )
        self.controlsLayout.addRow(
            Label(
                owner=self,
                name="processingAlgorithmBoxLabel",
                text="Processing algorithm: "
            ),
            ComboBox(
                owner=self,
                name="processingAlgorithmComboBox",
                items=[
                    "Option 1",
                    "Option 2"
                ]
            )
        )

        self.mainLayout.addLayout(self.controlsLayout)
        self.setLayout(self.mainLayout)
    

    def connectUI(self):

        # Image editing controls
        self.brightnessSlider.sliderReleased.connect(self.editorWidget.adjustBrightness)
        self.brightnessSlider.sliderMoved.connect(self.editorWidget.adjustBrightness)
        self.brightnessSlider.setRange(-127,127)

        self.contrastSlider.sliderReleased.connect(self.editorWidget.adjustContrast)
        self.contrastSlider.sliderMoved.connect(self.editorWidget.adjustContrast)
        self.contrastSlider.setRange(-127,127)

        self.rotationSlider.sliderReleased.connect(self.editorWidget.adjustRotation)
        self.rotationSlider.sliderMoved.connect(self.editorWidget.adjustRotation)
        self.rotationSlider.setRange(-15 * 10, 15 * 10)

