from PyQt6 import QtCore
from PyQt6.QtCore import QEvent, QObject, QPointF, QRect, QRectF, QSizeF, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPen, QResizeEvent
from view.worktop import GridScrollBar
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView


class WorktopView(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.last_time_move = None
        self.setScene(QGraphicsScene())
        self.grid = None
        self.places = None
        self.addition = False

        self.h_scroll = GridScrollBar()
        self.v_scroll = GridScrollBar()
        self.setStyleSheet("background: white;")
        self.setHorizontalScrollBar(self.h_scroll)
        self.setVerticalScrollBar(self.v_scroll)

        self.setSceneRect(QRectF(QPointF(0, 0), QSizeF(self.size())))

    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.sceneRect().width()
        height = self.sceneRect().height()
        if event.size().width() > width:
            width = event.size().width()

        if event.size().height() > height:
            height = event.size().height()
        self.setSceneRect(QRectF(QPointF(0, 0), QSizeF(width, height)))
        return super().resizeEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self.addition:
            if self.last_time_move is None:
                self.last_time_move = event.position()

            dx = self.last_time_move.x() - event.position().x()
            dy = self.last_time_move.y() - event.position().y()

            width = self.sceneRect().size().width()
            height = self.sceneRect().size().height()
            if self.h_scroll.is_at_maximum():
                width += abs(dx)
            if self.h_scroll.is_at_minimum():
                width += abs(dx)

            if self.v_scroll.is_at_maximum():
                height += abs(dy)
            if self.v_scroll.is_at_minimum():
                height += abs(dy)
            self.setSceneRect(0, 0, width, height)

            self.h_scroll.move_scroll_bar(dx)
            self.v_scroll.move_scroll_bar(dy)
            self.last_time_move = event.position()
            return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.last_time_move = None
        return super().mouseReleaseEvent(event)

    def __draw_grid(self):
        temp = QRect(0, 0, self.viewport().width(), self.viewport().height())
        visible_rect = self.mapToScene(temp).boundingRect()

        pen = QPen(Qt.GlobalColor.black)
        side = 100
        horizontal = int(visible_rect.width() / side) + 2
        vertical = int(visible_rect.height() / side) + 2
        x = int(visible_rect.x() / side) * 100
        y = int(visible_rect.y() / side) * 100
        self.grid = []
        for i in range(horizontal):
            for j in range(vertical):
                r = QRectF(QPointF(x + i*side, y + j*side), QSizeF(side, side))
                self.grid.append(self.scene().addRect(r, pen))

    def toggle_addition(self):
        self.addition = not self.addition
        print(len(self.scene().items()))
        if self.addition:
            self.setCursor(Qt.CursorShape.UpArrowCursor)
            self.__draw_grid()
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            for cell in self.grid:
                self.scene().removeItem(cell)
            self.grid = []
            