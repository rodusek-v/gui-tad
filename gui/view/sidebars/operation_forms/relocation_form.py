from typing import List
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFormLayout, QLabel, QSizePolicy

from view.fields import ComboBox, TextField, CheckBox, RequirementList
from controller import CommandController
from model import ItemNode


class RelocationForm(QObject):
    
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

        self.from_combo_box = ComboBox()
        self.from_combo_box.currentIndexChanged.connect(self.__change_from)
        self.layout.addWidget(QLabel("From", font=font))
        self.layout.addWidget(self.from_combo_box)

        self.to_combo_box = ComboBox()
        self.to_combo_box.currentIndexChanged.connect(self.__change_to)
        self.layout.addWidget(QLabel("To", font=font))
        self.layout.addWidget(self.to_combo_box)

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

        pickable_chkbox = CheckBox()
        pickable_chkbox.setChecked(self.controller.get_can_die())
        pickable_chkbox.stateChanged.connect(self.pass_to_can_die)
        self.layout.addWidget(QLabel("Can die", font=font))
        self.layout.addWidget(pickable_chkbox)

        self.requirement = RequirementList(controller=self.controller)
        self.requirement.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(QLabel("Requirements", font=font))
        self.layout.addWidget(self.requirement)

        self.sidebar.main_controller.item_deletion.connect(self.__reload_from_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_from_box)
        self.sidebar.main_controller.item_deletion.connect(self.__reload_to_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_to_box)
        self.sidebar.main_controller.item_deletion.connect(self.__reload_items_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_items_box)

        self.__reload_from_box()
        self.__reload_to_box()
        self.__reload_items_box()

    def __set_current_from(self):
        from_ = self.controller.get_from()
        self.from_combo_box.setCurrentText(from_.name if from_ else None)

    def __set_current_to(self):
        to = self.controller.get_to()
        self.to_combo_box.setCurrentText(to.name if to else None)

    def __reload_items_box(self):
        self.requirement.fill_combo_box(self.sidebar.main_controller.get_objects())

    def __reload_from_box(self):
        self.from_combo_box.currentIndexChanged.disconnect(self.__change_from)
        self.__fill_combo_box(self.from_combo_box, self.sidebar.main_controller.get_places())
        self.__set_current_from()
        self.from_combo_box.currentIndexChanged.connect(self.__change_from)

    def __reload_to_box(self):
        self.to_combo_box.currentIndexChanged.disconnect(self.__change_to)
        self.__fill_combo_box(self.to_combo_box, self.sidebar.main_controller.get_places())
        self.__set_current_to()
        self.to_combo_box.currentIndexChanged.connect(self.__change_to)

    def __change_from(self):
        self.controller.set_from(self.from_combo_box.currentData())

    def __change_to(self):
        self.controller.set_to(self.to_combo_box.currentData())

    def __fill_combo_box(self, combo_box: ComboBox, items: List[ItemNode]):
        combo_box.clear()
        combo_box.addItem("", None)
        for item in items:
            combo_box.addItem(item.q_icon, item.name, item)

    def pass_to_can_die(self, value):
        self.controller.set_can_die(bool(value))

    def disconnect_all_signals(self):
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_from_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_from_box)
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_items_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_items_box)