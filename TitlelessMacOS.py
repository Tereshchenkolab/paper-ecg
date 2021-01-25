from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QEvent
import objc, AppKit

from PyQt5 import QtCore
import numpy as np
import qimage2ndarray as QImageConvert

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


class CustomTreeView(QtWidgets.QTreeView):

    def mouseDoubleClickEvent(self, event):
        print(event)
        print(self.selectedIndexes())


# def window(centralWidget, title):


def imageHotReloadDemo():
    imageView = QtWidgets.QLabel()
    imageView.setScaledContents(True)

    slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

    dummyImage = np.ones((100, 100,3),dtype=np.uint8)
    dummyImage = np.transpose(dummyImage, (1,0,2))

    qImage = QImageConvert.array2qimage(dummyImage)

    pixmap = QtGui.QPixmap(qImage)
    pixmap = pixmap.scaled(100,100, QtCore.Qt.KeepAspectRatio)
    imageView.setPixmap(pixmap)

    return VerticalBoxLayout(None, "", margins=(10,10,10,10), contents=[imageView, slider]), "Image Demo"

def fileBrowserDemo():

    model = QtWidgets.QFileSystemModel()
    model.setRootPath("/")
    tree = CustomTreeView()
    tree.setModel(model)
    tree.setAlternatingRowColors(True)

    return tree, "File Browser Demo"


if __name__ == '__main__':
    app = QApplication([])

    window = MacOSWindow()

    widget, title = fileBrowserDemo()
    # widget, title = imageHotReloadDemo()

    HorizontalBoxLayout(window, "mainLayout", margins=(0,38,0,0), contents=[
        widget
    ])

    mainContainer = QtWidgets.QWidget()
    mainContainer.setLayout(window.mainLayout)

    window.setCentralWidget(mainContainer)

    window.setWindowTitle(title)
    window.show()




    app.exec_()