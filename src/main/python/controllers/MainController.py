"""
MainController.py
Created November 9, 2020

Controls the primary window, including the menu bar and the editor.
"""
from pathlib import Path
import os
from PyQt5 import QtWidgets

from Conversion import convertECGLeads, exportSignals
from ImageUtilities import opencvImageToPixmap
from views.MainWindow import MainWindow
from views.ImageView import *
from views.ROIView import *
from views.ExportFileDialog import *
from views.MessageDialog import *
from model.EcgModel import *
from model.LeadModel import *
from QtWrapper import *


class MainController:

    def __init__(self):
        self.window = MainWindow()
        self.connectUI()
        # The ECG model that we will update and pass to the backend to process
        self.ecg = Ecg() 

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
        self.window.editor.imageViewer.leadImageUpdated.connect(self.saveLeadImage)
        self.window.editor.removeLead.connect(self.removeLead)
        self.window.editor.leadStartTimeChanged.connect(self.updateLeadStartTime)
        self.window.editor.gridTimeScaleChanged.connect(self.updateEcgTimeScale)
        self.window.editor.gridVoltScaleChanged.connect(self.updateEcgVoltScale)
        self.window.editor.processDataButtonClicked.connect(self.confirmDigitization)
        # self.window.editor.exportPathChosen.connect(self.processECGData)

    def openImageFile(self):

        # Per pathlib documentation, if no selection is made then Path('.') is returned
        #  https://docs.python.org/3/library/pathlib.html
        path = Path(self.openFileBrowser("Open File", "Images (*.png *.jpg)"))
        self.outputDirectory = os.path.splitext(path)[0]
        
        if not os.path.exists(self.outputDirectory):
            os.mkdir(self.outputDirectory)

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
        """Closes out current image file and resets editor controls."""
        self.window.editor.removeImage()
        self.removeAllLeads() 
        self.window.editor.resetImageEditControls()       

    def addLead(self, leadId):
        """Adds a Lead ROI box to the image view and corresponding lead object to the ECG model. 

        Args:
            leadId (str): the ID of the lead to be added
        """
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

    def removeLead(self, leadROI):
        """Removes a single ROI box from the image view and its corresponding lead from the ECG model.
        This function is connected to the "Delete Lead" button in the lead detail view panel through
        the 'removeLead' signal.

        Args:
            leadROI (ROIItem): the ROI box of the lead being deleted
        """
        # Remove lead roi box from image view
        self.window.editor.imageViewer.removeRoiBox(leadROI)
        # Re-enable add lead menu button
        self.window.leadButtons[leadROI.leadId].setEnabled(True)
        # Set editor pane back to global view
        self.setEditorPane()                                      
        # Delete lead data from ecg model
        del self.ecg.leads[leadROI.leadId]                            

    def removeAllLeads(self):
        """Removes all of the ROI boxes present and their corresponding leads from the ECG model."""
        # Remove all lead roi boxes from image view
        self.window.editor.imageViewer.removeAllRoiBoxes() 
        # Re-enable all add lead menu buttons
        for lead, button in self.window.leadButtons.items():   
            button.setEnabled(True)             
        # Set editor pane back to global view
        self.setEditorPane()                                    
        # Clear all lead data from model
        self.ecg.leads.clear()                                  

    def setEditorPane(self, leadId=None, leadSelected=False):
        """Switch the Editor pane between Global and Lead-Detail view. Lead-Detail view
        is shown when a ROI box is selected, Global view is displayed otherwise. This is
        connected to the roiItemSelected signal which is emitted when an ROIItem is selected
        or deselected.

        Args:
            leadId ([str], optional): The leadId of the selected ROI. Defaults to None.
            leadSelected (bool, optional): Indicates if a lead ROI was selected. Defaults to False.
        """
        if leadSelected == True and leadId is not None:
            lead = self.ecg.leads[leadId]
            self.window.editor.showLeadDetailView(lead)
        else:
            self.window.editor.showGlobalView(self.ecg.gridVoltageScale, self.ecg.gridTimeScale)

    def updateEcgTimeScale(self, timeScale):
        """Updates the grid time scale in the ECG model. This is connected to the
        time scale spinbox in the global editor pane. It is called whenever the
        spinbox is updated and the gridTimeScaleChanged signal is emitted.

        Args:
            timeScale ([double]): the value of the time scale spinbox
        """
        self.ecg.gridTimeScale = timeScale

    def updateEcgVoltScale(self, voltScale):
        """Updates the grid volt scale in the ECG model. This is connected to the
        volt scale spinbox in the global editor pane. It is called whenever the
        spinbox is updated and the gridVoltScaleChanged signal is emitted.

        Args:
            voltScale ([double]): the value of the volt scale spinbox
        """
        self.ecg.gridVoltageScale = voltScale

    def updateLeadStartTime(self, leadId, value):
        """Updates the start time of a lead in the ECG model. This is connected to the
        start time spinbox in the lead-detail editor pane. It is called whenever the 
        spinbox is updated and the leadStartTimeChanged signal is emitted.

        Args:
            leadId ([type]): [description]
            value ([type]): [description]
        """
        self.ecg.leads[leadId].leadStartTime = value

    def confirmDigitization(self):
        if len(self.ecg.leads) > 0:
            self.processECGData()
        else:
            warningDialog = MessageDialog(
                message="Warning: No data to process\n\nPlease select at least one lead to digitize",
                title="Warning"
            )
            warningDialog.exec_()
    
    # we have all ECG data and export location - ready to pass off to backend to digitize
    def processECGData(self):
        extractedSignals, previewImages = convertECGLeads(self.ecg)
        
        if extractedSignals is None:
            
            errorDialog = MessageDialog(
                message="Error: Signal Processing Failed\n\nPlease check your lead selection boxes",
                title="Error"
            )
            errorDialog.exec_()
        else:
            exportFileDialog = ExportFileDialog(previewImages)
            if exportFileDialog.exec_():
                self.exportECGData(exportFileDialog.fileExportPath, exportFileDialog.delimiterDropdown.currentText(), extractedSignals)

    def exportECGData(self, exportPath, delimiter, extractedSignals):
        if delimiter == "Comma":
            seperator = ','
        elif delimiter == "Tab":
            seperator = '\t'
        elif delimiter == "Space":
            seperator = ' '
    
        exportSignals(extractedSignals, exportPath, separator=seperator)

    def saveLeadImage(self, roi):
        """Saves the cropped lead image. This function is connected to the leadImageUpdated signal which is emitted from
        ROIView.updatePixelData(), meaning a new version of the image is saved every time the lead bounding box is moved.
        Args:
            roi ([ROIItem]): the ROI item from which we need to save the cropped lead image
        """
        imageName = roi.leadId + ".png"
        fullPath = Path.joinpath(Path(self.outputDirectory), imageName)
        pixmap = opencvImageToPixmap(roi.pixelData)     # easier to save a pixmap object than numpy array since we already have this function
        pixmap.save(str(fullPath), "PNG")