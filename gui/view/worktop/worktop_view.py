from PyQt6.QtCore import QEvent, QLineF, QPointF, QRect, QRectF, QSizeF, Qt
from PyQt6.QtGui import QColor, QMouseEvent, QPen, QResizeEvent, QTransform, QWheelEvent
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QWidget

from view.worktop import GridScrollBar


class WorktopView(QGraphicsView):

    def __init__(self, action_selector, parent=None, side=100):
        super().__init__(parent=parent)
        self.last_time_move = None
        self.grid = []
        self.places = None
        
        self.action_selector = action_selector
        self.action_selector.cursor_changed.connect(
            lambda: self.setCursor(self.action_selector.get_current_cursor())
        )
        self.action_selector.grid_changed.connect(
            lambda: self.__draw_grid() if self.action_selector.grid() else self.__delete_grid()
        )

        self.dragging = False
        self.move_selection = None
        
        self.hover_cell = None
        self.side = side

        self.h_scroll = GridScrollBar()
        self.v_scroll = GridScrollBar()
        self.setStyleSheet("background: #f0f0f0;")
        self.setHorizontalScrollBar(self.h_scroll)
        self.setVerticalScrollBar(self.v_scroll)
        self.h_scroll.sliderMoved.connect(self.__slider_change)
        self.v_scroll.sliderMoved.connect(self.__slider_change)

        self.setMouseTracking(True)
        self.setScene(QGraphicsScene())

    def __refresh_grid(self):
        if self.action_selector.grid():
            self.__delete_grid()
            self.__draw_grid()
    
    def __delete_grid(self):
        for cell in self.grid:
            self.scene().removeItem(cell)
        self.grid = []

    def __slider_change(self):
        if self.action_selector.grid():
            self.__refresh_grid()

    def __draw_grid(self):
        visible_rect = self.get_visible_rect()
        pen = QPen(Qt.GlobalColor.darkGray)
        pen.setDashPattern([0, 5, 10, 5])
        width = visible_rect.width()
        height = visible_rect.height()
        horizontal = int(width / self.side) + 2
        vertical = int(height / self.side) + 2
        x = int(visible_rect.x() / self.side) * self.side
        y = int(visible_rect.y() / self.side) * self.side
        for i in range(0, horizontal + 1):
            r = QLineF(
                QPointF(x + i * self.side, y - self.side), 
                QPointF(x + i * self.side, y + height + self.side)
            )
            self.grid.append(self.scene().addLine(r, pen))
        for j in range(0, vertical + 1):
            r = QLineF(
                QPointF(x - self.side, y + j * self.side), 
                QPointF(x + width + self.side, y + j * self.side)
            )
            self.grid.append(self.scene().addLine(r, pen))

    def __resize_scene(self, dx, dy):
        current_scene = self.sceneRect()
        visible_rect = self.get_visible_rect()
        translated_visible_rect = visible_rect.translated(dx, dy)
        try:
            new_rect = translated_visible_rect.united(self.places.boundingRect())
        except:
            new_rect = translated_visible_rect
        new_scene = new_rect.united(current_scene)

        if current_scene == new_scene:
            left_top_point = None
            right_bottom_point = None
            if dx >= 0 and dy >= 0:
                left_top_point = new_rect.topLeft()
                right_bottom_point = current_scene.bottomRight()
            elif dx >= 0 and dy <= 0:
                left_top_point = QPointF(new_rect.x(), current_scene.y())
                right_bottom_point = QPointF(current_scene.topRight().x(), new_rect.bottomLeft().y())
            elif dx <= 0 and dy >= 0:
                left_top_point = QPointF(current_scene.x(), new_rect.topRight().y())
                right_bottom_point = QPointF(new_rect.topRight().x(), current_scene.bottomRight().y())
            else:
                left_top_point = current_scene.topLeft()
                right_bottom_point = new_rect.bottomRight()

            new_scene = QRectF(left_top_point, right_bottom_point)
            if self.size().width() - 5 > new_scene.width() or self.size().height() - 5 > new_scene.height():
                new_scene = current_scene
                
        if (translated_visible_rect.contains(new_rect.topLeft()) and \
            translated_visible_rect.contains(new_rect.topRight())) or \
                translated_visible_rect.contains(new_rect.bottomLeft()) and \
            translated_visible_rect.contains(new_rect.bottomRight()):
            self.h_scroll.hide()
        else:
            self.h_scroll.show()

        if (translated_visible_rect.contains(new_rect.topLeft()) and \
            translated_visible_rect.contains(new_rect.bottomLeft())) or \
                translated_visible_rect.contains(new_rect.topRight()) and \
            translated_visible_rect.contains(new_rect.bottomRight()):
            self.v_scroll.hide()
        else:
            self.v_scroll.show() 
        self.setSceneRect(new_scene)

    def __dragging(self, event: QMouseEvent):
        if self.action_selector.grid():
            self.__refresh_grid()
        if self.last_time_move is None:
            self.last_time_move = event.position()

        dx = self.last_time_move.x() - event.position().x()
        dy = self.last_time_move.y() - event.position().y()
        self.__resize_scene(dx, dy)
        self.h_scroll.move_scroll_bar(dx)
        self.v_scroll.move_scroll_bar(dy)
        self.last_time_move = event.position()

    def __add_hover(self, event: QMouseEvent):
        adding_point = QPointF(
            event.position().x() + self.h_scroll.value(),
            event.position().y() + self.v_scroll.value()
        )
        if self.hover_cell:
            self.scene().removeItem(self.hover_cell)
            self.hover_cell = None
        row = int(adding_point.x() / self.side)
        column = int(adding_point.y() / self.side)
        if adding_point.x() < 0:
            row -= 1
        if adding_point.y() < 0:
            column -= 1
        margin = 10
        side_size = self.side - margin * 2
        point = QPointF(row * self.side + margin, column * self.side + margin)
        item = self.scene().itemAt(point, QTransform())
        if self.places is None or item not in self.places.childItems():
            r = QRectF(point, QSizeF(side_size, side_size))
            pen = QPen(Qt.GlobalColor.black)
            pen.setDashPattern([0, 5, 10, 5])
            self.hover_cell = self.scene().addRect(r, pen, QColor(168, 168, 168))

    def resizeEvent(self, event: QResizeEvent) -> None:
        scene_x = self.sceneRect().x()
        scene_y = self.sceneRect().y()
        width = self.sceneRect().width()
        height = self.sceneRect().height()
        if event.size().width() > width:
            width = event.size().width()

        if event.size().height() > height:
            height = event.size().height()
        
        self.setSceneRect(QRectF(QPointF(scene_x, scene_y), QSizeF(width, height)))
        self.__refresh_grid()
        return super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.action_selector.grid():
            self.__refresh_grid()
        if self.places:
            self.__resize_scene(0, -(event.angleDelta().y() / 6))
        return super().wheelEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        add = self.action_selector.add()
        if add:
           self.__add_hover(event)
        if self.places is not None and not add and self.dragging:
            self.__dragging(event)

        return super().mouseMoveEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        if self.hover_cell:
            self.scene().removeItem(self.hover_cell)
            self.hover_cell = None
        return super().leaveEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.action_selector.drag():
            self.dragging = True
            self.setCursor(self.action_selector.get_cursor("grab"))
        if self.action_selector.add():
            adding_point = QPointF(
                event.position().x() + self.h_scroll.value(),
                event.position().y() + self.v_scroll.value()
            )
            row = int(adding_point.x() / self.side)
            column = int(adding_point.y() / self.side)
            if adding_point.x() < 0:
                row -= 1
            if adding_point.y() < 0:
                column -= 1
            margin = 10
            side_size = self.side - margin * 2
            point = QPointF(row * self.side + margin, column * self.side + margin)
            item = self.scene().itemAt(point, QTransform())
            if self.places is None or item not in self.places.childItems():
                ta = QWidget()
                ta.setStyleSheet("background: black;")
                ta.setGeometry(QRect(point.toPoint(), QSizeF(side_size, side_size).toSize()))

                new_place = self.scene().addWidget(ta)

                if self.places is None:
                    self.places = self.scene().createItemGroup([new_place])
                else:
                    self.places.addToGroup(new_place)
                self.scene().removeItem(self.hover_cell)
                self.hover_cell = None
        if self.action_selector.select():
            pass
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.last_time_move = None
        if self.action_selector.drag():
            self.setCursor(self.action_selector.get_cursor("drag"))
            self.dragging = False
        return super().mouseReleaseEvent(event)

    def get_visible_rect(self):
        return QRectF(
            self.h_scroll.value(), 
            self.v_scroll.value(), 
            self.viewport().width(), 
            self.viewport().height()
        )
