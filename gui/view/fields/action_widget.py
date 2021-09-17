from typing import List
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QButtonGroup, QGridLayout, QLabel, QRadioButton, QSizePolicy, QWidget

from view.fields.combo_box import ComboBox
from view.fields.text_field import TextField
from view.fields.basic_list import BasicList, BasicItem
from view.buttons import ToggleButton
from controller import FlagController
from model import Flag


class ActionWidget(QWidget):

    def __init__(self, controller: FlagController, type: bool, parent=None) -> None:
        super().__init__(parent=parent)
        self.controller = controller
        self.type = type
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)
        self.__init_input()
        
    def __init_input(self):
        font = self.font()
        font.setPointSize(10)
        self.grid.addWidget(QLabel("Message", font=font), 0, 0, 1, 2)

        msg = self.controller.get_true_message() if self.type else self.controller.get_false_message()
        set_message = self.controller.set_true_message if self.type else self.controller.set_false_message
        msg_txt_bot = TextField(msg)
        msg_txt_bot.editing_done.connect(set_message)
        self.grid.addWidget(msg_txt_bot, 1, 0, 1, 2)

        self.flag_combo_box = ComboBox()
        self.flag_combo_box.currentIndexChanged.connect(self.enable_add)
        self.grid.addWidget(self.flag_combo_box, 2, 0, 1, 2)

        indicator_group = QButtonGroup()
        self.true_btn = QRadioButton("true")
        self.true_btn.clicked.connect(self.enable_add)
        self.false_btn = QRadioButton("false")
        self.false_btn.clicked.connect(self.enable_add)
        indicator_group.addButton(self.true_btn)
        indicator_group.addButton(self.false_btn)
        self.grid.addWidget(self.true_btn, 3, 0)
        self.grid.addWidget(self.false_btn, 4, 0)

        self.add_btn = ToggleButton("Add")
        self.add_btn.setCheckable(False)
        self.add_btn.clicked.connect(self.add_dependency)
        self.add_btn.setStyle("background", "#3d3d3d")
        self.add_btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.add_btn.setEnabled(False)
        self.grid.addWidget(self.add_btn, 3, 1, 2, 1)

        self.dependencies = BasicList()
        self.fill_list_items()
        self.grid.addWidget(self.dependencies, 5, 0, 1, 2)

    def set_buttons_text(self, text1, text2):
        self.true_btn.setText(text1)
        self.false_btn.setText(text2)

    def enable_add(self):
        flag = self.flag_combo_box.currentData()
        if (not self.true_btn.isChecked() and not self.false_btn.isChecked()) or flag is None:
            self.add_btn.setStyle("background", "#878787")
            self.add_btn.setEnabled(False)
        else:
            self.add_btn.setStyle("background", "#3d3d3d")
            self.add_btn.setEnabled(True)

    def add_dependency(self):
        flag = self.flag_combo_box.currentData()
        value = self.true_btn.isChecked()

        if self.type:
            self.controller.add_true_dependency(flag, value)
        else:
            self.controller.add_false_dependency(flag, value)
        self.flag_combo_box.setCurrentText("")
        self.true_btn.setChecked(True)
        self.fill_list_items()

    def fill_list_items(self):
        self.dependencies.clear()
        items = self.controller.get_action(self.type).get_dependecines()
        for item in items:
            self.dependencies.addItem(BasicItem(item))

    def fill_combo_box(self, items: List['Flag']):
        self.flag_combo_box.clear()
        self.flag_combo_box.addItem("", None)
        for item in items:
            self.flag_combo_box.addItem(item.name, item)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            items = self.dependencies.selectedItems()
            if len(items) != 0:
                for item in items:
                    if self.type:
                        self.controller.remove_true_dependency(item.item_data)
                    else:
                        self.controller.remove_false_dependency(item.item_data)
                self.fill_list_items()
        super().keyPressEvent(event)
    