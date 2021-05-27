"""
MainWindow.py
Created November 7, 2020

Primary window of the application
"""
from PyQt5 import QtCore, QtGui, QtWidgets

from views.EditorWidget import Editor
from model.Lead import LeadId
import QtWrapper as Qt


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.buildUI()


    def buildUI(self):
        self.buildMenuBar()
        self.buildLeadButtonDictionary()

        self.editor = Editor(self)
        self.setCentralWidget(self.editor)
        self.setContentsMargins(0,0,0,0)

        self.setWindowTitle("Paper ECG")
        # self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.resize(800, 500)

        self.showMaximized()


    def buildMenuBar(self):
        Qt.MenuBar(
            owner=self,
            name='bar',
            menus=[
                self.buildFileMenu(),
                self.buildLeadMenu()
            ]
        )

    def buildFileMenu(self):
        return Qt.Menu(
            owner=self,
            name='fileMenu',
            displayName='File',
            items=[
                Qt.MenuAction(
                    owner=self,
                    name="fileMenuOpen",
                    displayName="Open",
                    shortcut=QtGui.QKeySequence.Open,
                    statusTip="Open an image file"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="fileMenuClose",
                    displayName="Close",
                    shortcut=QtGui.QKeySequence.Close,
                    statusTip="Close image file"
                )
            ]
        )

    def buildLeadMenu(self):
        return Qt.Menu(
            owner=self,
            name='leadMenu',
            displayName='Leads',
            items=[
               Qt.MenuAction(
                    owner=self,
                    name="addLead1",
                    displayName="Add Lead I",
                    shortcut=QtGui.QKeySequence('Ctrl+1'),
                    statusTip="Add Lead I"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLead2",
                    displayName="Add Lead II",
                    shortcut=QtGui.QKeySequence('Ctrl+2'),
                    statusTip="Add Lead II"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLead3",
                    displayName="Add Lead III",
                    shortcut=QtGui.QKeySequence('Ctrl+3'),
                    statusTip="Add Lead III"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLeadaVR",
                    displayName="Add Lead aVR",
                    shortcut=QtGui.QKeySequence('Ctrl+4'),
                    statusTip="Add Lead aVR"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLeadaVL",
                    displayName="Add Lead aVL",
                    shortcut=QtGui.QKeySequence('Ctrl+5'),
                    statusTip="Add Lead aVL"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLeadaVF",
                    displayName="Add Lead aVF",
                    shortcut=QtGui.QKeySequence('Ctrl+6'),
                    statusTip="Add Lead aVF"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLeadV1",
                    displayName="Add Lead V1",
                    shortcut=QtGui.QKeySequence('Ctrl+7'),
                    statusTip="Add Lead V1"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLeadV2",
                    displayName="Add Lead V2",
                    shortcut=QtGui.QKeySequence('Ctrl+8'),
                    statusTip="Add Lead V2"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLeadV3",
                    displayName="Add Lead V3",
                    shortcut=QtGui.QKeySequence('Ctrl+9'),
                    statusTip="Add Lead V3"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLeadV4",
                    displayName="Add Lead V4",
                    shortcut=QtGui.QKeySequence('Ctrl+0'),
                    statusTip="Add Lead V4"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLeadV5",
                    displayName="Add Lead V5",
                    shortcut=QtGui.QKeySequence('Ctrl+['),
                    statusTip="Add Lead V5"
                ),
                Qt.MenuAction(
                    owner=self,
                    name="addLeadV6",
                    displayName="Add Lead V6",
                    shortcut=QtGui.QKeySequence('Ctrl+]'),
                    statusTip="Add Lead V6"
                )
            ]
        )

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)

    def buildLeadButtonDictionary(self):
        # Creates relationship between lead ID and the menu button used to add that lead
        self.leadButtons = {
            LeadId(0): self.addLead1,
            LeadId(1): self.addLead2,
            LeadId(2): self.addLead3,
            LeadId(3): self.addLeadaVR,
            LeadId(4): self.addLeadaVL,
            LeadId(5): self.addLeadaVF,
            LeadId(6): self.addLeadV1,
            LeadId(7): self.addLeadV2,
            LeadId(8): self.addLeadV3,
            LeadId(9): self.addLeadV4,
            LeadId(10): self.addLeadV5,
            LeadId(11): self.addLeadV6
        }