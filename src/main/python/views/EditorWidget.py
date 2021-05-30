"""
EditorWindow.py
Created November 7, 2020

-
"""
import dataclasses
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

import digitize
from model.Lead import LeadId
from views.ImageView import *
from views.ROIView import *
from views.EditPanelLeadView import *
from views.EditPanelGlobalView import *
from QtWrapper import *
import model.EcgModel as EcgModel
from views.MessageDialog import *

@dataclasses.dataclass(frozen=False)
class Lead:
    x: int
    y: int
    width: int
    height: int
    startTime: int

@dataclasses.dataclass(frozen=False)
class InputParameters:
    rotation: int
    timeScale: int
    voltScale: int
    leads: dict

class Editor(QtWidgets.QWidget):
    processEcgData = QtCore.pyqtSignal()
    saveAnnotationsButtonClicked = QtCore.pyqtSignal(object)

    image = None # The openCV image

    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent

        self.initUI()
        self.connectUI()

        # I'm not sure how well having this mutable will work... In particular if another class *sets* this
        # value, because I don't know how to make the interface `listen` to these values. What about a
        # getter-setter style approach that just uses this class to package the state of the editor?
        self.inputParameters = InputParameters(
            rotation=self.EditPanelGlobalView.rotationSlider.value(),
            timeScale=self.EditPanelGlobalView.timeScaleSpinBox.value(),
            voltScale=self.EditPanelGlobalView.voltScaleSpinBox.value(),
            leads={}
        )

        print(self.inputParameters)

    def initUI(self):
        self.setLayout(
            HorizontalBoxLayout(self, "main", margins=(0,0,0,0), contents=[
                HorizontalSplitter(owner=self, name="viewSplitter", contents=[
                    Custom(
                        owner=self,
                        name="imageViewer",
                        widget=ImageView()
                    ),
                    ScrollArea(
                        owner=self,
                        name="controlPanel",
                        horizontalScrollBarPolicy=QtCore.Qt.ScrollBarAlwaysOff,
                        verticalScrollBarPolicy=QtCore.Qt.ScrollBarAsNeeded,
                        widgetIsResizable=True,
                        innerWidget=
                        StackedWidget(owner=self, name="editPanel", widgets=[
                            Custom(
                                owner=self,
                                name="EditPanelGlobalView",
                                widget=EditPanelGlobalView(self)
                            ),
                            Custom(
                                owner=self,
                                name="EditPanelLeadView",
                                widget=EditPanelLeadView(self)
                            )
                        ])
                    )
                ])
            ])
        )
        self.viewSplitter.setCollapsible(0,False)
        self.viewSplitter.setCollapsible(1,False)
        self.viewSplitter.setSizes([2,1])
        self.editPanel.setCurrentIndex(0)

        # Constraint the width of the adjustable side panel on the right of the editor
        self.controlPanel.setMinimumWidth(250)
        self.controlPanel.setMaximumWidth(450)

    def connectUI(self):
        self.mainWindow.addLead1.triggered.connect(lambda: self.addLead(LeadId(0)))
        self.mainWindow.addLead2.triggered.connect(lambda: self.addLead(LeadId(1)))
        self.mainWindow.addLead3.triggered.connect(lambda: self.addLead(LeadId(2)))
        self.mainWindow.addLeadaVR.triggered.connect(lambda: self.addLead(LeadId(3)))
        self.mainWindow.addLeadaVL.triggered.connect(lambda: self.addLead(LeadId(4)))
        self.mainWindow.addLeadaVF.triggered.connect(lambda: self.addLead(LeadId(5)))
        self.mainWindow.addLeadV1.triggered.connect(lambda: self.addLead(LeadId(6)))
        self.mainWindow.addLeadV2.triggered.connect(lambda: self.addLead(LeadId(7)))
        self.mainWindow.addLeadV3.triggered.connect(lambda: self.addLead(LeadId(8)))
        self.mainWindow.addLeadV4.triggered.connect(lambda: self.addLead(LeadId(9)))
        self.mainWindow.addLeadV5.triggered.connect(lambda: self.addLead(LeadId(10)))
        self.mainWindow.addLeadV6.triggered.connect(lambda: self.addLead(LeadId(11)))

        self.imageViewer.roiItemSelected.connect(self.setControlPanel)
        self.imageViewer.updateRoiItem.connect(self.updateLeadRoi)

        self.EditPanelLeadView.leadStartTimeChanged.connect(self.updateLeadStartTime)
        self.EditPanelLeadView.deleteLeadRoi.connect(self.deleteLeadRoi)

    def loadMetaData(self, data):
        self.setRotation(data['rotation'])
        self.EditPanelGlobalView.setValues(voltScale=data['voltageScale'], timeScale=data['timeScale'])
        
        # print(data['leads'])
        leads = data['leads']
        for name in leads:
            lead = leads[name]
            cropping = lead['cropping']
            self.addLead(LeadId[name], cropping['x'], cropping['y'], cropping['width'], cropping['height'])
            self.inputParameters.leads[LeadId[name]].startTime = lead['start']

