"""
ImageView.py
Created November 1, 2020

...
"""

from PyQt5 import QtGui, uic, QtCore, QtWidgets
import os, sys


# From: https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
class ImageView(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)

        self._scene = QtWidgets.QGraphicsScene(self)
        self._image = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._image)

        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def setImage(self, pixmap=None):
        # Set it so the user can drag the image to pan
        # self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

        self._image.setPixmap(pixmap)

    def event(self, event):
        # Detects pinching gesture on macOS
        # Examples: https://doc.qt.io/qt-5/qtwidgets-gestures-imagegestures-example.html
        if type(event) is QtGui.QNativeGestureEvent:
            pinchAmount = event.value()
            scale = (1 + pinchAmount)
            self.scale(scale, scale)

        return super().event(event)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    image = "./fullScan.png"
    pixmap = QtGui.QPixmap(image)

    viewer = ImageView(None)
    viewer.setImage(pixmap)

    viewer.show()

    app.exec_()