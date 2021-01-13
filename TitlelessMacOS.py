from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QEvent
import objc, AppKit

from src.main.python.QtWrapper import *

# Source: https://github.com/razaqq/PotatoAlert/blob/44b251ea4b32bba87133b7d5a548a09ef77eae65/assets/qtmodern/_borderless/darwin.py
class MacOSWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Save a reference to the underlying NSWindow
        windowID = int(self.winId())
        nativeView = objc.objc_object(c_void_p=windowID)
        self._nativeWindow = nativeView.window()

        # Add an empty toolbar that later be combined with the titlebar
        toolbar = AppKit.NSToolbar.alloc().init()
        toolbar.setShowsBaselineSeparator_(False)
        self._nativeWindow.setToolbar_(toolbar)

        self._hideTitleBar()

    def changeEvent(self, event):
        super().changeEvent(event)
        # FIX for QTBUG-69975
        if event.type() == QEvent.WindowStateChange:
            self._hideTitleBar()

    def paintEvent(self, event):
        super().paintEvent(event)
        # FIX: title bar re-appears on some occasions
        self._nativeWindow.setTitlebarAppearsTransparent_(True)

    def _hideTitleBar(self):
        # Make the title bar invisible
        self._nativeWindow.setTitlebarAppearsTransparent_(True)
        # Hide the window title text
        self._nativeWindow.setTitleVisibility_(AppKit.NSWindowTitleHidden)
        # Push the content to the top of the window
        self._insertStyleMask(AppKit.NSFullSizeContentViewWindowMask)
        # Expand the titlebar to be the size of the toolbar
        self._insertStyleMask(AppKit.NSUnifiedTitleAndToolbarWindowMask)

    def _insertStyleMask(self, mask):
        self._nativeWindow.setStyleMask_(self._nativeWindow.styleMask() | mask)

if __name__ == '__main__':
    app = QApplication([])

    window = MacOSWindow()

    groupBox = QtWidgets.QGroupBox("Exclusive Radio Buttons")

    radio1 = QtWidgets.QRadioButton("Radio button 1")
    radio2 = QtWidgets.QRadioButton("Radio button 2")
    radio3 = QtWidgets.QRadioButton("Radio button 3")

    radio1.setChecked(True)

    vbox = QtWidgets.QVBoxLayout()
    vbox.addWidget(radio1)
    vbox.addWidget(radio2)
    vbox.addWidget(radio3)
    vbox.addStretch(1)

    groupBox.setLayout(vbox)

    HorizontalBoxLayout(window, "mainLayout", margins=(30,60,30,30), contents=[
        groupBox
    ])

    mainContainer = QtWidgets.QWidget()
    mainContainer.setLayout(window.mainLayout)

    window.setCentralWidget(mainContainer)

    window.setWindowTitle("Testing")
    window.show()

    app.exec_()