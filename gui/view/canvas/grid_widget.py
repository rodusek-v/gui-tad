from enum import Enum
from PyQt6 import QtGui
from PyQt6.QtCore import QPoint, Qt
from view.canvas.grid_scroll import GridScroll
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget


class Corner(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOT_LEFT = 2
    BOT_RIGHT = 3


class Grid(QFrame):

    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.grid_scroll = GridScroll(self)
        self.grid_scroll.setStyleSheet("background-color: #c9c5c5; border: none;")
        self.layout().setContentsMargins(10, 10, 0, 0)
        
        self.canvas = CanvasGrid(self.grid_scroll)
        self.__triggerBars()
        self.canvas.setStyleSheet("background-color: white")
        self.grid_scroll.setWidget(self.canvas)
        
        self.layout().addWidget(self.grid_scroll)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.__triggerBars()
        return super().resizeEvent(a0)

    def __triggerBars(self):
        height = self.grid_scroll.frameGeometry().height()
        width = self.grid_scroll.frameGeometry().width()
        size = self.canvas.size()
        if self.canvas.size().width() <= width:
            size.setWidth(width - 10)
        
        if self.canvas.size().height() <= height:
            size.setHeight(height - 10)

        self.canvas.resize(size)


        '''
        if not self.canvas.checkChildrenVisibility():
            if self.grid_scroll.verticalScrollBar().visibleRegion().isEmpty():
                size = self.canvas.size()
                size.setHeight(new_height - 10)
                self.canvas.resize(size)
                
            if self.grid_scroll.horizontalScrollBar().visibleRegion().isEmpty():   
                size = self.canvas.size()
                size.setWidth(new_width - 10)
                self.canvas.resize(size)
        '''

        #print(self.canvas.geometry().topLeft(), self.canvas.geometry().topRight(), self.canvas.geometry().bottomLeft(), self.canvas.geometry().bottomRight())

class CanvasGrid(QFrame):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.places = []
        self.places.append(QWidget(self))
        self.places[0].setGeometry(0, 0, 200, 200)
        self.places[0].setStyleSheet("background: blue;")

    def checkChildrenVisibility(self):
        self.__check_size()
        for child in self.places:
            if child.visibleRegion().isEmpty():
                return False
        return True

    def __check_size(self):
        geometry = self.geometry()
        for child in self.places:
            top_left = CanvasGrid.new_point(child.geometry().topLeft(), geometry.topLeft(), Corner.TOP_LEFT)
            top_right = CanvasGrid.new_point(child.geometry().topRight(), geometry.topRight(), Corner.TOP_RIGHT)
            bot_left = CanvasGrid.new_point(child.geometry().bottomLeft(), geometry.bottomLeft(), Corner.BOT_LEFT)
            bot_right = CanvasGrid.new_point(child.geometry().bottomRight(), geometry.bottomRight(), Corner.BOT_RIGHT)
        geometry.setBottomLeft(bot_left)
        geometry.setBottomRight(bot_right)
        geometry.setTopLeft(top_left)
        geometry.setTopRight(top_right)
        self.setGeometry(geometry)
        #print(self.geometry().topLeft(), self.geometry().topRight(), self.geometry().bottomRight(), self.geometry().bottomLeft())

    @staticmethod
    def new_point(point1, point2, corner):
        if corner == Corner.TOP_LEFT:
            if point1.x() < point2.x() and point1.y() < point2.y():
                return QPoint(point1)
            elif point1.x() < point2.x() and point1.y() > point2.y():
                return QPoint(point1.x(), point2.y())
            elif point1.x() > point2.x() and point1.y() < point2.y():
                return QPoint(point2.x(), point1.y())
            else:
                return QPoint(point2)
        elif corner == Corner.TOP_RIGHT:
            if point1.x() > point2.x() and point1.y() < point2.y():
                return QPoint(point1)
            elif point1.x() < point2.x() and point1.y() < point2.y():
                return QPoint(point2.x(), point1.y())
            elif point1.x() > point2.x() and point1.y() > point2.y():
                return QPoint(point1.x(), point2.y())
            else:
                return QPoint(point2)
        elif corner == Corner.BOT_LEFT:
            if point1.x() < point2.x() and point1.y() < point2.y():
                return QPoint(point1.x(), point2.y())
            elif point1.x() < point2.x() and point1.y() > point2.y():
                return QPoint(point1)
            elif point1.x() > point2.x() and point1.y() > point2.y():
                return QPoint(point2.x(), point1.y())
            else:
                return QPoint(point2)
        elif corner == Corner.BOT_RIGHT:
            if point1.x() > point2.x() and point1.y() > point2.y():
                return QPoint(point1)
            elif point1.x() > point2.x() and point1.y() > point2.y():
                return QPoint(point1.x(), point2.y())
            elif point1.x() < point2.x() and point1.y() > point2.y():
                return QPoint(point2.x(), point1.y())
            else:
                return QPoint(point2)
        else:
            raise Exception("ERROR")
                
    