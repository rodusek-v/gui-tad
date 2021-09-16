from typing import List
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QListWidget, QSizePolicy, QWidget

from view.sidebars.form import Form
from view.sidebars.contains_list import ContainsList
from view.fields import TextField, TextArea, CheckBox, ComboBox
from view.worktop import ObjectItem
from controller import ObjectController
from model import Container, Object


class ObjectForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar=sidebar)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.tab_widget)
        self.contains_widget = QWidget()
        self.props_widget = QWidget()
        self.tab_widget.addTab(self.props_widget, "Properties")
        self.tab_widget.addTab(self.contains_widget, "Object content")

        self.controller = ObjectController(model)
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

        pickable_chkbox = CheckBox()
        pickable_chkbox.setChecked(self.controller.get_pickable())
        pickable_chkbox.stateChanged.connect(lambda x: self.controller.set_pickable(bool(x)))
        layout.addWidget(QLabel("Pickable", font=font))
        layout.addWidget(pickable_chkbox)

        self.container_combo_box = ComboBox()
        self.container_combo_box.currentIndexChanged.connect(self.__change_container)
        self.__reload_combo_box()
        layout.addWidget(QLabel("Container", font=font))
        layout.addWidget(self.container_combo_box)
        self.controller.model.container_chaged.connect(self.__reload_combo_box)
        self.sidebar.main_controller.item_deletion.connect(self.__reload_combo_box)

    def __init_contains_form(self):
        layout = QGridLayout()
        self.contains_widget.setLayout(layout)

        font = self.font()
        font.setPointSize(13)
        font.setBold(True)

        model_object_group = QGroupBox("Object content", font=font)
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

    def __change_container(self):
        self.controller.set_container(self.container_combo_box.currentData())

    def __reload_combo_box(self):
        self.container_combo_box.currentIndexChanged.disconnect(self.__change_container)
        self.__fill_combo_box(self.sidebar.main_controller.get_containers(), self.controller.model)
        self.__set_current_container(self.controller.get_container())
        self.container_combo_box.currentIndexChanged.connect(self.__change_container)

    def __fill_combo_box(self, containers: List['Container'], object: Object):
        self.container_combo_box.clear()
        self.container_combo_box.addItem("", None)
        if object in containers:
            containers.remove(object)
        for container in containers:
            self.container_combo_box.addItem(container.name, container)

    def __set_current_container(self, container: Container):
        self.container_combo_box.setCurrentText(container.name if container else None)

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
        self.controller.model.container_chaged.disconnect(self.__reload_combo_box)
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_combo_box)
        self.sidebar.main_controller.object_changes.disconnect(self.reload_lists)

    def reload_lists(self):
        filter_list = self.controller.get_contains()[:]
        filter_list.append(self.controller.model)
        self.__load_list(self.model_objects_list, self.controller.get_contains())
        self.__load_list(
            self.rest_object_list, 
            self.sidebar.main_controller.get_objects(),
            filter_list
        )

    