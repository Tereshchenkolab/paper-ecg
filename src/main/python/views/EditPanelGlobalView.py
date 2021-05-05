from PyQt5 import QtCore, QtWidgets

from QtWrapper import *


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
                    HorizontalSlider(self, "rotationSlider"),
                    PushButton(self, "autoRotateButton", text="Auto Rotate")
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
                minVal=0.01,
                maxVal=1000.0,
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
                minVal=0.01,
                maxVal=1000.0,
                suffix=" mm/mV"
            )
        )
        # self.controlsLayout.addRow(
        #     Label(
        #         owner=self,
        #         name="processingAlgorithmBoxLabel",
        #         text="Processing algorithm: "
        #     ),
        #     ComboBox(
        #         owner=self,
        #         name="processingAlgorithmComboBox",
        #         items=[
        #             "Option 1",
        #             "Option 2"
        #         ]
        #     )
        # )

        self.mainLayout.addLayout(self.controlsLayout)

        self.mainLayout.addWidget(
            PushButton(
                owner=self,
                name="processDataButton",
                text="Process Lead Data"
            ),
            alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter
        )

        self.setLayout(self.mainLayout)

        self.clearTimeSpinBox()
        self.clearVoltSpinBox()


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

        self.autoRotateButton.clicked.connect(self.editorWidget.autoRotate)

        self.voltScaleSpinBox.valueChanged.connect(lambda: self.editorWidget.gridVoltScaleChanged.emit(self.voltScaleSpinBox.value()))
        self.timeScaleSpinBox.valueChanged.connect(lambda: self.editorWidget.gridTimeScaleChanged.emit(self.timeScaleSpinBox.value()))
        self.processDataButton.clicked.connect(lambda: self.editorWidget.processDataButtonClicked.emit())


    def clearVoltSpinBox(self):
        self.voltScaleSpinBox.setValue(1.0)

    def clearTimeSpinBox(self):
        self.timeScaleSpinBox.setValue(1.0)

    def setValues(self, voltScale, timeScale):
        self.voltScaleSpinBox.setValue(voltScale)
        self.timeScaleSpinBox.setValue(timeScale)
