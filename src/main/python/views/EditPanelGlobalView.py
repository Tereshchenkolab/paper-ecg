from PyQt5 import QtCore, QtWidgets

from QtWrapper import *
import model.EcgModel as EcgModel


class EditPanelGlobalView(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()

        self.editorWidget = parent

        self.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)

        self.initUI()
        self.connectUI()

    def initUI(self):

        VerticalBoxLayout(owner=self, name="mainLayout", margins=(5, 5, 5, 5), contents=[
            GroupBox(owner=self, name="adjustmentsGroup", title="Image Adjustments", layout=
                VerticalBoxLayout(owner=self, name="adjustmentsGroupLayout", contents=[
                    Label("Rotation"),
                    HorizontalSlider(self, "rotationSlider"),
                    HorizontalBoxLayout(owner=self, name="buttonLayout", margins=(0, 0, 0, 0), contents=[
                        PushButton(self, "autoRotateButton", text="Auto Rotate"),
                        PushButton(self, "resetRotationButton", text="Reset")
                    ])
                ])
            ),
            GroupBox(owner=self, name="gridScaleGroup", title="Grid Scale", layout=
                FormLayout(owner=self, name="controlsLayout", contents=[
                    (
                        Label(
                            owner=self,
                            name="timeScaleLabel",
                            text="Time Scale: "
                        ),
                        HorizontalBoxLayout(
                            owner=self,
                            name="timeScaleBoxLayout",
                            contents=[
                                SpinBox(
                                    owner=self,
                                    name="timeScaleSpinBox",
                                    minVal=1,
                                    maxVal=1000,
                                    suffix=" mm/s",
                                    defaultValue=EcgModel.Ecg.DEFAULT_TIME_SCALE
                                )
                            ]
                        )
                    ),
                    (
                        Label(
                            owner=self,
                            name="voltScaleLabel",
                            text="Voltage Scale: "
                        ),
                        HorizontalBoxLayout(
                            owner=self,
                            name="voltageScaleBoxLayout",
                            contents=[
                                SpinBox(
                                    owner=self,
                                    name="voltScaleSpinBox",
                                    minVal=1,
                                    maxVal=1000,
                                    suffix=" mm/mV",
                                    defaultValue=EcgModel.Ecg.DEFAULT_VOLTAGE_SCALE
                                )
                            ]
                        )

                    )
                ])
            ),
            PushButton(
                owner=self,
                name="processDataButton",
                text="Process Lead Data"
            ),
            PushButton(
                owner=self,
                name="saveAnnotationsButton",
                text="Save Metadata"
            )
        ])

        self.mainLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.setLayout(self.mainLayout)

        # Align the field labels in the grid scale form to the left
        self.controlsLayout.setFormAlignment(QtCore.Qt.AlignLeft)
        self.controlsLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
        # Force the rows to grow horizontally
        self.controlsLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        # Align the inputs in the grid scale form to the right
        self.timeScaleBoxLayout.setAlignment(QtCore.Qt.AlignRight)
        self.voltageScaleBoxLayout.setAlignment(QtCore.Qt.AlignRight)

        self.clearTimeSpinBox()
        self.clearVoltSpinBox()


    def connectUI(self):
        self.rotationSlider.sliderPressed.connect(self.editorWidget.rotationSliderChanged)
        self.rotationSlider.sliderMoved.connect(self.editorWidget.rotationSliderChanged)
        self.rotationSlider.setRange(-15 * 10, 15 * 10)

        self.autoRotateButton.clicked.connect(self.editorWidget.autoRotate)
        self.resetRotationButton.clicked.connect(self.editorWidget.resetRotation)

        self.voltScaleSpinBox.valueChanged.connect(self.editorWidget.updateVoltScale)
        self.timeScaleSpinBox.valueChanged.connect(self.editorWidget.updateTimeScale)
        self.processDataButton.clicked.connect(self.editorWidget.confirmDigitization)
        self.saveAnnotationsButton.clicked.connect(lambda: self.editorWidget.saveAnnotationsButtonClicked.emit())


    def clearVoltSpinBox(self):
        self.voltScaleSpinBox.setValue(EcgModel.Ecg.DEFAULT_VOLTAGE_SCALE)

    def clearTimeSpinBox(self):
        self.timeScaleSpinBox.setValue(EcgModel.Ecg.DEFAULT_TIME_SCALE)

    def setValues(self, voltScale, timeScale):
        self.voltScaleSpinBox.setValue(voltScale)
        self.timeScaleSpinBox.setValue(timeScale)
        
