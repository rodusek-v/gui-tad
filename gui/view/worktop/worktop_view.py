from PyQt6.QtCore import QEvent, QLineF, QObject, QPointF, QRect, QRectF, QSizeF, Qt
from PyQt6.QtGui import QMouseEvent, QPen, QResizeEvent, QWheelEvent
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QWidget

from view.worktop import GridScrollBar


class WorktopView(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMouseTracking(True)
        self.last_time_move = None
        self.setScene(QGraphicsScene())
        self.grid = []
        self.places = None
        self.addition = False
        self.grid_turn_on = False
        self.drag = False
        self.dragging = False

        self.h_scroll = GridScrollBar()
        self.v_scroll = GridScrollBar()
        self.setStyleSheet("background: white;")
        self.setHorizontalScrollBar(self.h_scroll)
        self.setVerticalScrollBar(self.v_scroll)
        self.h_scroll.sliderMoved.connect(self.__slider_change)
        self.v_scroll.sliderMoved.connect(self.__slider_change)

        self.setSceneRect(QRectF(QPointF(0, 0), QSizeF(self.size())))

    def __refresh_grid(self):
        if self.grid_turn_on:
            for cell in self.grid:
                self.scene().removeItem(cell)
            self.grid = []  
            self.__draw_grid()

    def __slider_change(self):
        if self.grid_turn_on:
            self.__refresh_grid()

    def __draw_grid(self):
        visible_rect = QRect(
            self.h_scroll.value(), 
            self.v_scroll.value(), 
            self.viewport().width(), 
            self.viewport().height())
        pen = QPen(Qt.GlobalColor.darkGray)
        pen.setDashPattern([10, 10])
        side = 100
        width = visible_rect.width()
        height = visible_rect.height()
        horizontal = int(width / side) + 2
        vertical = int(height / side) + 2
        x = int(visible_rect.x() / side) * 100
        y = int(visible_rect.y() / side) * 100
        for i in range(0, horizontal + 1):
            r = QLineF(
                QPointF(x + i*side, y - 100), 
                QPointF(x + i*side, y + height + 100))
            self.grid.append(self.scene().addLine(r, pen))
        for j in range(0, vertical + 1):
            r = QLineF(
                QPointF(x - 100, y + j*side), 
                QPointF(x + width + 100, y + j*side))
            self.grid.append(self.scene().addLine(r, pen))

        self.repaint()

    def __resize_scene(self, dx, dy):
        dx = abs(dx)
        dy = abs(dy)
        width = self.sceneRect().width()
        height = self.sceneRect().height()
        scene_x = self.sceneRect().x()
        scene_y = self.sceneRect().y()
        if self.h_scroll.is_at_maximum():
            width += dx
        elif self.h_scroll.is_at_minimum():
            scene_x -= dx
            width += dx

        if self.v_scroll.is_at_maximum():
            height += dy
        elif self.v_scroll.is_at_minimum():
            scene_y -= dy
            height += dy

        self.setSceneRect(scene_x, scene_y, width, height)

    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.sceneRect().width()
        height = self.sceneRect().height()
        if event.size().width() > width:
            width = event.size().width()

        if event.size().height() > height:
            height = event.size().height()
        self.setSceneRect(QRectF(QPointF(0, 0), QSizeF(width, height)))
        return super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.grid_turn_on:
            self.__refresh_grid()
        if self.places:
            self.__resize_scene(0, 20)
        return super().wheelEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.places is not None and not self.addition and self.dragging:
            if self.grid_turn_on:
                self.__refresh_grid()
            if self.last_time_move is None:
                self.last_time_move = event.position()

            dx = self.last_time_move.x() - event.position().x()
            dy = self.last_time_move.y() - event.position().y()
            self.__resize_scene(dx, dy)

            self.h_scroll.move_scroll_bar(dx)
            self.v_scroll.move_scroll_bar(dy)
            self.last_time_move = event.position()

        return super().mouseMoveEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.drag:
            self.dragging = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        if self.addition:
            adding_point = QPointF(
                event.position().x() + self.h_scroll.value(),
                event.position().y() + self.v_scroll.value())
            x = int(adding_point.x() / 100)
            y = int(adding_point.y() / 100)
            if adding_point.x() < 0:
                x -= 1
            if adding_point.y() < 0:
                y -= 1
            
            ta = QWidget()
            ta.setStyleSheet("background: red;")
            ta.setGeometry(x * 100 + 10, y * 100 + 10, 80, 80)

            new_place = self.scene().addWidget(ta)
            if self.places is None:
                self.places = self.scene().createItemGroup([new_place])
            else:
                self.places.addToGroup(new_place)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.last_time_move = None
        if self.drag:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            self.dragging = False
        return super().mouseReleaseEvent(event)

    def toggle_addition(self):
        self.addition = not self.addition
        if self.addition:
            self.setCursor(Qt.CursorShape.UpArrowCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def toggle_grid(self):
        self.grid_turn_on = not self.grid_turn_on
        if self.grid_turn_on:
            self.__draw_grid()
        else:
            for cell in self.grid:
                self.scene().removeItem(cell)
            self.grid = []  

    def toggle_drag(self):
        self.drag = not self.drag
        if self.drag:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            