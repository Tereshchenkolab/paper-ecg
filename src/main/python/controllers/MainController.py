
import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from views.MainWindow import MainWindow


class MainController:

    def __init__(self, editorWidget, mainWindow):
        self.editor = editorWidget
        self.window = mainWindow

        self.connectWindow()

    def connectWindow(self):
        # Hook UI up to handlers in the controller
        self.window.fileMenuOpen.triggered.connect(self.openImageFile)

    def openImageFile(self):
        fileInfo = QFileDialog.getOpenFileName(self.window, "Open File", "/", "Images (*.png *.jpg)")
        print("file selected: ", fileInfo[0])
        self.editor.displayImage(fileInfo[0])   # Attempt to display image in editor (causing issues currently)
