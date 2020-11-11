
import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog

class ImageControl:

    def __init__(self, editorWidget):
        self.editor = editorWidget
        self.imgPath = ""

    def openImgFile(self):
        self.imgPath = QFileDialog.getOpenFileName(self.editor, "Open File", "/", "Images (*.png *.jpg)")
        print("file selected: ", self.imgPath[0])
        self.editor.displayImg(self.imgPath[0])



    