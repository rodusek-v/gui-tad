from PyQt6.QtWidgets import QTreeView

class WorldTreeView(QTreeView):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setStyleSheet("border: none; background-color: transparent; color: #bfbfbf;")