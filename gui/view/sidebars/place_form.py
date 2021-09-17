from typing import List
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QListWidget, QSizePolicy, QSpinBox, QWidget

from view.sidebars.form import Form
from view.fields import TextField, TextArea, ContainsList
from view.worktop import ObjectItem
from controller import PlaceController
from model import Object


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

    def reload_lists(self):
        self.__load_list(self.model_objects_list, self.controller.get_contains())
        self.__load_list(
            self.rest_object_list, 
            self.sidebar.main_controller.get_objects(),
            self.controller.get_contains()
        )

    def disconnect_all_signals(self):
        self.sidebar.main_controller.object_changes.disconnect(self.reload_lists)

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