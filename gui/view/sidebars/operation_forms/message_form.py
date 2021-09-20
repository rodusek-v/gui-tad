from typing import List
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFormLayout, QLabel, QSizePolicy

from view.fields import TextArea, ComboBox
from controller import CommandController
from model import ItemNode, Object, Place


class MessageForm(QObject):
    
    def __init__(self, controller: CommandController, sidebar, layout: QFormLayout, font: QFont) -> None:
        super().__init__()
        self.controller = controller
        self.sidebar = sidebar
        self.layout = layout
        self.font = font
        self._init_operation()

    def _init_operation(self):
        font = self.font
        font.setPointSize(13)
        font.setBold(True)

        msg_txt_box = TextArea(self.controller.get_message())
        msg_txt_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        msg_txt_box.text_modified.connect(self.controller.set_message)
        self.layout.addWidget(QLabel("Message", font=font))
        self.layout.addWidget(msg_txt_box)

        self.item_combo_box = ComboBox()
        self.item_combo_box.currentIndexChanged.connect(self.__change_item)
        self.layout.addWidget(QLabel("Item", font=font))
        self.layout.addWidget(self.item_combo_box)

        self.place_combo_box = ComboBox()
        self.place_combo_box.currentIndexChanged.connect(self.__change_place)
        self.layout.addWidget(QLabel("At", font=font))
        self.layout.addWidget(self.place_combo_box)

        self.sidebar.main_controller.item_deletion.connect(self.__reload_item_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_item_box)
        self.sidebar.main_controller.item_deletion.connect(self.__reload_at_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_at_box)

        self.__reload_item_box()
        self.__reload_at_box()

    def __set_currect_item(self):
        item = self.controller.get_item()
        print(item)
        self.item_combo_box.setCurrentText(item.name if item else None)

    def __set_current_place(self):
        at = self.controller.get_at()
        self.place_combo_box.setCurrentText(at.name if at else None)

    def __reload_item_box(self, model=None):
        if model is None or isinstance(model, Object):
            self.item_combo_box.currentIndexChanged.disconnect(self.__change_item)
            self.__fill_combo_box(self.item_combo_box, self.sidebar.main_controller.get_objects())
            self.__set_currect_item()
            self.item_combo_box.currentIndexChanged.connect(self.__change_item)

    def __reload_at_box(self, model=None):
        if model is None or isinstance(model, Place):
            self.place_combo_box.currentIndexChanged.disconnect(self.__change_place)
            self.__fill_combo_box(self.place_combo_box, self.sidebar.main_controller.get_places())
            self.__set_current_place()
            self.place_combo_box.currentIndexChanged.connect(self.__change_place)

    def __change_item(self):
        self.controller.set_item(self.item_combo_box.currentData())

    def __change_place(self):
        self.controller.set_at(self.place_combo_box.currentData())

    def __fill_combo_box(self, combo_box: ComboBox, items: List[ItemNode]):
        combo_box.clear()
        combo_box.addItem("", None)
        for item in items:
            combo_box.addItem(item.q_icon, item.name, item)

    def disconnect_all_signals(self):
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_item_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_item_box)
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_at_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_at_box)