from typing import List
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from view.fields.equal_list import EqualList
from view.fields.basic_list import BasicItem
from controller import FlagController, CommandController
from model import Flag, Object


class ActionList(EqualList):

    def __init__(self, controller: FlagController, type: bool, parent=None) -> None:
        super().__init__(parent=parent)
        self.controller = controller
        self.type = type
        self.fill_list_items()
        
    def _init_input(self):
        super()._init_input()
        self.add_btn.clicked.connect(self.add_dependency)

    def add_dependency(self):
        flag = self.combo_box.currentData()
        value = self.btn1.isChecked()

        if self.type:
            self.controller.add_true_dependency(flag, value)
        else:
            self.controller.add_false_dependency(flag, value)
        self.combo_box.setCurrentText("")
        self.btn1.setChecked(True)
        self.fill_list_items()

    def fill_list_items(self):
        self.basic_list.clear()
        items = self.controller.get_action(self.type).get_dependencies()
        for item in items:
            list_item = BasicItem(item)
            list_item.setText(f"{item.flag.name} == {str(item.value).lower()}")
            self.basic_list.addItem(list_item)

    def fill_combo_box(self, items: List['Flag']):
        self.combo_box.clear()
        self.combo_box.addItem("", None)
        for item in items:
            self.combo_box.addItem(item.q_icon, item.name, item)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            items = self.basic_list.selectedItems()
            if len(items) != 0:
                for item in items:
                    if self.type:
                        self.controller.remove_true_dependency(item.item_data)
                    else:
                        self.controller.remove_false_dependency(item.item_data)
                self.fill_list_items()
        super().keyPressEvent(event)
    

class RequirementList(EqualList):

    def __init__(self, controller: CommandController, parent=None) -> None:
        super().__init__(parent=parent)
        self.controller = controller
        self.fill_list_items()
        
    def _init_input(self):
        super()._init_input()
        self.add_btn.clicked.connect(self.add_requirement)
        self.set_buttons_text("present", "carrying")

    def add_requirement(self):
        item = self.combo_box.currentData()
        value = self.btn1.isChecked()

        if value:
            self.controller.add_present_requirement(item)
        else:
            self.controller.add_carry_requirement(item)
        self.combo_box.setCurrentText("")
        self.btn1.setChecked(True)
        self.fill_list_items()

    def fill_list_items(self):
        self.basic_list.clear()
        items = self.controller.get_carry_requirements()
        for item in items:
            list_item = BasicItem(item)
            list_item.setText(f"is carrying {item.name}")
            self.basic_list.addItem(list_item)
        items = self.controller.get_present_requirements()
        for item in items:
            list_item = BasicItem(item)
            list_item.setText(f"is present {item.name}")
            self.basic_list.addItem(list_item)

    def fill_combo_box(self, items: List['Object']):
        self.combo_box.clear()
        self.combo_box.addItem("", None)
        for item in items:
            self.combo_box.addItem(item.q_icon, item.name, item)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            items = self.basic_list.selectedItems()
            if len(items) != 0:
                for item in items:
                    if "carrying" in item.text():
                        self.controller.remove_carry_requirement(item.item_data)
                    else:
                        self.controller.remove_present_requirement(item.item_data)
                self.fill_list_items()
        super().keyPressEvent(event)
    