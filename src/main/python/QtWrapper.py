"""
QtWrapper.py
Created November 7, 2020

Wrapper to simplify interacting with Qt
"""

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from typing import List, Union, Optional


class IncompatibleFunction(Exception):
    """Thrown when a decorated function is incompatible with the decorator."""
    pass


def bindsToClass(createWidgetFunction):
    """
    Decorator for binding a created widget to the owner using the given name.
    Decorated functions must have the first 2 parameters: (owner, name, ...).

    Example:
        @bindsToClass
        def createWidget(owner, name, other, parameters)
            pass

        class Window():
            def __init__(self):
                createWidget(self, "example", foo, bar)
                print(self.example)
    """
    def createAndBind(*args, **kwargs):
        # Try to extract the `owner` and `name` parameters
        if "owner" in kwargs and "name" in kwargs:
            owner, name = kwargs["owner"], kwargs["name"]
        elif len(args) == 1 and "name" in kwargs:
            owner, name = args[0], kwargs["name"]
        elif len(args) >= 2:
            owner, name = args[:2]
        else:
            # If `owner` and `name` can't be found, just throw an
            # error to explain what happened
            raise IncompatibleFunction(f"Function '{createWidgetFunction.__name__}' missing 'owner' and 'name' parameters required by @bindsToClass decorator.")

        # Create the widget by calling the decorated function
        widget = createWidgetFunction(*args, **kwargs)

        # Set `owner.name = widget` so the owner class is able to access the widget
        setattr(owner, name, widget)

        return widget


    return createAndBind


@bindsToClass
def MenuAction(owner: QWidget, name:str, displayName:str, shortcut:Optional[Union[str, QtGui.QKeySequence]], statusTip: Optional[str]) -> QAction:
    """Creates a MenuAction

    Args:
        owner (QWidget): The class to which the Menu property will be added
        name (str): The property name of the Menu in the class (not seen by users)
        displayName (str): The name displayed to the user in the menu list for this action
        shortcut (Union[str, QtGui.QKeySequence]): The keyboard shortcut to trigger the action
        statusTip (str): ???
    """
    action = QAction('&' + displayName, owner) # In this case the owner is the main window
    if shortcut:
        action.setShortcut(shortcut)
    if statusTip:
        action.setStatusTip(statusTip)

    return action


class Separator():
    """A dummy type to represent a menu separator
    """
    pass


@bindsToClass
def Menu(owner: QWidget, name:str, displayName:str, items:List[Union[QAction, Separator]]) -> QMenu:
    """Creates a QMenu

    Args:
        owner (QWidget): The class to which the Menu property will be added
        name (str): The property name of the Menu in the class (not seen by users)
        displayName (str): The Menu name displayed to the user
        items (List[Union[QAction, Separator]]): Items to display in the menu

    Returns:
        QMenu: Menu
    """
    menu = QMenu(displayName) # In this case the `owner` is the main window
    for item in items:
        if type(item) is Separator: menu.addSeparator()
        elif type(item) is QAction: menu.addAction(item)

    return menu


@bindsToClass
def MenuBar(owner: QWidget, name:str, menus: List[QMenu]) -> QMenuBar:
    """Creates a QMenuBar

    Args:
        owner (QWidget): The MainWindow to which the MenuBar will be added
        name (str): The name of the MenuBar property
        menus (List[QMenu]): Menus container in the MenuBar

    Returns:
        QMenuBar: The menubar created
    """
    menuBar = owner.menuBar() # In this case the `owner` is the main window
    for menu in menus:
        menuBar.addMenu(menu)

    return menuBar
