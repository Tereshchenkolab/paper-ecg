"""
MainWindow.py
Created November 7, 2020

Primary window of the application
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys

from QtHelper import *

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.populateMenuBar()


    def populateMenuBar(self):
        self.bar = self.menuBar()

        self.bar.addMenu(
            createMenu(
                owner=self,
                name='fileMenu',
                parent=self.bar,
                displayName='File',
                actions=[
                    createMenuAction(
                        owner=self,
                        name="fileMenuOpen",
                        displayName="Open",
                        shortcut=QtGui.QKeySequence.Open,
                        statusTip="Open an image file"
                    ),
                    "separator",
                    createMenuAction(
                        owner=self,
                        name="fileMenuExport",
                        displayName="Export",
                        shortcut="Ctrl+E",
                        statusTip="Export to a signal file"
                    )
                ]
            )
        )

    def quit(self):
        print("'quit()' handler called")
        sys.exit()


    def open(self):
        print("'open()' handler not implemented")


    def export(self):
        print("'export()' handler not implemented!")
