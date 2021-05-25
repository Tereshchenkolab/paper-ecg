"""
QtWrapper.py
Created November 7, 2020

Wrapper to simplify interacting with Qt
"""
from typing import cast, List, Optional, Tuple, Union

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QAction, QComboBox, QGroupBox, QHBoxLayout, QLabel, QLayout, QMenu, QMenuBar, QMainWindow, QPushButton, QRadioButton, QScrollArea, QSizePolicy, QSlider, QSplitter, QTabWidget, QVBoxLayout, QWidget, QStackedWidget, QSpinBox, QDoubleSpinBox, QLineEdit, QFormLayout


class SplitterOrientation:
    Horizontal = QtCore.Qt.Horizontal
    Vertical = QtCore.Qt.Vertical


class Separator():
    """A dummy type to represent a menu separator"""
    pass


class Tab:
    def __init__(self, label: str, widget: QWidget):
        self.label = label
        self.widget = widget


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
        owner, name = None, None

        # Try to extract the `owner` and `name` parameters
        if "owner" in kwargs and "name" in kwargs:
            owner, name = kwargs["owner"], kwargs["name"]
        elif len(args) == 1 and "name" in kwargs:
            owner, name = args[0], kwargs["name"]
        elif len(args) >= 2:
            owner, name = args[:2]

        # Create the widget by calling the decorated function
        widget = createWidgetFunction(*args, **kwargs)

        # Improve ease of debugging (this error presents as a segfault)
        assert widget is not None, f"Widget creation function '{createWidgetFunction.__name__}' returned None"

        if owner is not None and name is not None and name != "":
            # Set `owner.name = widget` so the owner class is able to access the widget
            setattr(owner, name, widget)

        return widget

    return createAndBind


@bindsToClass
def ComboBox(
    items: List[str],
    owner: Optional[QWidget] = None,
    name: Optional[str] = None
) -> QComboBox:
    """[summary]"""

    comboBox = QComboBox()
    comboBox.addItems(items)

    return comboBox


@bindsToClass
def SpinBox(
    owner: QWidget,
    name: str,
    minVal: int,
    maxVal: int,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    defaultValue: Optional[int] = None,
) -> QSpinBox:
    spinbox = QSpinBox()
    spinbox.setMinimum(minVal)
    spinbox.setMaximum(maxVal)
    if prefix:
        spinbox.setPrefix(prefix)
    if suffix:
        spinbox.setSuffix(suffix)
    if defaultValue:
        spinbox.setValue(defaultValue)
    return spinbox


@bindsToClass
def DoubleSpinBox(
    owner: QWidget,
    name: str,
    minVal: float,
    maxVal: float,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    defaultValue: Optional[float] = None
) -> QDoubleSpinBox:
    spinbox = QDoubleSpinBox()
    spinbox.setMinimum(minVal)
    spinbox.setMaximum(maxVal)
    if prefix:
        spinbox.setPrefix(prefix)
    if suffix:
        spinbox.setSuffix(suffix)
    if defaultValue:
        spinbox.setValue(defaultValue)
    return spinbox


@bindsToClass
def Custom(
    owner: QWidget,
    name: str,
    widget: QWidget
):
    """Wraps any sort of custom Widget so it can fit in the QtWrapper paradigm"""
    return widget


@bindsToClass
def GroupBox(
    title: str,  # Shown to user
    layout: QLayout,
    owner: QWidget = None,
    name: str = None
) -> QGroupBox:
    horizontalBoxLayout = QGroupBox(title)
    horizontalBoxLayout.setLayout(layout)

    return horizontalBoxLayout


@bindsToClass
def HorizontalBoxLayout(
    owner: QWidget = None,
    name: str = None,
    margins: Optional[Tuple[int, int, int, int]] = None,
    contents: List[Union[QWidget, QLayout]] = []
) -> QHBoxLayout:
    """[summary]

    Args:
        owner (QWidget): The class to which the property will be added
        name (str): The property name of the created object in the class (not seen by users)
        margins (Tuple[int, int, int, int]): left, top, right, bottom
        contents (List[Union[QWidget, QLayout]])

    Returns:
        QVBoxLayout
    """
    horizontalBoxLayout = QHBoxLayout()

    if margins is not None:
        left, top, right, bottom = margins
        horizontalBoxLayout.setContentsMargins(left, top, right, bottom)

    for item in contents:
        if issubclass(type(item), QWidget):
            horizontalBoxLayout.addWidget(cast(QWidget, item))
        elif issubclass(type(item), QLayout):
            horizontalBoxLayout.addLayout(cast(QLayout, item))

    return horizontalBoxLayout


