from PyQt6.QtCore import QEvent, QLineF, QPoint, QPointF, QRectF, QSizeF, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QKeyEvent, QMouseEvent, QPen, QResizeEvent, QTransform, QWheelEvent
from PyQt6.QtWidgets import QGraphicsProxyWidget, QGraphicsScene, QGraphicsView

from view.worktop import GridScrollBar
from view.worktop.action_selection import ActionSelector
from view.worktop.place_item import PlaceItem, Sides


class WorktopView(QGraphicsView):

    viewport_change = pyqtSignal(QPoint)

    def __init__(self, action_selector: ActionSelector, parent=None, side=100, margin=5):
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
        self.selection = {
            "item": None,
            "boundries": []
        }
        
        self.hover_cell = None
        self.side = side
        self.margin = margin
        self.dash_pattern = [0, self.side / 20, self.side / 10, self.side / 20]

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
        self.setInteractive(False)

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
        pen.setDashPattern(self.dash_pattern)
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
            cell = self.scene().addLine(r, pen)
            cell.setZValue(-100)
            self.grid.append(cell)
        for j in range(0, vertical + 1):
            r = QLineF(
                QPointF(x - self.side, y + j * self.side), 
                QPointF(x + width + self.side, y + j * self.side)
            )
            cell = self.scene().addLine(r, pen)
            cell.setZValue(-100)
            self.grid.append(cell)

    def __resize_scene(self, dx=0, dy=0):
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
        self.viewport_change.emit(translated_visible_rect.topLeft().toPoint())
        return move_scroll

    def __dragging(self, event: QMouseEvent):
        scene_point = self.get_scene_point(event.position())
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

    def __add_place_hover(self, event: QMouseEvent):
        adding_point = self.get_scene_point(event.position())
        if self.hover_cell:
            self.scene().removeItem(self.hover_cell)
            self.hover_cell = None
        space_rect = self.is_space_available(adding_point)
        if space_rect:
            pen = QPen(Qt.GlobalColor.black)
            pen.setDashPattern(self.dash_pattern)
            self.hover_cell = self.scene().addRect(space_rect, pen, QColor(212, 212, 212))

    def __add_place_press(self, event: QMouseEvent):
        adding_point = self.get_scene_point(event.position())
        space_rect = self.is_space_available(adding_point)
        if space_rect:
            place = PlaceItem(margin=self.margin)
            place.setStyleSheet("""
                background: rgb(140, 140, 140);
            """)
            place.setGeometry(space_rect.toRect())
            new_place = self.scene().addWidget(place)

            if self.places is None:
                self.places = self.scene().createItemGroup([new_place])
            else:
                self.places.addToGroup(new_place)
            
            self.__check_neighbours(place)
            self.scene().removeItem(self.hover_cell)
            self.hover_cell = None
            self.__resize_scene()

    def __selecting(self, event: QMouseEvent):
        select_point = self.get_scene_point(event.position())
        item = self.scene().itemAt(select_point, QTransform())

        if self.selection["item"] is not None:
            for child in self.selection["boundries"]:
                self.scene().removeItem(child)

            self.selection["boundries"] = []
        if self.places and item in self.places.childItems():
            item_rect = item.sceneBoundingRect()
            left_top_rect = self.create_selection_frame(item_rect.topLeft(), 4)
            right_top_rect = self.create_selection_frame(item_rect.topRight(), 4)
            left_bottom_rect = self.create_selection_frame(item_rect.bottomLeft(), 4)
            right_bottom_rect = self.create_selection_frame(item_rect.bottomRight(), 4)

            pen = QPen(Qt.GlobalColor.black, 0.7)
            brush = QBrush(Qt.GlobalColor.white)

            self.selection["item"] = item
            self.selection["boundries"] = [
                self.scene().addLine(QLineF(item_rect.topLeft(), item_rect.topRight()), pen),
                self.scene().addLine(QLineF(item_rect.topLeft(), item_rect.bottomLeft()), pen),
                self.scene().addLine(QLineF(item_rect.bottomLeft(), item_rect.bottomRight()), pen),
                self.scene().addLine(QLineF(item_rect.bottomRight(), item_rect.topRight()), pen),
                self.scene().addRect(left_top_rect, pen, brush),
                self.scene().addRect(right_top_rect, pen, brush),
                self.scene().addRect(left_bottom_rect, pen, brush),
                self.scene().addRect(right_bottom_rect, pen, brush)
            ]

    def __moving(self, event: QMouseEvent):
        move_to_point = self.get_scene_point(event.position())
        space_rect = self.is_space_available(move_to_point)
        if space_rect:
            if self.selection["item"] is not None:
                dx = space_rect.x() - self.selection["item"].x()
                dy = space_rect.y() - self.selection["item"].y()
                
                if isinstance(self.selection["item"], QGraphicsProxyWidget):
                    points = self.selection["item"].widget().say_goodbye()
                    self.__remove_items(points)
                    self.places.removeFromGroup(self.selection["item"])
                    self.selection["item"].moveBy(dx, dy)
                    self.places.addToGroup(self.selection["item"])
                    self.__check_neighbours(self.selection["item"].widget())

                self.selection["item"] = None
                self.selection["boundries"] = []

                self.scene().removeItem(self.hover_cell)
                self.hover_cell = None
                self.__resize_scene()

    def __remove_items(self, points):
        z_value = self.places.zValue()
        self.places.setZValue(-100)
        for point in points:
            item = self.scene().itemAt(point, QTransform())
            if item:
                self.scene().removeItem(item)
        self.places.setZValue(z_value)

    
    def __check_neighbours(self, new_place: PlaceItem):
        center_point = QPointF(
            new_place.geometry().x() + self.side / 2,
            new_place.geometry().y() + self.side / 2
        )
        
        pen = QPen(Qt.GlobalColor.black, 0.7)
        brush = QBrush(QColor(140, 140, 140))
        for direction, offset in PlaceItem.directions.items():
            check_point = QPointF(
                center_point.x() + offset.x() * self.side,
                center_point.y() + offset.y() * self.side
            )
            item = self.scene().itemAt(check_point, QTransform())
            if isinstance(item, QGraphicsProxyWidget):
                rel_rect = new_place.say_hello(Sides(direction), item.widget())
                bar = self.scene().addRect(rel_rect, pen, brush)
                bar.setZValue(-10)

    def get_scene_point(self, point: QPointF):
        return QPointF(
            point.x() + self.h_scroll.value(),
            point.y() + self.v_scroll.value()
        )

    def is_space_available(self, point: QPointF):
        row = int(point.x() / self.side)
        column = int(point.y() / self.side)
        if point.x() < 0:
            row -= 1
        if point.y() < 0:
            column -= 1
        side_size = self.side - self.margin * 2
        point = QPointF(
            row * self.side + self.margin + side_size / 2, 
            column * self.side + self.margin + side_size / 2
        )
        item = self.scene().itemAt(point, QTransform())
        if self.places is None or item not in self.places.childItems():
            point = QPointF(row * self.side + self.margin, column * self.side + self.margin)
            return QRectF(point, QSizeF(side_size, side_size))
        else:
            return None

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete and self.selection["item"]:
            for item in self.selection["boundries"]:
                self.scene().removeItem(item)
            points = self.selection["item"].widget().say_goodbye()
            self.__remove_items(points)
            self.places.removeFromGroup(self.selection["item"])
            
            self.selection["item"] = None
            self.selection["boundries"] = []
            if self.hover_cell:
                self.scene().removeItem(self.hover_cell)
                self.hover_cell = None
            self.__resize_scene()
        return super().keyPressEvent(event)

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
        if self.places and len(self.places.childItems()) != 0:
            self.__resize_scene()
        self.__refresh_grid()
        return super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.action_selector.grid():
            self.__refresh_grid()
        if self.places and len(self.places.childItems()) != 0:
            ind = self.__resize_scene(0, -(event.angleDelta().y() / 6))
            if ind[1]:
                self.v_scroll.move_scroll_bar(-(event.angleDelta().y() / 6))

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        add_place = self.action_selector.add_place()
        select = self.action_selector.select()
        if add_place:
            self.__add_place_hover(event)
        if (self.places and len(self.places.childItems()) != 0) and not add_place and self.dragging:
            self.__dragging(event)
        if select and self.selection["item"] is not None:
            self.__add_place_hover(event)

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
        if self.action_selector.add_place():
            self.__add_place_press(event)
        if self.action_selector.select():
            self.__selecting(event)
            if self.selection["item"] is not None:
                self.__moving(event)

        self.repaint()
                
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
