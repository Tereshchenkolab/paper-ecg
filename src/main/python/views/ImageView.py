"""
ImageView.py
Created November 1, 2020

...
"""
from PyQt5 import QtGui, QtCore, QtWidgets

import ImageUtilities


# From: https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
class ImageView(QtWidgets.QGraphicsView):
    roiItemSelected = QtCore.pyqtSignal(object, bool)
    
    def __init__(self):
        super().__init__()

        self.setMinimumSize(600, 400)

        self._scene = QtWidgets.QGraphicsScene(self)
        self._image = None                                  # OpenCV form of the image data - used for processing
        self._pixmapItem = QtWidgets.QGraphicsPixmapItem()  # The pixmap form of the image data - used for displaying
        self._scene.addItem(self._pixmapItem)
        self._zoom = 0
        self._scaleFactor = 1.5
        self._empty = True

        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        # Enable ctrl+ and ctrl- shortcuts for zoom in/out
        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.ZoomIn),
            self,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.zoomIn,
        )

        QtWidgets.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.ZoomOut),
            self,
            context=QtCore.Qt.WidgetShortcut,
            activated=self.zoomOut,
        )

    def resizeEvent(self, event):
        if self.hasImage() and not self.verticalScrollBar().isVisible() and not self.horizontalScrollBar().isVisible():
           self.fitInView(QtCore.QRectF(self._pixmapItem.pixmap().rect()), QtCore.Qt.KeepAspectRatio)
        QtWidgets.QGraphicsView.resizeEvent(self, event)

    def hasImage(self):
        return not self._empty

    def setImage(self, image=None):
        self._image = image
        self._pixmapItem.setPixmap(ImageUtilities.opencvImageToPixmap(image))
        self._empty = False
        self.fitInView(QtCore.QRectF(self._pixmapItem.pixmap().rect()), QtCore.Qt.KeepAspectRatio)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self._scene.setSceneRect(QtCore.QRectF(self._pixmapItem.pixmap().rect()))

        self.updateAllRoiBoxes()

    def updateAllRoiBoxes(self):
        # update pixel data for each roi present in the scene
        for item in self._scene.items():
            if item.type == QtWidgets.QGraphicsRectItem.UserType:
                item.updatePixelData()

    def removeImage(self):
        self._image = None
        self._pixmapItem.setPixmap(QtGui.QPixmap())
        self._empty = True

    def removeAllRoiBoxes(self):
        # remove roi boxes from scene
        for item in self._scene.items():
            if item.type == QtWidgets.QGraphicsRectItem.UserType:
                self._scene.removeItem(item)

    def removeRoiBox(self, lead):
        for item in self._scene.items():
            if item.type == QtWidgets.QGraphicsRectItem.UserType and item.leadId == lead.leadId:
                self._scene.removeItem(item)

    def event(self, event):
        # Detects pinching gesture on macOS
        # Examples: https://doc.qt.io/qt-5/qtwidgets-gestures-imagegestures-example.html
        if type(event) is QtGui.QNativeGestureEvent:
            pinchAmount = event.value()
            scale = (1 + pinchAmount)
            self.scale(scale, scale)

        return super().event(event)

    def wheelEvent(self, event):
        # Zoom in and out using mouse wheel
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    #zoomIn and zoomOut based on: https://stackoverflow.com/questions/57713795/zoom-in-and-out-in-widget
    def zoomIn(self):
        if self.hasImage():
            transformScale = QtGui.QTransform()
            transformScale.scale(self._scaleFactor, self._scaleFactor)

            transform = self.transform() * transformScale
            self.setTransform(transform)
            self._zoom += 1

            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def zoomOut(self):
        if self.hasImage():
            transformScale = QtGui.QTransform()
            transformScale.scale(self._scaleFactor, self._scaleFactor)
            invertedScale, invertible = transformScale.inverted()

            if invertible:
                if self._zoom > 1:
                    transform = self.transform() * invertedScale
                    self.setTransform(transform)
                    self._zoom -= 1
                elif self._zoom == 1:
                    self.fitInView(QtCore.QRectF(self._pixmapItem.pixmap().rect()), QtCore.Qt.KeepAspectRatio)
                    self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                    self._zoom = 0
            else:
                print("scale not invertible")