@bindsToClass
def HorizontalSlider(
    owner: QWidget = None,
    name: str = None,
) -> QSlider:
    """[summary]"""
    return QSlider(QtCore.Qt.Horizontal)


@bindsToClass
def HorizontalSplitter(
    contents=List[QWidget],
    owner: QWidget = None,
    name: str = None,
) -> QSplitter:
    splitter = QSplitter(QtCore.Qt.Horizontal)

    # NOTE: Splitters can only have QWidgets as children---not QLayouts
    for widget in contents:
        splitter.addWidget(widget)

    return splitter


@bindsToClass
def Label(
    text: str,
    owner: QWidget = None,
    name: str = None
) -> QLabel:

    return QLabel(text)


@bindsToClass
def Menu(
    items: List[Union[QAction, Separator]],
    owner: QWidget = None,
    name: str = None,
    displayName: str = None
) -> QMenu:
    """Creates a QMenu

    Args:
        owner (QWidget): The class to which the Menu property will be added
        name (str): The property name of the Menu in the class (not seen by users)
        displayName (str): The Menu name displayed to the user
        items (List[Union[QAction, Separator]]): Items to display in the menu

    Returns:
        QMenu: Menu
    """
    menu = QMenu(displayName)  # In this case the `owner` is the main window
    for item in items:
        if type(item) is Separator:
            menu.addSeparator()
            # Cast `item` : `Union[QAction, Separator] -> QAction` for mypy
        elif type(item) is QAction:
            menu.addAction(cast(QAction, item))

    return menu


@bindsToClass
def MenuAction(
    shortcut: Optional[Union[str, QtGui.QKeySequence]],
    statusTip: Optional[str],
    owner: QWidget = None,
    name: str = None,
    displayName: str = None
) -> QAction:
    """Creates a MenuAction

    Args:
        owner (QWidget): The class to which the Menu property will be added
        name (str): The property name of the Menu in the class (not seen by users)
        displayName (str): The name displayed to the user in the menu list for this action
        shortcut (Union[str, QtGui.QKeySequence]): The keyboard shortcut to trigger the action
        statusTip (str): ???
    """
    action = QAction(
        '&' + displayName, owner
    ) if displayName else QAction(owner) # In this case the owner is the main window
    if shortcut:
        action.setShortcut(shortcut)
    if statusTip:
        action.setStatusTip(statusTip)

    return action


@bindsToClass
def MenuBar(
    owner: QMainWindow, menus: List[QMenu], name: str = None
) -> QMenuBar:
    """Creates a QMenuBar

    Args:
        owner (QMainWindow): The MainWindow to which the MenuBar will be added
        name (str): The name of the MenuBar property
        menus (List[QMenu]): Menus container in the MenuBar

    Returns:
        QMenuBar: The menubar created
    """
    # In this case the `owner` is the main window
    menuBar = owner.menuBar()  # type: QMenuBar
    for menu in menus:
        menuBar.addMenu(menu)

    return menuBar


@bindsToClass
def PushButton(
    owner: QWidget = None,
    name: str = None,
    icon: Optional[QtGui.QIcon] = None,
    text: str = ""
) -> QPushButton:
    if icon is not None:
        button = QPushButton(icon, text)
    else:
        button = QPushButton(text)

    return button


@bindsToClass
def RadioButton(
    text: str, owner: QWidget = None, name: str = None
) -> QRadioButton:
    return QRadioButton(text)


