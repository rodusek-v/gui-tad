from typing import List
from PyQt6.QtWidgets import QFormLayout, QLabel, QWidget

from view.sidebars.form import Form
from view.fields import ComboBox
from controller import FinishController
from model import Place, ItemNode


class FinishForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar.side_bar_width, sidebar=sidebar)
        self.props_widget = QWidget()
        self.layout().addWidget(self.props_widget)

        self.controller = FinishController(model)
        self.__init_prop_form()

    def __init_prop_form(self):
        layout = QFormLayout()
        self.props_widget.setLayout(layout)

        font = self.font()
        font.setPointSize(13)
        font.setBold(True)

        self.place_combo_box = ComboBox()
        self.place_combo_box.currentIndexChanged.connect(self.__change_place)
        layout.addWidget(QLabel("Position", font=font))
        layout.addWidget(self.place_combo_box)

        self.flag_combo_box = ComboBox()
        self.flag_combo_box.currentIndexChanged.connect(self.__change_flag)
        layout.addWidget(QLabel("Flag", font=font))
        layout.addWidget(self.flag_combo_box)

        self.sidebar.main_controller.item_deletion.connect(self.__reload_flag_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_flag_box)
        self.sidebar.main_controller.item_deletion.connect(self.__reload_position_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_position_box)

        self.__reload_position_box()
        self.__reload_flag_box()

    def __set_current_place(self):
        position = self.controller.get_position()
        self.place_combo_box.setCurrentText(position.name if position else None)

    def __reload_position_box(self, model=None):
        if model is None or isinstance(model, Place):
            self.place_combo_box.currentIndexChanged.disconnect(self.__change_place)
            self.__fill_combo_box(self.place_combo_box, self.sidebar.main_controller.get_places())
            self.__set_current_place()
            self.place_combo_box.currentIndexChanged.connect(self.__change_place)

    def __change_place(self):
        self.controller.set_position(self.place_combo_box.currentData())

    def __set_current_flag(self):
        flag = self.controller.get_flag()
        self.flag_combo_box.setCurrentText(flag.name if flag else None)

    def __reload_flag_box(self):
        self.flag_combo_box.currentIndexChanged.disconnect(self.__change_flag)
        self.__fill_combo_box(self.flag_combo_box, self.sidebar.main_controller.get_flags())
        self.__set_current_flag()
        self.flag_combo_box.currentIndexChanged.connect(self.__change_flag)
    
    def __change_flag(self):
        self.controller.set_flag(self.flag_combo_box.currentData())

    def __fill_combo_box(self, combo_box: ComboBox, items: List[ItemNode]):
        combo_box.clear()
        combo_box.addItem("", None)
        for item in items:
            combo_box.addItem(item.q_icon, item.name, item)

    def disconnect_all_signals(self):
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_flag_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_flag_box)
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_position_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_position_box)