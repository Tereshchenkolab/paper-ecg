"""
EditorWindow.py
Created November 7, 2020

-
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from QtWrapper import *
from Utility import *
from views.ImageView import *

class Editor(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.connectUI()

        # Initialize a single ROI as a demo
        self.initROI()


    def initUI(self):

        self.imageViewer = ImageView(None)

        # Initialize tab screen
        tabs = QtWidgets.QTabWidget()

        globalLayout = QtWidgets.QVBoxLayout()

        globalGroup1 = QtWidgets.QGroupBox("Color Adjustments")

        VerticalBoxLayout(
            self,
            "globalGroup1Layout",
            contents=[
                QtWidgets.QSlider(QtCore.Qt.Horizontal),
                QtWidgets.QSlider(QtCore.Qt.Horizontal),
                QtWidgets.QSlider(QtCore.Qt.Horizontal),
                PushButton(self, "showBoxButton", text="show bounding box"),
                PushButton(self, "hideBoxButton", text="hide bounding box")
            ]
        )

        globalGroup1.setLayout(self.globalGroup1Layout)

        globalLayout.addWidget(globalGroup1)

        globalScrollContents = QtWidgets.QWidget()
        globalScrollContents.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        globalScrollContents.setLayout(globalLayout)

        globalScrollArea = QtWidgets.QScrollArea()
        globalScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        globalScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        globalScrollArea.setWidgetResizable(True)
        globalScrollArea.setWidget(globalScrollContents)

        globalTab = globalScrollArea

        leadTab = QtWidgets.QWidget()

        leadTab.layout = QtWidgets.QVBoxLayout(self)
        leadSelector = QtWidgets.QComboBox()
        leadSelector.addItems(["Lead I", "Lead II", "Lead III"])
        leadTab.layout.addWidget(leadSelector)
        leadTab.setLayout(leadTab.layout)


        # Add tabs
        tabs.addTab(globalTab,"Image")
        tabs.addTab(leadTab,"Leads")

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.imageViewer)
        splitter.addWidget(tabs)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0) # Adds 11px by default
        hbox.addWidget(splitter)

        self.setLayout(hbox)


    def connectUI(self):
        self.showBoxButton.clicked.connect(self.showBoundingBoxButton)
        self.hideBoxButton.clicked.connect(self.hideBoundingBoxButton)


    def displayImage(self, image):
        print("Image width: ", QtGui.QPixmap(image).width(), "height: ", QtGui.QPixmap(image).height())
        self.imageViewer.setImage(QtGui.QPixmap(image))


    def initROI(self):
        self.box = ROIItem(self.imageViewer._scene)
        self.box.setRect(300, 100, 400, 200)

        # Hide bounding box initially
        self.box.hide()

        self.imageViewer._scene.addItem(self.box)
        #self.box.setPos(0,0)
        #print(self.box.isSelected())


    def showBoundingBoxButton(self):
        self.box.show()


    def hideBoundingBoxButton(self):
        self.box.hide()