@bindsToClass
def ScrollArea(
    innerWidget: QWidget,
    owner: Optional[QWidget] = None,
    name: Optional[str] = None,
    horizontalScrollBarPolicy: Optional[QtCore.Qt.ScrollBarPolicy] = None,
    verticalScrollBarPolicy: Optional[QtCore.Qt.ScrollBarPolicy] = None,
    widgetIsResizable: Optional[bool] = None
) -> QScrollArea:
    """[summary]"""

    scrollArea = QScrollArea()

    if horizontalScrollBarPolicy is not None:
        scrollArea.setHorizontalScrollBarPolicy(horizontalScrollBarPolicy)

    if verticalScrollBarPolicy is not None:
        scrollArea.setVerticalScrollBarPolicy(verticalScrollBarPolicy)

    if widgetIsResizable is not None:
        scrollArea.setWidgetResizable(widgetIsResizable)

    scrollArea.setWidget(innerWidget)

    return scrollArea


@bindsToClass
def TabWidget(
    tabs: List[Tab],
    owner: Optional[QWidget] = None,
    name: Optional[str] = None,
) -> QTabWidget:
    """[summary]"""

    tabWidget = QTabWidget()

    for tab in tabs:
        tabWidget.addTab(tab.widget, tab.label)

    return tabWidget


@bindsToClass
def StackedWidget(
    widgets: List[QWidget],
    owner: Optional[QWidget] = None,
    name: Optional[str] = None,
) -> QStackedWidget:
    """[summary]"""

    stackedWidget = QStackedWidget()

    for widget in widgets:
        stackedWidget.addWidget(widget)

    return stackedWidget


@bindsToClass
def VerticalBoxLayout(
    owner: QWidget = None,
    name: str = None,
    margins: Optional[Tuple[int, int, int, int]] = None,
    contents: List[Union[QWidget, QLayout]] = []
) -> QVBoxLayout:
    """[summary]

    Args:
        owner (QWidget): The class to which the property will be added
        name (str): The property name of the created object in the class (not seen by users)
        margins (Tuple[int, int, int, int]): left, top, right, bottom
        contents (List[Union[QWidget, QLayout]])

    Returns:
        QVBoxLayout
    """
    verticalBoxLayout = QVBoxLayout()

    if margins is not None:
        left, top, right, bottom = margins
        verticalBoxLayout.setContentsMargins(left, top, right, bottom)

    for item in contents:
        if issubclass(type(item), QWidget):
            verticalBoxLayout.addWidget(cast(QWidget, item))
        elif issubclass(type(item), QLayout):
            verticalBoxLayout.addLayout(cast(QLayout, item))

    return verticalBoxLayout


@bindsToClass
def VerticalSplitter(
    contents=List[QWidget],
    owner: QWidget = None,
    name: str = None
) -> QSplitter:
    splitter = QSplitter(QtCore.Qt.Vertical)

    # NOTE: Splitters can only have QWidgets as children---not QLayouts
    for widget in contents:
        splitter.addWidget(widget)

    return splitter


@bindsToClass
def Widget(
    owner: QWidget = None,
    name: str = None,
    horizontalPolicy: Optional[QSizePolicy.Policy] = None,
    verticalPolicy: Optional[QSizePolicy.Policy] = None,
    layout: Optional[QLayout] = None
) -> QWidget:
    """[summary]

    Args:
        owner (QWidget): [description]
        name (str): [description]
        layout (QLayout): [description]
        horizontalPolicy (QSizePolicy.Policy, optional): [description]. Defaults to None.
        verticalPolicy (QSizePolicy.Policy, optional): [description]. Defaults to None.

    Returns:
        QWidget: [description]
    """
    widget = QWidget()

    sizePolicy = widget.sizePolicy()

    if horizontalPolicy is not None:
        sizePolicy.setHorizontalPolicy(horizontalPolicy)

    if verticalPolicy is not None:
        sizePolicy.setVerticalPolicy(verticalPolicy)

    widget.setSizePolicy(sizePolicy)

    if layout is not None:
        widget.setLayout(layout)

    return widget


@bindsToClass
def LineEdit(
    owner: QWidget = None,
    name: str = None,
    contents: str = "",
    readOnly: bool = False
) -> QLineEdit:

    lineEdit = QLineEdit()
    lineEdit.setText(contents)
    lineEdit.setReadOnly(readOnly)
    return lineEdit

@bindsToClass
def FormLayout(
    contents: List[Tuple[QWidget, QWidget]],
    name: Optional[str] = None,
    owner: Optional[QWidget] = None
) -> QFormLayout:

    layout = QFormLayout()

    for item in contents:
        item1, item2 = item
        layout.addRow(item1, item2)

    return layout