###########################
# Control Panel Functions #
###########################

    def setControlPanel(self, leadId=None, leadSelected=False):
        if leadSelected == True and leadId is not None:
            self.showLeadDetailView(leadId)
        else:
            self.showGlobalView(self.inputParameters.voltScale, self.inputParameters.timeScale)

    def showGlobalView(self, voltScale=EcgModel.Ecg.DEFAULT_VOLTAGE_SCALE, timeScale=EcgModel.Ecg.DEFAULT_TIME_SCALE):
        self.EditPanelGlobalView.setValues(voltScale, timeScale)
        self.editPanel.setCurrentIndex(0)

    def showLeadDetailView(self, leadId):
        leadStartTime = self.inputParameters.leads[LeadId(leadId)].startTime
        self.EditPanelLeadView.setValues(leadId, LeadId(leadId).name, leadStartTime)
        self.editPanel.setCurrentIndex(1)

    def rotationSliderChanged(self, _ = None):
        value = self.getRotation()

        self.inputParameters.rotation = value
        self.imageViewer.rotateImage(value)

    def getRotation(self) -> float:
        return self.EditPanelGlobalView.rotationSlider.value() / -10

    def setRotation(self, angle: float):
        self.EditPanelGlobalView.rotationSlider.setValue(angle * -10)
        self.rotationSliderChanged()

    def autoRotate(self):
        if self.image is None: return

        angle = digitize.estimateRotationAngle(self.image)

        if angle is None:
            errorModal = QtWidgets.QMessageBox()
            errorModal.setWindowTitle("Error")
            errorModal.setText("Unable to detect the angle automatically!")
            errorModal.setInformativeText("Use the slider to adjust the rotation manually")
            errorModal.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            errorModal.exec_()
        else:
            self.setRotation(angle)

    def resetRotation(self):
        self.setRotation(0)
        # self.EditPanelGlobalView.rotationSlider.setValue(0)
        # self.adjustRotation()

    def confirmDigitization(self):
        if len(self.inputParameters.leads) > 0:
            self.processEcgData.emit(self.inputParameters)
        else:
            warningDialog = MessageDialog(
                message="Warning: No data to process\n\nPlease select at least one lead to digitize",
                title="Warning"
            )
            warningDialog.exec_()


    ###################
    # Image Functions #
    ###################

    def resetImageEditControls(self):
        self.EditPanelGlobalView.rotationSlider.setValue(0)
        self.EditPanelGlobalView.clearTimeSpinBox()
        self.EditPanelGlobalView.clearVoltSpinBox()
        self.showGlobalView()

    def loadImageFromPath(self, path: Path):
        self.image = ImageUtilities.readImage(path)
        self.displayImage()

    def displayImage(self):
        self.imageViewer.setImage(self.image)
        self.editPanel.show()

        # Adjust zoom to fit image in view
        self.imageViewer.fitImageInView()

    def removeImage(self):
        self.image = None
        self.imageViewer.removeImage()

    ########################
    # Grid Scale Functions #
    ########################

    def updateTimeScale(self, value = None):
        if value is None:
            value = self.EditPanelGlobalView.timeScaleSpinBox.value()

        self.inputParameters.timeScale = value
        print("updated time scale\n",self.inputParameters)

    def updateVoltScale(self, value = None):
        if value is None:
            value = self.EditPanelGlobalView.voltScaleSpinBox.value()

        self.inputParameters.voltScale = value
        print("updated volt scale\n",self.inputParameters)


    ######################
    # Lead ROI functions #
    ######################

    def addLead(self, leadIdEnum, x=0, y=0, width=400, height=200):
        if self.imageViewer.hasImage():
            idName = leadIdEnum.name
            leadId = leadIdEnum.value

            # Disable menu action so user can't add more than one bounding box for an individual lead
            # action.setEnabled(False)
            self.mainWindow.leadButtons[leadIdEnum].setEnabled(False)

            # Create instance of Region of Interest (ROI) bounding box and add to image viewer
            roiBox = ROIItem(self.imageViewer._scene, leadId)
            roiBox.setRect(x, y, width, height)
            # roiBox.setPos(x,y)
            self.imageViewer._scene.addItem(roiBox)
            roiBox.show()

            # Create new lead instance and add to ECG model
            lead = Lead(roiBox.x, roiBox.y, roiBox.width, roiBox.height, 0)
            self.inputParameters.leads[leadIdEnum] = lead
            print("input parameters:")
            print(self.inputParameters)

    def updateLeadRoi(self, roi):
        print("update lead ", roi.leadId, " roi ")
        self.inputParameters.leads[LeadId(roi.leadId)].x = roi.x
        self.inputParameters.leads[LeadId(roi.leadId)].y = roi.y
        self.inputParameters.leads[LeadId(roi.leadId)].width = roi.width
        self.inputParameters.leads[LeadId(roi.leadId)].height = roi.height
        print(self.inputParameters.leads)

    def updateLeadStartTime(self, leadId, value=None):
        if value is None:
            value = self.EditPanelLeadView.leadStartTimeSpinBox.value()

        self.inputParameters.leads[LeadId(leadId)].startTime = value
        print("updated lead", leadId, " start time\n",self.inputParameters)

    def deleteLeadRoi(self, leadId):
        self.imageViewer.removeRoiBox(leadId)   # Remove lead roi box from image view
        self.mainWindow.leadButtons[leadId].setEnabled(True)    # Re-enable add lead menu button
        self.setControlPanel()  # Set editor pane back to global view
        del self.inputParameters.leads[LeadId(leadId)]  # Delete lead data from input parameters

        print("lead ", leadId, " deleted\n", self.inputParameters)

    def deleteAllLeadRois(self):
        self.imageViewer.removeAllRoiBoxes()  # Remove all lead roi boxes from image view

        # Re-enable all add lead menu buttons
        for lead, button in self.mainWindow.leadButtons.items():
            button.setEnabled(True)

        self.setControlPanel()    # Set editor pane back to global view
        self.inputParameters.leads.clear()  # Clear all lead data from model
