"""
Main.py
Created November 1, 2020

Entry point for the application
"""

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic

from Utility import *
from MainWindow import MainWindow
from EditorWidget import Editor

import os, sys

if __name__ == '__main__':
    context = ApplicationContext()

    # Translate asset paths to useable format for PyInstaller
    def resource(relativePath):
        return context.get_resource(relativePath)

    editor = Editor()

    window = MainWindow()
    window.setWindowTitle("Paper ECG")
    window.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
    window.setCentralWidget(editor)
    window.setContentsMargins(0,0,0,0)
    window.resize(800, 500)
    window.show()

    exit_code = context.app.exec_()
    print(f"Exiting with status {exit_code}")
    sys.exit(exit_code)