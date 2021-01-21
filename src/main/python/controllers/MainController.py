"""
MainController.py
Created November 9, 2020

Controls the primary window, including the menu bar and the editor.
"""

import sys
from PyQt5 import QtGui, QtWidgets, QtCore

from views.MainWindow import MainWindow


class MainController:

    def __init__(self):
        self.window = MainWindow()
        self.connectUI()


    def connectUI(self):
        """
        Hook UI up to handlers in the controller
        """
        self.window.fileMenuOpen.triggered.connect(self.openImageFile)


    def openImageFile(self):
        fileInfo = QtWidgets.QFileDialog.getOpenFileName(self.window, "Open File", "/", "Images (*.png *.jpg)")
        print("file selected: ", fileInfo[0])
        if (fileInfo[0] != ""):
            self.window.editor.displayImage(fileInfo[0])
