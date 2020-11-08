"""
EditorWindow.py
Created November 7, 2020

-
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, platform

from QtHelper import *

class Editor(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0) # Adds ~10px by default

        midleft = QtWidgets.QFrame()

        # Initialize tab screen
        tabs = QtWidgets.QTabWidget()

        globalLayout = QtWidgets.QVBoxLayout()

        globalGroup1 = QtWidgets.QGroupBox("Color Adjustments")

        globalGroup1Layout = QtWidgets.QVBoxLayout()
        globalGroup1Layout.addWidget(QtWidgets.QSlider(QtCore.Qt.Horizontal))
        globalGroup1Layout.addWidget(QtWidgets.QSlider(QtCore.Qt.Horizontal))
        globalGroup1Layout.addWidget(QtWidgets.QSlider(QtCore.Qt.Horizontal))

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
        splitter.addWidget(midleft)

        # If on MacOS
        if platform.system() == "Darwin":
            tabs.setStyleSheet("""
                QTabWidget:left {
                    left: 10px;
                }

                QTabWidget:right {
                    right: 10px;
                }

                QTabWidget::pane:top {
                    top: 40px;
                }

                QTabWidget::tab-bar {
                     /* Force it stretch as wide as possible */
                    width: 1000px;
                }

                QTabWidget::tab-bar:top {
                    top: 20px;
                }
                QTabWidget::tab-bar:bottom {
                    bottom: 20px;
                }
                """
            )

            tabsLayout = QtWidgets.QHBoxLayout()
            tabsLayout.setContentsMargins(10,0,10,0)
            tabsLayout.addWidget(tabs)

            tabsContainer = QtWidgets.QWidget()
            tabsContainer.setLayout(tabsLayout)
            tabsContainer.setObjectName("tabsContainer")

            tabsContainer.setStyleSheet("""
                .QWidget#tabsContainer {
                    background: rgba(0,0,0,0.1);
                }
            """)

            splitter.setStyleSheet("""
                QSplitter::handle {

                }
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