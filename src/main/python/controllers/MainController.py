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
from views.ROIView import *
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

        self.window.addLead1.triggered.connect(lambda: self.addLead("I", self.window.addLead1))
        self.window.addLead2.triggered.connect(lambda: self.addLead("II", self.window.addLead2))
        self.window.addLead3.triggered.connect(lambda: self.addLead("III", self.window.addLead3))
        self.window.addLeadaVR.triggered.connect(lambda: self.addLead("aVR", self.window.addLeadaVR))
        self.window.addLeadaVL.triggered.connect(lambda: self.addLead("aVL", self.window.addLeadaVL))
        self.window.addLeadaVF.triggered.connect(lambda: self.addLead("aVF", self.window.addLeadaVF))
        self.window.addLeadV1.triggered.connect(lambda: self.addLead("V1", self.window.addLeadV1))
        self.window.addLeadV2.triggered.connect(lambda: self.addLead("V2", self.window.addLeadV2))
        self.window.addLeadV3.triggered.connect(lambda: self.addLead("V3", self.window.addLeadV3))
        self.window.addLeadV4.triggered.connect(lambda: self.addLead("V4", self.window.addLeadV4))
        self.window.addLeadV5.triggered.connect(lambda: self.addLead("V5", self.window.addLeadV5))
        self.window.addLeadV6.triggered.connect(lambda: self.addLead("V6", self.window.addLeadV6))

        self.window.editor.imageViewer.itemSelected.connect(self.updateEditorPane)


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


    def addLead(self, selection, action):
        if self.window.editor.imageViewer.hasImage():
            # Disable menu action so user can't add more than one bounding box for an individual lead
            action.setEnabled(False)

            box = ROIItem(self.window.editor.imageViewer._scene)
            box.setLeadId(selection)
            box.setRect(0, 0, 400, 200)
            box.setPos(0,0)

            self.window.editor.imageViewer._scene.addItem(box)
            
            box.show()

    def updateEditorPane(self, item, selected):
        print("update editor panel")
        print("item: ", item.getLeadId())
        print("selected: ", selected)
        self.window.editor.setEditPanel(selected)

