import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
from model.Lead import LeadId

import ImageUtilities

# According the docs, custom items should have type >= UserType (65536)
# Setting the type allows you to distinguish between items in the graphics scene
# https://doc.qt.io/archives/qt-4.8/qgraphicsitem.html#UserType-var
ROI_ITEM_TYPE = QtWidgets.QGraphicsRectItem.UserType

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

    def __init__(self, parent, leadId, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)

        self.leadId = leadId
        self.startTime = 0.0

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

        # Set item type to identify ROI items in scene - according to custom items should
        # have type >= UserType (65536)
        self.type = ROI_ITEM_TYPE

    @property
    def x(self):
        return self.mapToScene(self.rect()).boundingRect().toRect().x()

    @property
    def y(self):
        return self.mapToScene(self.rect()).boundingRect().toRect().y()

    @property
    def width(self):
        return self.mapToScene(self.rect()).boundingRect().toRect().width()

    @property
    def height(self):
        return self.mapToScene(self.rect()).boundingRect().toRect().height()

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
        self.updateHandlesPos()
        self.mousePressPos = mouseEvent.pos()
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
            self.updateHandlesPos()
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None

        self.parentViews[0].updateRoiItem.emit(self)
        self.update()

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
        sceneRect = self.parentScene.sceneRect()
        boundingRect = self.boundingRect()
        mappedRect = self.mapToScene(self.boundingRect()).boundingRect()
        rect = self.rect()
        diff = QtCore.QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleTopLeft:
            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()

            if boundingRect.bottom() - toY > self.minHeight and mappedRect.y() - (boundingRect.y()-toY) >= sceneRect.top():
                diff.setY(toY - fromY)
                boundingRect.setTop(toY)
                rect.setTop(boundingRect.top() + offset)
            if boundingRect.right() - toX > self.minWidth and mappedRect.x() - (boundingRect.x()-toX) >= sceneRect.left():
                    diff.setX(toX - fromX)
                    boundingRect.setLeft(toX)
                    rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if boundingRect.bottom() - toY > self.minHeight and mappedRect.y() - (boundingRect.y()-toY) >= sceneRect.top():
                diff.setY(toY - fromY)
                boundingRect.setTop(toY)
                rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if boundingRect.bottom() - toY > self.minHeight and mappedRect.y() - (boundingRect.y()-toY) >= sceneRect.top():
                diff.setY(toY - fromY)
                boundingRect.setTop(toY)
                rect.setTop(boundingRect.top() + offset)
            if toX - boundingRect.left() > self.minWidth and mappedRect.topRight().x() - (boundingRect.topRight().x()-toX) <= sceneRect.right():
                diff.setX(toX - fromX)
                boundingRect.setRight(toX)
                rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            if boundingRect.right() - toX > self.minWidth and mappedRect.x() - (boundingRect.x()-toX) >= sceneRect.left():
                diff.setX(toX - fromX)
                boundingRect.setLeft(toX)
                rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            if toX - boundingRect.left() > self.minWidth and mappedRect.right() - (boundingRect.right()-toX) <= sceneRect.right():
                diff.setX(toX - fromX)
                boundingRect.setRight(toX)
                rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if toY - boundingRect.top() > self.minHeight and mappedRect.bottomLeft().y() - (boundingRect.bottomLeft().y()-toY) <= sceneRect.bottom():
                diff.setY(toY - fromY)
                boundingRect.setBottom(toY)
                rect.setBottom(boundingRect.bottom() - offset)
            if boundingRect.right() - toX > self.minWidth and mappedRect.x() - (boundingRect.x()-toX) >= sceneRect.left():
                diff.setX(toX - fromX)
                boundingRect.setLeft(toX)
                rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if toY - boundingRect.top() > self.minHeight and mappedRect.bottom() - (boundingRect.bottom()-toY) <= sceneRect.bottom():
                diff.setY(toY - fromY)
                boundingRect.setBottom(toY)
                rect.setBottom(boundingRect.bottom() - offset)
                self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            if toY - boundingRect.top() > self.minHeight and mappedRect.bottomRight().y() - (boundingRect.bottomRight().y()-toY) <= sceneRect.bottom():
                diff.setY(toY - fromY)
                boundingRect.setBottom(toY)
                rect.setBottom(boundingRect.bottom() - offset)
            if toX - boundingRect.left() > self.minWidth and mappedRect.bottomRight().x() - (boundingRect.bottomRight().x()-toX) <= sceneRect.right():
                diff.setX(toX - fromX)
                boundingRect.setRight(toX)
                rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        self.updateHandlesPos()


    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsRectItem.ItemPositionChange:
            if self.parentScene is not None:
                return self.restrictMovement(value)

        if change == QtWidgets.QGraphicsRectItem.ItemSelectedChange:
            self.parentViews[0].roiItemSelected.emit(self.leadId, value)
            if value == True:
                self.setZValue(1)
            else:
                self.setZValue(0)

        return QtWidgets.QGraphicsRectItem.itemChange(self, change, value)


    # https://stackoverflow.com/questions/55771100/how-do-i-reimplement-the-itemchange-and-mousemoveevent-of-a-qgraphicspixmapitem
    def restrictMovement(self, value):

        boxRect = self.mapToScene(self.boundingRect()).boundingRect()
        handleOffset = self.handleSpace
        sceneRect = self.parentScene.sceneRect()

        # 'value' represents the amount the item is being moved along the x,y plane so we calculate the actual (x,y) position the item is moving to
        x = value.x()+self.handles[self.handleTopLeft].x()
        y = value.y()+self.handles[self.handleTopLeft].y()

        relativeRect = QtCore.QRectF(sceneRect.topLeft(), sceneRect.size() - boxRect.size())

        # If item is being moved out of bounds, override the appropriate x,y values to keep item within scene
        if not relativeRect.contains(x, y):
            if x < 1:
                value.setX(sceneRect.left()-self.handles[self.handleTopLeft].x()+self.handleSpace)
            elif x+boxRect.width() >= sceneRect.width():
                value.setX(sceneRect.right()-boxRect.width()-self.handles[self.handleTopLeft].x()-self.handleSpace)
            if y < 1:
                value.setY(sceneRect.top()-self.handles[self.handleTopLeft].y()+self.handleSpace)
            elif y+boxRect.height() >= sceneRect.bottom():
                value.setY(sceneRect.bottom()-boxRect.height()-self.handles[self.handleTopLeft].y()-self.handleSpace)

        return QtCore.QPointF(value.x(), value.y())

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

        painter.setFont(QtGui.QFont('Default', 50))
        fontMetrics = QtGui.QFontMetrics(painter.font())

        if self.isSelected():
            # Set color (red) and draw box (when selected)
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2.0, QtCore.Qt.SolidLine))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 64)))
            painter.drawRect(self.rect())

            # Set color and paint resize handles
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 255)))
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0, 255), 2.0, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))

            for handle, rect in self.handles.items():
                painter.drawRect(rect)
        else:
            # Set color (grey) and draw box (unselected)
            painter.setPen(QtGui.QPen(QtGui.QColor(128, 128, 128), 2.0, QtCore.Qt.SolidLine))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(128, 128, 128, 64)))
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, self.leadId)
            painter.drawRect(self.rect())

