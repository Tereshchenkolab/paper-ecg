"""
EditorWindow.py
Created November 7, 2020

-
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from QtWrapper import *
from Utility import *

class Editor(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()


    def initUi(self):
        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0) # Adds ~10px by default

        self.imageWidget = QtWidgets.QLabel()
        self.imageWidget.setGeometry(0, 0, 200, 200)
        self.imageWidget.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.imageWidget.setScaledContents(True)

        self.box = BoundingBox(self.imageWidget)
        self.box.setGeometry(150, 150, 150, 150)

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
        splitter.addWidget(self.imageWidget)
        print("image widget position: ", self.imageWidget.pos())

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
        self.imageWidget.setPixmap(QtGui.QPixmap(image))

    def showBoundingBoxButton(self):
        self.box.showBoundingBox()

    def hideBoundingBoxButton(self):
        self.box.hideBoundingBox()


class BoundingBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BoundingBox, self).__init__(parent)

        self._box = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)

        self.draggable = False
        self.dragThreshold = 5
        self.mousePressPosition = None
        self.mouseMovePosition = None
        self.borderRadius = 5

        self.setWindowFlags(QtCore.Qt.SubWindow)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QtWidgets.QSizeGrip(self._box))
        layout.addWidget(QtWidgets.QSizeGrip(self._box))
        self.setLayout(layout)

        self.show()


    def mousePressEvent(self, event):
        if self.draggable and event.button() == QtCore.Qt.LeftButton:
            self.mousePressPosition = event.globalPos()
            print("mouse press position (global): ", self.mousePressPosition)
            self.mouseMovePosition = event.globalPos() - self.pos()
            print("mouse press position (local): ", self.mouseMovePosition)
        super(BoundingBox, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & QtCore.Qt.LeftButton:
            globalPos = event.globalPos()
            moved = globalPos - self.mousePressPosition
            if moved.manhattanLength() > self.dragThreshold:
                newLocation = globalPos - self.mouseMovePosition
                print("new location (global): ", newLocation)
                self.move(newLocation)
                self.mouseMovePosition = globalPos - self.pos()
                print("new location (local): ", self.mouseMovePosition)
        super(BoundingBox, self).mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if self.mousePressPosition is not None:
            if event.button() == QtCore.Qt.LeftButton:
                moved = event.globalPos() - self.mousePressPosition
                if moved.manhattanLength() > self.dragThreshold:
                    event.ignore()
                self.mousePressPosition = None
        super(BoundingBox, self).mouseReleaseEvent(event)


    def resizeEvent(self, event):
        self._box.resize(self.size())


    def hideBoundingBox(self):
        self._box.hide()
        self.draggable = False


    def showBoundingBox(self):
        self._box.show()
        self.draggable = True

