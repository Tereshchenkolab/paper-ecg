from PyQt5 import QtCore, QtWidgets

from QtWrapper import *


class EditPanelLeadView(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent # the editor widget
        
        self.lead = None

        self.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)

        self.title = QtWidgets.QLabel()
        self.imagePreview = QtWidgets.QLabel()

        self.initUI()

    def initUI(self):

        self.mainlayout = QtWidgets.QVBoxLayout()
        self.mainlayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainlayout.setContentsMargins(5, 5, 5, 5)

        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.mainlayout.addWidget(self.title)

        self.controlsLayout = QtWidgets.QFormLayout()

        self.controlsLayout.addRow(
            Label(
                owner=self,
                name="leadStartTimeLabel",
                text="Start time: "
            ),
            DoubleSpinBox(
                owner=self,
                name="leadStartTimeSpinBox",
                suffix=" ms",
                minVal=0.0,
                maxVal=500.0
            )
        )

        self.mainlayout.addLayout(self.controlsLayout)
        
        self.mainlayout.addWidget(
            PushButton(
                owner=self,
                name="deleteLeadButton",
                text="Delete Lead"
            )
        )

        self.setLayout(self.mainlayout)
        self.leadStartTimeSpinBox.valueChanged.connect(self.startTimeChanged)
        self.deleteLeadButton.clicked.connect(lambda: self.parent.removeLead.emit(self.lead))


    def setValues(self, lead):
        self.lead = lead
        self.setTitle(lead.leadId)
        self.leadStartTimeSpinBox.setValue(lead.leadStartTime)

    def setTitle(self, leadId):
        # self.leadId = leadId
        self.title.setText("Lead " + leadId)

    def startTimeChanged(self):
        print("start time changed: " + str(self.leadStartTimeSpinBox.value()))
        self.parent.leadStartTimeChanged.emit(self.lead.leadId, self.leadStartTimeSpinBox.value())