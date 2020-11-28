"""
EditorWindow.py
Created November 7, 2020

-
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from QtWrapper import *
from Utility import *
from ImageView import *

class Editor(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()


    def initUi(self):
        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0) # Adds ~10px by default
 
        self.imageViewer = ImageView(None)

        self.box = ROIItem(self.imageViewer._scene)
        self.box.setRect(300, 100, 400, 200)
        
        # Hide bounding box initially
        self.box.hide()

        self.imageViewer._scene.addItem(self.box)
        print(self.box.isSelected())

        # Initialize tab screen
        tabs = QtWidgets.QTabWidget()

        globalLayout = QtWidgets.QVBoxLayout()

        globalGroup1 = QtWidgets.QGroupBox("Color Adjustments")

        globalGroup1Layout = QtWidgets.QVBoxLayout()
        globalGroup1Layout.addWidget(QtWidgets.QSlider(QtCore.Qt.Horizontal))
        globalGroup1Layout.addWidget(QtWidgets.QSlider(QtCore.Qt.Horizontal))
        globalGroup1Layout.addWidget(QtWidgets.QSlider(QtCore.Qt.Horizontal))

        self.showBoxButton = QtWidgets.QPushButton("show bounding box")
        self.showBoxButton.clicked.connect(self.showBoundingBoxButton)
        self.hideBoxButton = QtWidgets.QPushButton("hide bounding box")
        self.hideBoxButton.clicked.connect(self.hideBoundingBoxButton)

        globalGroup1Layout.addWidget(self.showBoxButton)
        globalGroup1Layout.addWidget(self.hideBoxButton)

        globalGroup1.setLayout(globalGroup1Layout)

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

        # If on MacOS
        if onMacOS:
            tabs.setStyleSheet(
                """
                QTabWidget:left { left: 10px; }
                QTabWidget:right { right: 10px; }
                QTabWidget::pane:top { top: 40px; }
                /* Force it stretch as wide as possible */
                QTabWidget::tab-bar { width: 1000px; }
                QTabWidget::tab-bar:top { top: 20px; }
                QTabWidget::tab-bar:bottom { bottom: 20px; }
                """
            )

            tabsLayout = QtWidgets.QHBoxLayout()
            tabsLayout.setContentsMargins(10,0,10,0)
            tabsLayout.addWidget(tabs)

            tabsContainer = QtWidgets.QWidget()
            tabsContainer.setLayout(tabsLayout)
            tabsContainer.setObjectName("tabsContainer")

            tabsContainer.setStyleSheet("""
                .QWidget#tabsContainer { background: rgba(0,0,0,0.1); }
            """)

            splitter.setStyleSheet("""
                QSplitter::handle:vertical {
                    color: rgba(0,0,0,.2) ;
                    width: 2px;
                }
            """)

            splitter.addWidget(tabsContainer)
        else:
            splitter.addWidget(tabs)

        hbox.addWidget(splitter)
        self.setLayout(hbox)


    def displayImage(self, image):
        self.imageViewer.setImage(QtGui.QPixmap(image))


    def showBoundingBoxButton(self):
        self.box.show()


    def hideBoundingBoxButton(self):
        self.box.hide()

