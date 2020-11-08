"""
MainWindow.py
Created November 7, 2020

Primary window of the application
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from QtHelper import *

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.populateMenuBar()


    def populateMenuBar(self):
        menuBar = self.menuBar()

        self.addFileMenu(menuBar)


    def addFileMenu(self, menuBar):
        fileMenu = menuBar.addMenu('File')

        fileMenu.addAction(
            createMenuAction(
                window=self,
                name="Open",
                shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an image file",
                handler=self.open
            )
        )

        fileMenu.addSeparator()

        fileMenu.addAction(
            createMenuAction(
                window=self,
                name="Export",
                shortcut="Ctrl+E",
                statusTip="Export to a signal file",
                handler=self.export
            )
        )


    def quit(self):
        print("'open()' handler called")
        sys.exit()


    def open(self):
        print("'open()' handler not implemented!")


    def export(self):
        print("'export()' handler not implemented!")
