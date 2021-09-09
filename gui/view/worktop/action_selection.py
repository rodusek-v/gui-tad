
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QCursor, QPixmap


class ActionSelector(QObject):

    cursor_changed = pyqtSignal()
    grid_changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.grid_turn_on = False
        self.cursors = {
            "add_place": QCursor(QPixmap('icons/cursors/box.png')),
            "add_object": QCursor(QPixmap('icons/cursors/object.png')),
            "drag": QCursor(QPixmap('icons/cursors/hand.png')),
            "select": QCursor(QPixmap('icons/cursors/arrow.png')),
            "grab": QCursor(QPixmap('icons/cursors/grab.png'))
        }

        self.interaction_group = {
            "add_place": False,
            "add_object": False,
            "drag": False,
            "select": False
        }

        self.current_cursor = None

    def __set_interaction(self, select):
        for key in self.interaction_group:
            if select != key:
                self.interaction_group[key] = False
        
        self.interaction_group[select] = True

    def get_cursor(self, name):
        return self.cursors[name]

    def activate(self, key):
        self.__set_interaction(key)
        self.current_cursor = self.cursors[key]
        self.cursor_changed.emit()

    def add_place(self):
        return self.interaction_group['add_place']    

    def add_object(self):
        return self.interaction_group['add_object']   
    
    def toggle_grid(self):
        self.grid_turn_on = not self.grid_turn_on
        self.grid_changed.emit()

    def grid(self):
        return self.grid_turn_on

    def drag(self):
        return self.interaction_group['drag']

    def select(self):
        return self.interaction_group['select']

    def get_current_cursor(self):
        return self.current_cursor
    