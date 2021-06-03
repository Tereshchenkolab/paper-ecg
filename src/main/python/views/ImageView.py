"""
ImageView.py
Created November 1, 2020

...
"""
import sys
from typing import Any

from PyQt5 import QtGui, QtCore, QtWidgets

import ImageUtilities
from views.ROIView import ROI_ITEM_TYPE
from model.Lead import Lead, LeadId


MACOS_SCROLL_KEYS = {QtCore.Qt.Key_Meta}  # Option key
# TODO: Try to find a way for the command key to work? A keydownEvent is registered for CMD+O, but
# no keyupEvent fires because the file selector window steals focus without the main window noticing that it
# lost focus. (ARGH!!!)
SCROLL_STEP_FACTOR= 1.5


onMacOS = sys.platform == "darwin"


# From: https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
class ImageView(QtWidgets.QGraphicsView):
    roiItemSelected = QtCore.pyqtSignal(str, bool)
    updateRoiItem = QtCore.pyqtSignal(object)
    updateScale = QtCore.pyqtSignal(float)

    def __init__(self):
        super().__init__()

        self._zoom = 0
        self._scale = 1
        self._empty = True
        self._imageRect = None
        self._macosScrollKey = False

        self._scene = QtWidgets.QGraphicsScene(self)
        self._container = ImageView.createContainer()  # Permits rotation mechanics
        self._pixmapItem = QtWidgets.QGraphicsPixmapItem(parent=self._container)  # The pixmap form of the image data
        self._scene.addItem(self._container)

        self.setMinimumSize(600, 400) # What does this do?
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.addShortcuts()


    def addShortcuts(self):
        """ Enable ctrl+ and ctrl- shortcuts for zoom in/out """
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

    @staticmethod
    def createContainer():
        container = QtWidgets.QGraphicsRectItem()
        container.setPen(QtGui.QPen(QtCore.Qt.NoPen))  # Hide the border
        container.setFlag(container.ItemClipsChildrenToShape)  # Clip the rotated corners
        container.setBrush(QtCore.Qt.white)  # default
        return container

    def setContainerBackground(self, color: Any):
        # TODO Figure out how to set the color correctly
        self._container.setBrush(QtCore.Qt.white)

    @property
    def imageRect(self):
        return QtCore.QRectF(self._pixmapItem.pixmap().rect())

    def imageChanged(self):
        print("Image changed")
        newRect = self.imageRect
        self._scene.setSceneRect(newRect)
        self._container.setRect(newRect)

    def resizeEvent(self, event):
        if self.hasImage() and not self.verticalScrollBar().isVisible() and not self.horizontalScrollBar().isVisible():
           self.fitInView(self.imageRect, QtCore.Qt.KeepAspectRatio)

        super().resizeEvent(event)

    def hasImage(self):
        return not self._empty

    def setImage(self, image=None):
        print("Image set")
        self._pixmapItem.setPixmap(ImageUtilities.opencvImageToPixmap(image))
        self._empty = False
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

        # Show the image background container
        self._container.setVisible(True)

        self.rotateImage(0)

        # Set rotation origin in the center of the image
        pixmapSize = self._pixmapItem.pixmap().size()
        self._pixmapItem.setTransformOriginPoint(pixmapSize.width() // 2, pixmapSize.height() // 2)

        self.imageChanged()

    def fitImageInView(self):
        self.fitInView(self.imageRect, QtCore.Qt.KeepAspectRatio)

    def removeImage(self):
        self._image = None
        self._pixmapItem.setPixmap(QtGui.QPixmap())
        self._empty = True

        # Hide the image background container
        self._container.setVisible(False)

        self.rotateImage(0)

    def removeAllRoiBoxes(self):
        # remove roi boxes from scene
        for item in self._scene.items():
            if item.type == ROI_ITEM_TYPE:
                self._scene.removeItem(item)

    def removeRoiBox(self, leadId):
        # remove indiviudual roi from scene
        for item in self._scene.items():
            if item.type == ROI_ITEM_TYPE and item.leadId == leadId:
                self._scene.removeItem(item)

    def getAllLeadRoisAsDict(self):
        # return all lead ROIs present in the scene as a dictionary with LeadId:Lead pairs
        leads = {}
        for item in self._scene.items():
            if item.type == ROI_ITEM_TYPE:
                leads[LeadId[item.leadId]] = Lead(x=item.x, y=item.y, width=item.width, height=item.height, startTime=item.startTime)
        return leads

    def getLeadRoiStartTime(self, leadId):
        # get start time for specific lead (looking into a way to do this without looping through all items in scene)
        for item in self._scene.items():
            if item.type == ROI_ITEM_TYPE and item.leadId == leadId:
                return item.startTime

    def setLeadRoiStartTime(self, leadId, startTime):
        # set start time for specific lead (looking into a way to do this without looping through all items in scene)
        for item in self._scene.items():
            if item.type == ROI_ITEM_TYPE and item.leadId == leadId:
                item.startTime = startTime

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if onMacOS and event.key() in MACOS_SCROLL_KEYS:
            self._macosScrollKey = True
        return super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if onMacOS and event.key() in MACOS_SCROLL_KEYS:
            self._macosScrollKey = False
        return super().keyPressEvent(event)

    def event(self, event):
        # Detects pinching gesture on macOS
        # Examples: https://doc.qt.io/qt-5/qtwidgets-gestures-imagegestures-example.html
        if isinstance(event, QtGui.QFocusEvent):
            if event.lostFocus():
                self._macosScrollKey = False

        if isinstance(event, QtGui.QNativeGestureEvent) and event.gestureType() == QtCore.Qt.ZoomNativeGesture:
            pinchAmount = event.value()
            self.smoothZoom(pinchAmount)

        return super().event(event)

    def wheelEvent(self, event):
        if onMacOS:
            if self._macosScrollKey:
                self.smoothZoom(event.angleDelta().y() / 750)
            else:
                super().wheelEvent(event)
        else: # Zoom in and out using mouse wheel
            if event.angleDelta().y() > 0:
                self.zoomIn()
            else:
                self.zoomOut()

    # def updatePixelSizeOnScreen(self):
    #     print()
    #     graphicsViewRect = self.rect()
    #     viewWidth, viewHeight = graphicsViewRect.width(), graphicsViewRect.height()
    #     imageWidth, imageHeight = self.imageRect.width(), self.imageRect.height()
    #     print(viewWidth, viewHeight, imageWidth, imageHeight)

    def smoothZoom(self, amount: float):
        """ Zooming in and out on macOS needs to be proportion to the strength of the user interaction """
        scaleChange = (1 + amount)
        new_scale = self._scale * scaleChange
        if (self._scale > 1 or amount > 0) and new_scale >= 1:
            self._scale = new_scale
            self.scale(scaleChange, scaleChange)
        else:  # Snap image to the window so it's never smaller than the canvas
            self.fitInView(QtCore.QRectF(self._pixmapItem.pixmap().rect()), QtCore.Qt.KeepAspectRatio)
            self._scale = 1

    #zoomIn and zoomOut based on: https://stackoverflow.com/questions/57713795/zoom-in-and-out-in-widget
    def zoomIn(self):
        if self.hasImage():
            transformScale = QtGui.QTransform()
            transformScale.scale(SCROLL_STEP_FACTOR, SCROLL_STEP_FACTOR)

            transform = self.transform() * transformScale
            self.setTransform(transform)
            self._zoom += 1

            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def zoomOut(self):
        if self.hasImage():
            transformScale = QtGui.QTransform()
            transformScale.scale(SCROLL_STEP_FACTOR, SCROLL_STEP_FACTOR)
            invertedScale, invertible = transformScale.inverted()

            if invertible:
                if self._zoom > 1:
                    transform = self.transform() * invertedScale
                    self.setTransform(transform)
                    self._zoom -= 1
                elif self._zoom == 1:
                    self.fitInView(self.imageRect, QtCore.Qt.KeepAspectRatio)
                    self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                    self._zoom = 0
            else:
                print("scale not invertible")

    def rotateImage(self, rotation: float):
        # The QGraphics notion of rotation is opposite standard angle meaning
        self._pixmapItem.setRotation(rotation * -1)