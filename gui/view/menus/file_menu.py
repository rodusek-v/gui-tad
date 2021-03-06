from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu

from controller import WorldController
from view.windows.creating_dialog import CreatingDialog
from view.windows.starting_dialog import StartingDialog
from view.windows.message_box import MessageBox
from constants import THIS_FOLDER


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
        self.controller = controller
        self.new_world_item = QMenu("New item", self)

        object_png = "/".join([THIS_FOLDER, "icons/object.png"])
        self.new_object_item = QAction(QIcon(object_png), "New object", self)
        self.new_object_item.setShortcut("CTRL+SHIFT+O")

        flag_png = "/".join([THIS_FOLDER, "icons/flag.png"])
        self.new_flag_item = QAction(QIcon(flag_png), "New flag", self)
        self.new_flag_item.setShortcut("CTRL+SHIFT+F")

        command_png = "/".join([THIS_FOLDER, "icons/command.png"])
        self.new_command_item = QAction(QIcon(command_png), "New command", self)
        self.new_command_item.setShortcut("CTRL+SHIFT+C")

        self.new_world_item.addAction(self.new_object_item)
        self.new_world_item.addAction(self.new_flag_item)
        self.new_world_item.addAction(self.new_command_item)

        self.new_project = QAction("New project", self)
        self.new_project.setShortcut("CTRL+SHIFT+N")
        self.new_project.triggered.connect(self.create)

        self.open = QAction("Open project", self)
        self.open.setShortcut("CTRL+O")
        self.open.triggered.connect(self.load)

        self.save = QAction("Save", self)
        self.save.setShortcut("CTRL+S")
        self.save.triggered.connect(self.save_func)

        self.exit = QAction("Exit", self)
        self.exit.triggered.connect(self.exit_)

        self.addAction(self.new_project)
        self.addMenu(self.new_world_item)
        self.addSeparator()
        self.addAction(self.open)
        self.addAction(self.save)
        self.addSeparator()
        self.addAction(self.exit)

    def load(self):
        dlg = StartingDialog(self.parent())
        dlg.accepted.connect(self.restart)
        dlg.exec()

    def create(self):
        dlg = CreatingDialog(self.parent())
        dlg.accepted.connect(self.restart)
        dlg.exec()

    def save_func(self):
        try:
            self.controller.save()
            dlg = MessageBox(self.parent(), "")
            dlg.setIcon(MessageBox.Icon.Information)
            dlg.setText("World model is saved successfully.")
            dlg.exec()
        except Exception as ex:
            dlg = MessageBox(self.parent(), "")
            ex_msg = str(ex)
            error_msg = f"Save successful but has some warnings:\n{ex_msg}" 
            dlg.setText(error_msg)
            dlg.exec()

    def restart(self):
        QApplication.exit(self.parent().EXIT_CODE_REBOOT)

    def exit_(self):
        QApplication.quit()