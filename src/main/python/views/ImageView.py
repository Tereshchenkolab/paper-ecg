"""
ImageView.py
Created November 1, 2020

...
"""

from PyQt5 import QtGui, QtCore, QtWidgets
import os, sys

# From: https://github.com/drmatthews/slidecrop_pyqt/blob/master/slidecrop/gui/roi.py#L116
class ROIItem(QtWidgets.QGraphicsRectItem):

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = +8.0
    handleSpace = -4.0


    handleCursors = {
        handleTopLeft: QtCore.Qt.SizeFDiagCursor,
        handleTopMiddle: QtCore.Qt.SizeVerCursor,
        handleTopRight: QtCore.Qt.SizeBDiagCursor,
        handleMiddleLeft: QtCore.Qt.SizeHorCursor,
        handleMiddleRight: QtCore.Qt.SizeHorCursor,
        handleBottomLeft: QtCore.Qt.SizeBDiagCursor,
        handleBottomMiddle: QtCore.Qt.SizeVerCursor,
        handleBottomRight: QtCore.Qt.SizeFDiagCursor,
    }

    def __init__(self, parent, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        # Pixel data within the bounding box region
        self.pixelData = None
        
        # Minimum width and height of box (in pixels)
        self.minHeight = 50
        self.minWidth = 50
        
        # QGraphicsScene that contains this ROIItem instance
        self.parentScene = parent

        # QGraphicsView that displays the parentScene
        self.parentViews = self.parentScene.views()

        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = QtCore.Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(QtCore.Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()

        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)
            self.updateHandlesPos()

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()
        mappedBox = self.mapToScene(self.boundingRect()).boundingRect()
        print("box location: ", mappedBox)
        self.pixelData = self.parentViews[0]._image.pixmap().copy(mappedBox.toRect())
        self.pixelData.save("test.png")
        

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()

        self.handles[self.handleTopLeft] = QtCore.QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QtCore.QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QtCore.QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QtCore.QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QtCore.QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QtCore.QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QtCore.QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QtCore.QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QtCore.QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleTopLeft:
            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if boundingRect.bottom() - toY > self.minHeight:
                diff.setY(toY - fromY)
                boundingRect.setTop(toY)
                rect.setTop(boundingRect.top() + offset)
            if boundingRect.right() - toX > self.minWidth:
                diff.setX(toX - fromX)
                boundingRect.setLeft(toX)
                rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if boundingRect.bottom() - toY > self.minHeight:
                diff.setY(toY - fromY)
                boundingRect.setTop(toY)
                rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if boundingRect.bottom() - toY > self.minHeight: 
                diff.setY(toY - fromY)
                boundingRect.setTop(toY)
                rect.setTop(boundingRect.top() + offset)
            if toX - boundingRect.left() > self.minWidth:
                diff.setX(toX - fromX)
                boundingRect.setRight(toX)
                rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            if boundingRect.right() - toX > self.minWidth:
                diff.setX(toX - fromX)
                boundingRect.setLeft(toX)
                rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            if toX - boundingRect.left() > self.minWidth:
                diff.setX(toX - fromX)
                boundingRect.setRight(toX)
                rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if toY - boundingRect.top() > self.minHeight:
                diff.setY(toY - fromY)
                boundingRect.setBottom(toY)
                rect.setBottom(boundingRect.bottom() - offset)
            if boundingRect.right() - toX > self.minWidth:
                diff.setX(toX - fromX)
                boundingRect.setLeft(toX)
                rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if toY - boundingRect.top() > self.minHeight:
                diff.setY(toY - fromY)
                boundingRect.setBottom(toY)
                rect.setBottom(boundingRect.bottom() - offset)
                self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if toY - boundingRect.top() > self.minHeight:
                diff.setY(toY - fromY)
                boundingRect.setBottom(toY)
                rect.setBottom(boundingRect.bottom() - offset)
            if toX - boundingRect.left() > self.minWidth:
                diff.setX(toX - fromX)
                boundingRect.setRight(toX)
                rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        self.updateHandlesPos()

    def inBounds(self):
        mappedRect = self.mapToScene(self.boundingRect()).boundingRect()
        topLeft = mappedRect.topLeft()
        bottomLeft = mappedRect.bottomLeft()
        if topLeft.x() >= 0 and bottomLeft.x() >= 0:
            return True 

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QtGui.QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        # painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2.0, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 64)))
        painter.drawRect(self.rect())

        painter.setFont(QtGui.QFont('Default', 50))
        fontMetrics = QtGui.QFontMetrics(painter.font())

        if self.isSelected():
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 255)))
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0, 255), 2.0, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            for handle, rect in self.handles.items():
                # print(self.handles.items())
                # if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)
        else:
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Lead i")


# From: https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview 
class ImageView(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)

        self._scene = QtWidgets.QGraphicsScene(self)
        self._image = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._image)
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
        print("graphicsview size ", self.width(), "x", self.height())
        #if self.hasImage(): 
        #    self.fitInView(QtCore.QRectF(self._image.pixmap().rect()), QtCore.Qt.KeepAspectRatio)
        QtWidgets.QGraphicsView.resizeEvent(self, event)

    def hasImage(self):
        return not self._empty

    def setImage(self, pixmap=None):
        # Set it so the user can drag the image to pan
        #self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        #self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

        self._image.setPixmap(pixmap)
        self._empty = False
        self.fitInView(QtCore.QRectF(self._image.pixmap().rect()), QtCore.Qt.KeepAspectRatio)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

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

    #def fitInView(self, scale = True):
        # Fit image to QGraphicsView container
        #    rect = QtCore.QRectF(self._image.pixmap().rect())
        #    if not rect.isNull():
        #        self.setSceneRect(rect)
        #        if self.hasImage():
        #            unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
        #            self.scale(1 / unity.width(), 1 / unity.height())
        #            viewrect = self.viewport().rect()
        #            scenerect = self.transform().mapRect(rect)
        #            factor = min(viewrect.width() / scenerect.width(),
        #            viewrect.height() / scenerect.height())
        #            self.scale(factor, factor)
                    # Disable panning when image is fit to view
        #            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        #        self._zoom = 0 

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
                    self.fitInView(QtCore.QRectF(self._image.pixmap().rect()), QtCore.Qt.KeepAspectRatio)
                    self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                    self._zoom = 0
            else:
                print("scale not invertible")

    #def mousePressEvent(self, event):
    #    print("click pos: ", event.pos())
    #    pixel_coord = self.mapToScene(self.mapFromGlobal(event.globalPos()))
    #    print("pixel pos: ", pixel_coord.x(), ",", pixel_coord.y())
    #    QtWidgets.QGraphicsView.mousePressEvent(self, event)
    

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    image = "./fullScan.png"
    pixmap = QtGui.QPixmap(image)

    viewer = ImageView(None)
    viewer.setImage(pixmap)

    roi = ROIItem(viewer._scene)
    #roi.setRect(300, 100, 400, 200)
    #print(roi.isSelected())
    viewer._scene.addItem(roi)
    viewer.show()

    app.exec_()