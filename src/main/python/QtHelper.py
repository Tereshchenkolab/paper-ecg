"""
QtHelper.py
Created November 7, 2020

Helper functions to simplify interacting with Qt
"""

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class IncompatibleFunction(Exception):
    """Thrown when a decorated function is incompatible with the decorator."""
    pass


def bindsToClass(createWidget):
    """
    Decorator for binding a created widget to the owner using the given name.
    Decorated functions must have the first 2 parameters: (owner, name, ...).

    Example:
        @bindsToClass
        def createWidget(owner, name, ...)
            pass

        class Window():
            def __init__(self):
                createWidget(self, "example", ...)
                print(self.example)
    """
    def createAndBind(*args, **kwargs):
        owner, name = None, None

        if "owner" in kwargs and "name" in kwargs:
            owner = kwargs["owner"]
            name = kwargs["name"]
        elif len(args) >= 2:
            owner, name = args[:2]
        else:
            raise IncompatibleFunction(f"Function '{createWidget.__name__}' missing 'name' and 'owner' parameters required by @bindsToClass decorator.")

        widget = createWidget(*args, **kwargs)
        setattr(owner, name, widget)
        return widget


    return createAndBind


@bindsToClass
def createMenuAction(owner: QWidget, name:str, displayName:str, shortcut, statusTip):
    action = QAction('&' + displayName, owner) # In this case the owner is the main window
    action.setShortcut(shortcut)
    action.setStatusTip(statusTip)

    return action


@bindsToClass
def createMenu(owner: QWidget, name:str, parent, displayName:str, actions):
    menu = QMenu(displayName, parent) # In this case the owner is the main window

    for action in actions:
        # TODO: Find a more type-safe way to do this
        if action == "separator":
            menu.addSeparator()
        else:
            menu.addAction(action)

    return menu
