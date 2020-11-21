"""
MainWindow.py
Created November 7, 2020

Primary window of the application
"""

import sys
import QtWrapper as Qt

from PyQt5 import QtCore, QtGui, QtWidgets

from views.EditorWidget import Editor


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.buildUI()


    def buildUI(self):
        self.buildMenuBar()

        self.editor = Editor()
        self.setCentralWidget(self.editor)
        self.setContentsMargins(0,0,0,0)

        self.setWindowTitle("Paper ECG")
        # self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.resize(800, 500)

        self.show()


    def buildMenuBar(self):
        Qt.MenuBar(
            owner=self,
            name='bar',
            menus=[
                self.buildFileMenu(),
                self.buildEditMenu(),
                Qt.Menu(
                    owner=self,
                    name='windowMenu',
                    displayName='Window',
                    items=[
                        Qt.MenuAction(
                            owner=self,
                            name="windowMenuExample",
                            displayName="Example",
                            shortcut=None,
                            statusTip="Example status tip"
                        )
                    ]
                )
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
                Qt.Separator(),
                Qt.MenuAction(
                    owner=self,
                    name="fileMenuExport",
                    displayName="Export",
                    shortcut="Ctrl+E",
                    statusTip="Export to a signal file"
                )
            ]
        )


    def buildEditMenu(self):
        return Qt.Menu(
            owner=self,
            name='editMenu',
            displayName='Edit',
            items=[
                Qt.MenuAction(
                    owner=self,
                    name="editMenuExample",
                    displayName="Example",
                    shortcut=None,
                    statusTip="Example status tip"
                )
            ]
        )
