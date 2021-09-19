from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QFormLayout, QLabel, QSizePolicy

from view.sidebars.operation_forms.flag_form import FlagForm
from view.fields import ComboBox, BasicList, BasicItem
from view.buttons import ToggleButton
from controller import CommandController
from model.operation import CDMType
from model import Object

class CDMForm(FlagForm):

    def __init__(self, controller: CommandController, sidebar, layout: QFormLayout, font: QFont) -> None:
        super().__init__(controller, sidebar, layout, font)
        self.container_objects = True 
        self.__reload_item_box()
        self.enable_add()
        self.fill_list_items()
        
    def _init_operation(self):
        super()._init_operation()

        font = self.font
        font.setPointSize(13)
        font.setBold(True)
        
        self.type_combo_box = ComboBox()
        self.layout.addWidget(QLabel("CDM list", font=font))
        self.layout.addWidget(self.type_combo_box)
        
        for type in CDMType:
            self.type_combo_box.addItem(type.value, type)

        self.item_combo_box = ComboBox()
        self.layout.addWidget(self.item_combo_box)

        self.cdm_btn = ToggleButton("Add")
        self.cdm_btn.setCheckable(False)
        self.cdm_btn.setStyle("background", "#3d3d3d")
        self.cdm_btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.cdm_btn.setEnabled(False)
        self.layout.addWidget(self.cdm_btn)

        self.cdm_list = BasicList()
        self.cdm_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(self.cdm_list)

        self.sidebar.main_controller.item_deletion.connect(self.__reload_item_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_item_box)
        self.sidebar.main_controller.object_changes.connect(self.__reload_item_box)
        
        self.type_combo_box.currentIndexChanged.connect(self.__select_type)
        self.item_combo_box.currentIndexChanged.connect(self.enable_add)
        self.cdm_btn.clicked.connect(self.__add_prop)

    def __add_prop(self):
        type = self.type_combo_box.currentData()
        item = self.item_combo_box.currentData()

        self.controller.add_cdm_prop(type, item)
        self.item_combo_box.setCurrentText("")
        self.fill_list_items()

    def __select_type(self):
        self.container_objects = self.type_combo_box.currentText() == CDMType.CREATE.value
        self.__reload_item_box()

    def __reload_item_box(self, model=None):
        if model is None or isinstance(model, Object):
            self.item_combo_box.clear()
            self.item_combo_box.addItem("", None)
            items = self.sidebar.main_controller.get_objects()
            items = filter(lambda x: bool(x.container) != self.container_objects, items)
            for item in items:
                self.item_combo_box.addItem(item.q_icon, item.name, item)
    
    def fill_list_items(self):
        self.cdm_list.clear()
        items = self.controller.get_cdm_props()
        for item in items:
            list_item = BasicItem(item)
            list_item.setText(f"{item.type.value}: {item.item.name}")
            self.cdm_list.addItem(list_item)

    def enable_add(self):
        data = self.item_combo_box.currentData()
        if data is None:
            self.cdm_btn.setStyle("background", "#878787")
            self.cdm_btn.setEnabled(False)
        else:
            self.cdm_btn.setStyle("background", "#3d3d3d")
            self.cdm_btn.setEnabled(True)

    def disconnect_all_signals(self):
        super().disconnect_all_signals()
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_item_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_item_box)
        self.sidebar.main_controller.object_changes.disconnect(self.__reload_item_box)


class CDMList(BasicList):

    def __init__(self, parent: 'CDMForm') -> None:
        super().__init__()
        self.parent_ = parent

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            items = self.selectedItems()
            if len(items) != 0:
                for item in items:
                    self.parent_.controller.remove_cdm_prop(item.item_data)
                self.parent_.fill_list_items()
        super().keyPressEvent(event)