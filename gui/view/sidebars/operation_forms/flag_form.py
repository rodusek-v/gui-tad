from typing import List
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QButtonGroup, QFormLayout, QLabel, QRadioButton, QSizePolicy

from view.fields import TextField, ComboBox, RequirementList
from controller import CommandController
from model import ItemNode


class FlagForm(QObject):
    
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

        self.flag_combo_box = ComboBox()
        self.flag_combo_box.currentIndexChanged.connect(self.__change_flag)
        self.layout.addWidget(QLabel("Flag and value", font=font))
        self.layout.addWidget(self.flag_combo_box)

        indicator_group = QButtonGroup()
        self.true_btn = QRadioButton("true")
        self.false_btn = QRadioButton("false")
        indicator_group.addButton(self.true_btn)
        indicator_group.addButton(self.false_btn)
        self.true_btn.setChecked(self.controller.get_value())
        self.layout.addWidget(self.true_btn)
        self.layout.addWidget(self.false_btn)
        self.true_btn.toggled.connect(self.controller.set_value)

        succ_txt_box = TextField(self.controller.get_success())
        succ_txt_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        succ_txt_box.editing_done.connect(self.controller.set_success)
        self.layout.addWidget(QLabel("Succes message", font=font))
        self.layout.addWidget(succ_txt_box)

        fail_txt_box = TextField(self.controller.get_fail())
        fail_txt_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        fail_txt_box.editing_done.connect(self.controller.set_fail)
        self.layout.addWidget(QLabel("Fail message", font=font))
        self.layout.addWidget(fail_txt_box)

        self.place_combo_box = ComboBox()
        self.place_combo_box.currentIndexChanged.connect(self.__change_place)
        self.layout.addWidget(QLabel("At", font=font))
        self.layout.addWidget(self.place_combo_box)

        self.requirement = RequirementList(controller=self.controller)
        self.requirement.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(QLabel("Requirements", font=font))
        self.layout.addWidget(self.requirement)

        self.sidebar.main_controller.item_deletion.connect(self.__reload_flag_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_flag_box)
        self.sidebar.main_controller.item_deletion.connect(self.__reload_at_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_at_box)
        self.sidebar.main_controller.item_deletion.connect(self.__reload_items_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_items_box)

        self.__reload_flag_box()
        self.__reload_at_box()
        self.__reload_items_box()

    def __set_current_place(self):
        at = self.controller.get_at()
        self.place_combo_box.setCurrentText(at.name if at else None)

    def __set_current_flag(self):
        flag = self.controller.get_flag()
        self.flag_combo_box.setCurrentText(flag.name if flag else None)

    def __reload_flag_box(self):
        self.flag_combo_box.currentIndexChanged.disconnect(self.__change_flag)
        self.__fill_combo_box(self.flag_combo_box, self.sidebar.main_controller.get_flags())
        self.__set_current_flag()
        self.flag_combo_box.currentIndexChanged.connect(self.__change_flag)

    def __reload_items_box(self):
        self.requirement.fill_combo_box(self.sidebar.main_controller.get_objects())

    def __reload_at_box(self):
        self.place_combo_box.currentIndexChanged.disconnect(self.__change_place)
        self.__fill_combo_box(self.place_combo_box, self.sidebar.main_controller.get_places())
        self.__set_current_place()
        self.place_combo_box.currentIndexChanged.connect(self.__change_place)

    def __change_flag(self):
        self.controller.set_flag(self.flag_combo_box.currentData())

    def __change_place(self):
        self.controller.set_at(self.place_combo_box.currentData())

    def __fill_combo_box(self, combo_box: ComboBox, items: List[ItemNode]):
        combo_box.clear()
        combo_box.addItem("", None)
        for item in items:
            combo_box.addItem(item.q_icon, item.name, item)

    def disconnect_all_signals(self):
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_flag_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_flag_box)
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_at_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_at_box)
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_items_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_items_box)