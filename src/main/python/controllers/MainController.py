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
        self.ecg = Ecg()
        self.connectUI()

    def connectUI(self):
        """
        Hook UI up to handlers in the controller
        """
        self.window.fileMenuOpen.triggered.connect(self.openImageFile)
        self.window.fileMenuClose.triggered.connect(self.closeImageFile)

        self.window.addLead1.triggered.connect(lambda: self.addLead("I"))
        self.window.addLead2.triggered.connect(lambda: self.addLead("II"))
        self.window.addLead3.triggered.connect(lambda: self.addLead("III"))
        self.window.addLeadaVR.triggered.connect(lambda: self.addLead("aVR"))
        self.window.addLeadaVL.triggered.connect(lambda: self.addLead("aVL"))
        self.window.addLeadaVF.triggered.connect(lambda: self.addLead("aVF"))
        self.window.addLeadV1.triggered.connect(lambda: self.addLead("V1"))
        self.window.addLeadV2.triggered.connect(lambda: self.addLead("V2"))
        self.window.addLeadV3.triggered.connect(lambda: self.addLead("V3"))
        self.window.addLeadV4.triggered.connect(lambda: self.addLead("V4"))
        self.window.addLeadV5.triggered.connect(lambda: self.addLead("V5"))
        self.window.addLeadV6.triggered.connect(lambda: self.addLead("V6"))

        self.window.editor.imageViewer.roiItemSelected.connect(self.setEditorPane)
        self.window.editor.removeLead.connect(self.removeLead)
        self.window.editor.leadStartTimeChanged.connect(self.updateLeadStartTime)
        self.window.editor.gridTimeScaleChanged.connect(self.updateEcgTimeScale)
        self.window.editor.gridVoltScaleChanged.connect(self.updateEcgVoltScale)
        self.window.editor.digitizeButtonClicked.connect(self.confirmDigitization)
        self.window.editor.exportPathChosen.connect(self.digitize)

    def openImageFile(self):

        # Per pathlib documentation, if no selection is made then Path('.') is returned
        #  https://docs.python.org/3/library/pathlib.html
        path = Path(self.openFileBrowser("Open File", "Images (*.png *.jpg)"))

        if path != Path('.'):
            self.window.editor.loadImageFromPath(path)
            self.window.editor.resetImageEditControls()
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

    def closeImageFile(self):
        self.window.editor.removeImage()
        self.removeAllLeads() 
        self.window.editor.resetImageEditControls()       

    def addLead(self, leadId):
        if self.window.editor.imageViewer.hasImage():
            # Disable menu action so user can't add more than one bounding box for an individual lead
            # action.setEnabled(False)
            self.window.leadButtons[leadId].setEnabled(False)

            # Create instance of Region of Interest (ROI) bounding box and add to image viewer
            roiBox = ROIItem(self.window.editor.imageViewer._scene, leadId)
            roiBox.setRect(0, 0, 400, 200)
            roiBox.setPos(0,0)
            self.window.editor.imageViewer._scene.addItem(roiBox)
            roiBox.show()

            # Create new lead instance and add to ECG model
            lead = Lead(leadId, roiBox)
            self.ecg.leads[leadId] = lead

    def removeLead(self, lead):
        # Re-enable menu action so lead can be added in the future
        self.window.editor.imageViewer.removeRoiBox(lead)       # remove lead roi box from image view
        self.window.leadButtons[lead.leadId].setEnabled(True)   # re-enable add lead menu button
        self.setEditorPane()                                    # set editor pane back to global view
        del self.ecg.leads[lead.leadId]                         # delete lead data from ecg model

    def removeAllLeads(self):
        self.window.editor.imageViewer.removeAllRoiBoxes()      # remove all lead roi boxes from image view
        for lead, button in self.window.leadButtons.items():    # re-enable all add lead menu buttons
            button.setEnabled(True)             
        self.setEditorPane()                                    # set editor pane back to global view
        self.ecg.leads.clear()                                  # clear all lead data from model

    def setEditorPane(self, leadId=None, leadSelected=False):
        if leadSelected == True and leadId is not None:
            lead = self.ecg.leads[leadId]
            self.window.editor.showLeadDetailView(lead)
        else:
            self.window.editor.showGlobalView(self.ecg.gridVoltageScale, self.ecg.gridTimeScale)

    def updateEcgTimeScale(self, timeScale):
        print("update ecg time scale: " + str(timeScale))
        self.ecg.gridTimeScale = timeScale
    
    def updateEcgVoltScale(self, voltScale):
        print("update ecg volt scale" + str(voltScale))
        self.ecg.gridVoltageScale = voltScale

    def updateLeadStartTime(self, leadId, value):
        print("update lead " + leadId + " start time to: " + str(value))
        self.ecg.leads[leadId].leadStartTime = value

    def confirmDigitization(self):
        self.window.editor.openExportFileDialog()
    
    # we have all ECG data and export location - ready to pass off to backend to digitize
    def digitize(self, exportPath, fileType):
        print("ready to digitize")
        print("export path: " + exportPath + "\nfile type: " + fileType)
        print("grid volt scale: " + str(self.ecg.gridVoltageScale) + 
                "\ngrid time scale: " + str(self.ecg.gridTimeScale))
        self.ecg.printLeadInfo()
