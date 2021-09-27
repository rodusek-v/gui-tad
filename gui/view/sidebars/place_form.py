from typing import List
from PyQt6.QtCore import QRegularExpression, Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent, QRegularExpressionValidator
from PyQt6.QtWidgets import QFormLayout, QGridLayout, QGroupBox, \
    QHBoxLayout, QLabel, QListWidget, QSizePolicy, QSpinBox, QWidget

from view.sidebars.form import Form
from view.fields import TextField, TextArea, ContainsList, ComboBox, BasicList, BasicItem
from view.worktop import ObjectItem
from view.buttons import ToggleButton
from controller import PlaceController
from model import Object
from model.utils import Sides


class PlaceForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar.side_bar_width, sidebar=sidebar)
        self.layout().addWidget(self.tab_widget)
        self.contains_widget = QWidget()
        self.props_widget = QWidget()
        self.tab_widget.addTab(self.props_widget, "Properties")
        self.tab_widget.addTab(self.contains_widget, "Place objects")

        self.controller = PlaceController(model)
        self.__init_prop_form()
        self.__init_contains_form()

    def __init_prop_form(self):
        layout = QFormLayout()
        self.props_widget.setLayout(layout)

        font = self.font()
        font.setPointSize(13)
        font.setBold(True)
        
        name_desc_txt_box = TextField(self.controller.get_descriptive_name())
        name_desc_txt_box.editing_done.connect(self.controller.set_descriptive_name)
        layout.addWidget(QLabel("Descriptive name", font=font))
        layout.addWidget(name_desc_txt_box)

        id_reg = QRegularExpressionValidator(QRegularExpression(r"[^\d\W]\w*\b"))
        name_txt_box = TextField(self.controller.get_name())
        name_txt_box.setValidator(id_reg)
        name_txt_box.editing_done.connect(self.controller.set_name)
        layout.addWidget(QLabel("Identification name", font=font))
        layout.addWidget(name_txt_box)

        name_desc_txt_box.editingFinished.connect(
            lambda: name_txt_box.editingFinished.emit()
        )
        name_desc_txt_box.textChanged.connect(
            lambda x: name_txt_box.setText(x.lower())
        )
        
        desc_txt_box = TextArea(self.controller.get_description())
        desc_txt_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        desc_txt_box.text_modified.connect(self.controller.set_description)
        layout.addWidget(QLabel("Description", font=font))
        layout.addWidget(desc_txt_box)

        blockade = QWidget()
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        blockade.setLayout(grid)
        
        self.flag_combo_box = ComboBox()
        self.flag_combo_box.currentIndexChanged.connect(self.enable_add)
        grid.addWidget(self.flag_combo_box, 0, 0, 1, 4)

        self.direction_box = ComboBox()
        for member in Sides:
            self.direction_box.addItem(member.value, member)
        grid.addWidget(self.direction_box, 0, 4)

        self.turns_spin = QSpinBox()
        self.turns_spin.setStyleSheet("""
            QSpinBox {
                padding: 1px 5px 5px 2px;
                border: 2px solid #545454;
            }
        """)
        self.turns_spin.setMinimum(-1)
        grid.addWidget(self.turns_spin, 1, 0, 1, 2)

        self.add_btn = ToggleButton("Add")
        self.add_btn.setCheckable(False)
        self.add_btn.setStyle("background", "#3d3d3d")
        self.add_btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.add_btn.setEnabled(False)
        self.enable_add()
        grid.addWidget(self.add_btn, 1, 3, 1, 2)

        self.block_list = BlockList()
        self.block_list.delete_pressed.connect(self.__remove_cdms)
        self.block_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        grid.addWidget(self.block_list, 2, 0, 1, 5)

        layout.addWidget(QLabel("Blockades", font=font))
        layout.addWidget(blockade)

        self.sidebar.main_controller.item_deletion.connect(self.__reload_flag_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_flag_box)
        self.add_btn.clicked.connect(self.__add_block)

        self.__reload_flag_box()
        self.fill_list_items()
        
    def __init_contains_form(self):
        layout = QGridLayout()
        self.contains_widget.setLayout(layout)

        font = self.font()
        font.setPointSize(13)
        font.setBold(True)

        model_object_group = QGroupBox("Place objects", font=font)
        rest_object_group = QGroupBox("Remaining objects", font=font)
        model_object_group.setLayout(QHBoxLayout())
        rest_object_group.setLayout(QHBoxLayout())
        
        self.model_objects_list = ContainsList(self.controller)

        self.rest_object_list = ContainsList(self.controller, has_model=False)
        self.sidebar.main_controller.object_changes.connect(self.reload_lists)

        self.reload_lists()

        model_object_group.layout().addWidget(self.model_objects_list)
        rest_object_group.layout().addWidget(self.rest_object_list)
        layout.addWidget(model_object_group, 0, 0)
        layout.addWidget(rest_object_group, 1, 0)

    def __add_block(self):
        flag = self.flag_combo_box.currentData()
        direction = self.direction_box.currentData()
        turns = self.turns_spin.value()

        self.controller.add_blockade(flag, direction, turns)
        self.flag_combo_box.setCurrentText("")
        self.fill_list_items()

    def __remove_cdms(self):
        items = self.block_list.selectedItems()
        if len(items) != 0:
            for item in items:
                self.controller.remove_blockade(item.item_data)
            self.fill_list_items()

    def __reload_flag_box(self):
        self.flag_combo_box.clear()
        self.flag_combo_box.addItem("", None)
        items = self.sidebar.main_controller.get_flags()
        for item in items:
            self.flag_combo_box.addItem(item.q_icon, item.name, item)

    def enable_add(self):
        data = self.flag_combo_box.currentData()
        if data is None:
            self.add_btn.setStyle("background", "#878787")
            self.add_btn.setEnabled(False)
        else:
            self.add_btn.setStyle("background", "#3d3d3d")
            self.add_btn.setEnabled(True)

    def fill_list_items(self):
        self.block_list.clear()
        items = self.controller.get_blockade()
        for item in items:
            list_item = BasicItem(item)
            text = f"flag = {item.flag.name}, direction = {item.direction.value}"
            text += "" if item.turns == -1 else f", allowed_turns = {item.turns}"
            list_item.setText(text)
            self.block_list.addItem(list_item)

    def reload_lists(self):
        self.__load_list(self.model_objects_list, self.controller.get_contains())
        self.__load_list(
            self.rest_object_list, 
            self.sidebar.main_controller.get_objects(),
            self.controller.get_contains()
        )

    def disconnect_all_signals(self):
        self.sidebar.main_controller.object_changes.disconnect(self.reload_lists)
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_flag_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_flag_box)

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


class BlockList(BasicList):

    delete_pressed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            self.delete_pressed.emit()
        super().keyPressEvent(event)