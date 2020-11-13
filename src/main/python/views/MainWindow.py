"""
MainWindow.py
Created November 7, 2020

Primary window of the application
"""

import sys
import QtWrapper as Qt

from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUi()

    def initUi(self):
        self.buildMenuBar()

    def buildMenuBar(self):
        return Qt.MenuBar(
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
