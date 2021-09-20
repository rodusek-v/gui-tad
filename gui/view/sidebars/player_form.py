from typing import List
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QFormLayout, QGroupBox, QHBoxLayout, QLabel, QListWidget, QWidget

from view.sidebars.form import Form
from view.fields import TextField, ComboBox, ContainsList
from view.worktop import ObjectItem
from controller import PlayerController
from model import Object, Place, ItemNode


class PlayerForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar.side_bar_width, sidebar=sidebar)
        self.props_widget = QWidget()
        self.layout().addWidget(self.props_widget)

        self.controller = PlayerController(model)
        self.__init_prop_form()

    def __init_prop_form(self):
        layout = QFormLayout()
        self.props_widget.setLayout(layout)

        font = self.font()
        font.setPointSize(13)
        font.setBold(True)
        
        id_reg = QRegularExpressionValidator(QRegularExpression(r"[^\d\W]\w*\b"))
        name_txt_box = TextField(self.controller.get_name())
        name_txt_box.setValidator(id_reg)
        name_txt_box.editing_done.connect(self.controller.set_name)
        layout.addWidget(QLabel("Identification name", font=font))
        layout.addWidget(name_txt_box)

        self.place_combo_box = ComboBox()
        self.place_combo_box.currentIndexChanged.connect(self.__change_place)
        layout.addWidget(QLabel("Position", font=font))
        layout.addWidget(self.place_combo_box)

        model_object_group = QGroupBox("Inventory", font=font)
        rest_object_group = QGroupBox("Remaining objects", font=font)
        model_object_group.setLayout(QHBoxLayout())
        rest_object_group.setLayout(QHBoxLayout())
        
        self.model_objects_list = ContainsList(self.controller)

        self.rest_object_list = ContainsList(self.controller, has_model=False)
        self.sidebar.main_controller.object_changes.connect(self.reload_lists)

        self.reload_lists()

        model_object_group.layout().addWidget(self.model_objects_list)
        rest_object_group.layout().addWidget(self.rest_object_list)
        layout.addWidget(model_object_group)
        layout.addWidget(rest_object_group)

        self.sidebar.main_controller.item_deletion.connect(self.__reload_position_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_position_box)

        self.__reload_position_box()

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

    def __fill_combo_box(self, combo_box: ComboBox, items: List[ItemNode]):
        combo_box.clear()
        combo_box.addItem("", None)
        for item in items:
            combo_box.addItem(item.q_icon, item.name, item)

    def reload_lists(self):
        self.__load_list(self.model_objects_list, self.controller.get_items())
        self.__load_list(
            self.rest_object_list, 
            self.sidebar.main_controller.get_objects(),
            self.controller.get_items()
        )

    @staticmethod
    def __load_list(
        list_widget: QListWidget, 
        objects: List['Object'], 
        filters: List['Object'] = None
    ) -> None:
        list_widget.clear()
        filtered = objects
        if filters is not None:
            filtered = filter(lambda x: True if x not in filters else False, objects)

        font = list_widget.font()
        font.setPointSize(13)

        for obj in filtered:
            item = ObjectItem(model=obj)
            item.setText(obj.name)
            item.setFont(font)
            list_widget.addItem(item)

    def disconnect_all_signals(self):
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_position_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_position_box)
        self.sidebar.main_controller.object_changes.disconnect(self.reload_lists)