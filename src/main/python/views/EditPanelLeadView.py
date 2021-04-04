from PyQt5 import QtGui, QtCore, QtWidgets
from QtWrapper import *
import os, sys

class EditPanelLeadView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
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
        self.setLayout(self.mainlayout)


    def setTitle(self, leadId):
        self.title.setText("Lead " + leadId.name)

