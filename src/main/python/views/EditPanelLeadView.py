from PyQt5 import QtCore, QtWidgets

from QtWrapper import *


class EditPanelLeadView(QtWidgets.QWidget):
    leadStartTimeChanged = QtCore.pyqtSignal(str, float)
    deleteLeadRoi = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()

        self.parent = parent # the editor widget

        self.leadId = None

        self.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)

        self.initUI()

    def initUI(self):

        VerticalBoxLayout(owner=self, name="mainlayout", margins=(5, 5, 5, 5), contents=[
            Label(
                owner=self,
                name="title",
                text=""
            ),
            FormLayout(owner=self, name="controlsLayout", contents=[
                [
                    Label(
                        owner=self,
                        name="leadStartTimeLabel",
                        text="Start time: "
                    ),
                    DoubleSpinBox(
                        owner=self,
                        name="leadStartTimeSpinBox",
                        suffix=" sec",
                        minVal=0,
                        maxVal=1000
                    )
                ]
            ]),
            PushButton(
                owner=self,
                name="deleteLeadButton",
                text="Delete Lead"
            )
        ])

        self.mainlayout.setAlignment(QtCore.Qt.AlignTop)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(self.mainlayout)
        self.leadStartTimeSpinBox.valueChanged.connect(lambda: self.leadStartTimeChanged.emit(self.leadId, self.leadStartTimeSpinBox.value()))
        self.deleteLeadButton.clicked.connect(lambda: self.deleteLeadRoi.emit(self.leadId))


    def setValues(self, leadId, startTime=0.0):
        self.leadId = leadId
        self.setTitle(leadId)
        self.leadStartTimeSpinBox.setValue(startTime)

    def setTitle(self, leadId):
        self.title.setText("Lead " + leadId)

    def startTimeChanged(self):
        print("start time changed: " + str(self.leadStartTimeSpinBox.value()))
        self.parent.leadStartTimeChanged.emit(self.leadId, self.leadStartTimeSpinBox.value())
