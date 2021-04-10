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
from views.ExportFileDialog import *
from model.EcgModel import *
from model.LeadModel import *
from QtWrapper import *

class MainController:

    def __init__(self):
        self.window = MainWindow()
        self.ecgModel = EcgModel()
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

        self.window.editor.imageViewer.itemSelected.connect(self.setEditorPane)
        self.window.editor.imageViewer.itemMoved.connect(self.updateEcgLead)
        self.window.editor.leadStartTimeChanged.connect(self.updateLeadStartTime)
        self.window.editor.gridTimeScaleChanged.connect(self.updateEcgTimeScale)
        self.window.editor.gridVoltScaleChanged.connect(self.updateEcgVoltScale)
        self.window.editor.digitizeButtonClicked.connect(self.confirmDigitization)
        self.window.editor.exportPathChosen.connect(self.digitize)


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


    def addLead(self, leadId, action):
        if self.window.editor.imageViewer.hasImage():
            # Disable menu action so user can't add more than one bounding box for an individual lead
            action.setEnabled(False)

            # Create instance of Region of Interest (ROI) bounding box and add to image viewer
            roiBox = ROIItem(self.window.editor.imageViewer._scene, leadId)
            roiBox.setRect(0, 0, 400, 200)
            roiBox.setPos(0,0)
            self.window.editor.imageViewer._scene.addItem(roiBox)
            roiBox.show()

            # Create new lead instance and add to ECG model
            lead = Lead(leadId, roiBox)
            self.ecgModel.leads[leadId] = lead


    def setEditorPane(self, leadId, leadSelected):
        if leadSelected == True and leadId is not None:
            lead = self.ecgModel.leads[leadId]
            self.window.editor.showLeadDetailView(lead)
        else:
            self.window.editor.showGlobalView(self.ecgModel.gridVoltageScale, self.ecgModel.gridTimeScale)

    def updateEcgLead(self, lead):
        print("update ecg lead: ", lead.leadId)
        index = lead.leadId
        self.ecgModel.leads[index].roiData.pixelData.save("modelTest.png")

    def updateEcgTimeScale(self, timeScale):
        print("update ecg time scale: " + str(timeScale))
        self.ecgModel.gridTimeScale = timeScale
    
    def updateEcgVoltScale(self, voltScale):
        print("update ecg volt scale" + str(voltScale))
        self.ecgModel.gridVoltageScale = voltScale

    def updateLeadStartTime(self, leadId, value):
        print("update lead " + leadId + " start time to: " + str(value))
        self.ecgModel.leads[leadId].leadStartTime = value

    # confirm all ECG model data is present and get export location
    def confirmDigitization(self):
        print("confirm digitization")
        if len(self.ecgModel.leads) == 12:
            self.window.editor.openExportFileDialog()
        else:
            print("missing lead data")
    
    # we have all ECG data and export location - ready to pass off to backend to digitize
    def digitize(self, exportPath, fileType):
        print("ready to digitize")
        print("export path: " + exportPath + "\nfile type: " + fileType)
        print("grid volt scale: " + str(self.ecgModel.gridVoltageScale) + 
                "\ngrid time scale: " + str(self.ecgModel.gridTimeScale))
        self.ecgModel.printLeadInfo()
