from PyQt6.QtCore import QEvent, QLineF, QPointF, QRect, QRectF, QSizeF, Qt
from PyQt6.QtGui import QBrush, QColor, QMouseEvent, QPen, QResizeEvent, QTransform, QWheelEvent
from PyQt6.QtWidgets import QGraphicsProxyWidget, QGraphicsScene, QGraphicsView, QWidget

from view.worktop import GridScrollBar
from view.worktop.action_selection import ActionSelector


class WorktopView(QGraphicsView):

    def __init__(self, action_selector: ActionSelector, parent=None, side=100):
        super().__init__(parent=parent)
        self.last_time_move = None
        self.grid = []
        self.places = None
        
        self.action_selector = action_selector
        self.action_selector.cursor_changed.connect(
            lambda: self.viewport().setCursor(self.action_selector.get_current_cursor())
        )
        self.action_selector.grid_changed.connect(
            lambda: self.__draw_grid() if self.action_selector.grid() else self.__delete_grid()
        )

        self.dragging = False
        self.selection = []
        
        self.hover_cell = None
        self.side = side

        self.h_scroll = GridScrollBar()
        self.v_scroll = GridScrollBar()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setStyleSheet("background: #f0f0f0;")
        self.setHorizontalScrollBar(self.h_scroll)
        self.setVerticalScrollBar(self.v_scroll)
        
        self.h_scroll.hide()
        self.v_scroll.hide()
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
        visible_rect = self.get_visible_rect()
        translated_visible_rect = visible_rect.translated(dx, dy)
        new_rect = translated_visible_rect.united(self.places.boundingRect())
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
        move_scroll = [True, True] 
        if self.sceneRect().width() > new_rect.width():
            move_scroll[0] = False
        if self.sceneRect().height() > new_rect.height():
            move_scroll[1] = False
        self.setSceneRect(new_rect)
        return move_scroll

    def __dragging(self, event: QMouseEvent):
        scene_point = QPointF(
            event.position().x() + self.h_scroll.value(),
            event.position().y() + self.v_scroll.value()
        )
        if self.action_selector.grid():
            self.__refresh_grid()
        if self.last_time_move is None:
            self.last_time_move = scene_point

        dx = self.last_time_move.x() - scene_point.x()
        dy = self.last_time_move.y() - scene_point.y()
        ind = self.__resize_scene(dx, dy)
        if ind[0]:
            self.h_scroll.move_scroll_bar(dx)
        if ind[1]:
            self.v_scroll.move_scroll_bar(dy)

        self.repaint()

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
            self.hover_cell = self.scene().addRect(r, pen, QColor(212, 212, 212))

    def __add_press(self, event: QMouseEvent):
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
            place = QWidget()
            place.setStyleSheet("""
                background: rgb(140, 140, 140);
            """)
            place.setGeometry(QRect(point.toPoint(), QSizeF(side_size, side_size).toSize()))
            new_place = self.scene().addWidget(place)

            if self.places is None:
                self.places = self.scene().createItemGroup([new_place])
            else:
                self.places.addToGroup(new_place)
            self.scene().removeItem(self.hover_cell)
            self.hover_cell = None

    def __selecting(self, event: QMouseEvent):
        select_point = QPointF(
            event.position().x() + self.h_scroll.value(),
            event.position().y() + self.v_scroll.value()
        )
        item = self.scene().itemAt(select_point, QTransform())

        if len(self.selection) != 0:
            for child in self.selection:
                if not isinstance(child, QGraphicsProxyWidget):
                    self.scene().removeItem(child)
            self.selection = []
        if self.places and item in self.places.childItems():
            item_rect = item.sceneBoundingRect()
            left_top_rect = self.create_selection_frame(item_rect.topLeft(), 4)
            right_top_rect = self.create_selection_frame(item_rect.topRight(), 4)
            left_bottom_rect = self.create_selection_frame(item_rect.bottomLeft(), 4)
            right_bottom_rect = self.create_selection_frame(item_rect.bottomRight(), 4)

            pen = QPen(Qt.GlobalColor.black)
            brush = QBrush(Qt.GlobalColor.white)

            self.selection.append(item)
            self.selection.append(self.scene().addRect(item_rect, pen))
            self.selection.append(self.scene().addRect(left_top_rect, pen, brush))
            self.selection.append(self.scene().addRect(right_top_rect, pen, brush))
            self.selection.append(self.scene().addRect(left_bottom_rect, pen, brush))
            self.selection.append(self.scene().addRect(right_bottom_rect, pen, brush))  

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
            ind = self.__resize_scene(0, -(event.angleDelta().y() / 6))
            if ind[1]:
                self.v_scroll.move_scroll_bar(-(event.angleDelta().y() / 6))
        #return super().wheelEvent(event)

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
            self.viewport().setCursor(self.action_selector.get_cursor("grab"))
        if self.action_selector.add():
            self.__add_press(event)
        if self.action_selector.select():
            self.__selecting(event)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.last_time_move = None
        if self.action_selector.drag():
            self.viewport().setCursor(self.action_selector.get_cursor("drag"))
            self.dragging = False
            
        return super().mouseReleaseEvent(event)

    def get_visible_rect(self):
        return QRectF(
            self.h_scroll.value(), 
            self.v_scroll.value(), 
            self.viewport().width() + 1, 
            self.viewport().height() + 1
        )

    @staticmethod
    def create_selection_frame(center_point, offset):
        return QRectF(
            center_point.x() - offset, 
            center_point.y() - offset,
            offset * 2, offset * 2
        )
    
    @staticmethod
    def move_by(items, dx, dy):
        for item in items:
            item.moveBy(dx, dy)
