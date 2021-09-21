from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

from controller import WorldController


class FileMenu(QMenu):

    def __init__(self, parent, controller: WorldController):
        super().__init__("File", parent=parent)

        self.setStyleSheet("""
            QMenu::item {
                padding: 10px;
            }
            QMenu::separator {
                background-color: #707070;
                height: 1px;
            }
        """)

        self.new_world_item = QAction("New item", self)
        self.new_world_item.setShortcut("CTRL+N")

        self.new_item = QAction("New project", self)
        self.new_item.setShortcut("CTRL+SHIFT+N")

        self.open = QAction("Open project", self)
        self.open.setShortcut("CTRL+O")
        self.open.triggered.connect(controller.load)

        self.save = QAction("Save", self)
        self.save.setShortcut("CTRL+S")
        self.save.triggered.connect(controller.save)

        self.exit = QAction("Exit", self)
        self.exit.triggered.connect(self.exit_)

        self.addAction(self.new_item)
        self.addAction(self.new_world_item)
        self.addSeparator()
        self.addAction(self.open)
        self.addAction(self.save)
        self.addSeparator()
        self.addAction(self.exit)

    def exit_(self):
        QtCore.QCoreApplication.instance().quit()