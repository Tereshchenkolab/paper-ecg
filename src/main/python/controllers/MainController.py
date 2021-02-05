"""
MainController.py
Created November 9, 2020

Controls the primary window, including the menu bar and the editor.
"""

import sys
from pathlib import Path
from PyQt5 import QtGui, QtWidgets, QtCore

from views.MainWindow import MainWindow
from views.ImageView import *
from QtWrapper import *


class MainController:

    def __init__(self):
        self.window = MainWindow()
        self.connectUI()


    def connectUI(self):
        """
        Hook UI up to handlers in the controller
        """
        self.window.fileMenuOpen.triggered.connect(self.openImageFile)
        self.window.leadMenuAdd.triggered.connect(self.showAddLeadDialog)


    def openImageFile(self):
        path = Path(self.openFileBrowser("Open File", "Images (*.png *.jpg)"))

        if path is not None:
            self.window.editor.loadImageFromPath(path)
        else:
            print("[Warning] No image selected")


    def openFileBrowser(self, caption: str, fileType: str, initialPath: str ="") -> str:
        """Launches a file browser for the user to select a file to open.

        Args:
            caption (str): The caption shown to the user
            fileType (str): The acceptable file types ex: `Images (*.png *.jpg)`
            initialPath (str, optional): The path at which the file browser opens. Defaults to "".

        Returns:
            str: Path to the selected file.
        """
        absolutePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.window, # Parent
            caption,
            initialPath, # If the initial path is `""` it defaults to the most recent path.
            fileType
        )

        return absolutePath
    
    def showAddLeadDialog(self):
        self.leadDialog = QtWidgets.QDialog()
        self.leadDialog.setWindowTitle("Add Lead")
        self.leadDialog.setMinimumSize(300, 200)
        self.leadDialog.setLayout(VerticalBoxLayout(self, "main", margins=(0,0,0,0), 
            contents=[
                VerticalBoxLayout(
                    owner=self,
                    name="dialogBoxMainLayout",
                    contents=[
                        ComboBox(["Lead I", "Lead II", "Lead III"], owner=self.leadDialog, name="leadCombo"),
                        PushButton(self.leadDialog, "acceptButton", text="select")
                    ]
                )
            ]))

        self.leadDialog.acceptButton.clicked.connect(self.selected)

        retVal = self.leadDialog.exec_()
        if retVal == 0:
            print("cancelled")


    def selected(self):
        print("selection made")
        selection = self.leadDialog.leadCombo.currentText()

        self.addLead(selection)

        self.leadDialog.accept()


    def addLead(self, selection):

        print("lead selected: ", selection)

        box = ROIItem(self.window.editor.imageViewer._scene)
        box.setLeadId(selection)
        box.setRect(0, 0, 400, 200)
        box.setPos(0,0)

        self.window.editor.imageViewer._scene.addItem(box)
        print(self.window.editor.imageViewer._scene.items())

        box.show()
