"""
QtHelper.py
Created November 7, 2020

Helper functions to simplify interacting with Qt
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def createMenuAction(window, name, shortcut, statusTip, handler):
    action = QtWidgets.QAction('&' + name, window)
    action.setShortcut(shortcut)
    action.setStatusTip(statusTip)
    action.triggered.connect(handler)

    return action