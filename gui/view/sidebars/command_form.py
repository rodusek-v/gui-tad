from typing import List
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QFormLayout, QLabel, QSizePolicy, QWidget

from view.sidebars.form import Form
from view.fields import TextField, TextArea, ComboBox
from controller import CommandController
from model.operation import OperationType
from model import ItemNode


class CommandForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar=sidebar)
        self.props_widget = QWidget()
        self.layout().addWidget(self.props_widget)

        self.controller = CommandController(model)
        layout = QFormLayout()
        self.props_widget.setLayout(layout)

        font = self.font()
        font.setPointSize(13)
        font.setBold(True)
        
        cmd_text_reg = QRegularExpressionValidator(
            QRegularExpression(r"(\w+( \w*)?, *)*(\w+( \w*)?){1}")
        )
        self.cmd_text_txt_box = TextField(", ".join(self.controller.get_cmd_text()))
        self.cmd_text_txt_box.setValidator(cmd_text_reg)
        self.cmd_text_txt_box.editing_done.connect(self.split_cmd_text)
        layout.addWidget(QLabel("Text commands", font=font))
        layout.addWidget(self.cmd_text_txt_box)

        if self.controller.get_type() == OperationType.MESSAGE_OPERATION:
            self.__init_message_operation()

    def __init_message_operation(self):
        layout = self.props_widget.layout()

        font = self.font()
        font.setPointSize(13)
        font.setBold(True)

        msg_txt_box = TextArea(self.controller.get_message())
        msg_txt_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        msg_txt_box.text_modified.connect(self.controller.set_message)
        layout.addWidget(QLabel("Message", font=font))
        layout.addWidget(msg_txt_box)

        self.item_combo_box = ComboBox()
        self.item_combo_box.currentIndexChanged.connect(self.__change_item)
        layout.addWidget(QLabel("Item", font=font))
        layout.addWidget(self.item_combo_box)

        self.place_combo_box = ComboBox()
        self.place_combo_box.currentIndexChanged.connect(self.__change_place)
        layout.addWidget(QLabel("At", font=font))
        layout.addWidget(self.place_combo_box)

        self.sidebar.main_controller.item_deletion.connect(self.__reload_item_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_item_box)
        self.sidebar.main_controller.item_deletion.connect(self.__reload_at_box)
        self.sidebar.main_controller.item_addition.connect(self.__reload_at_box)

        self.__reload_item_box()
        self.__reload_at_box()
        item = self.controller.get_item()
        self.item_combo_box.setCurrentText(item.name if item else None)
        at = self.controller.get_at()
        self.place_combo_box.setCurrentText(at.name if at else None)

    def __reload_item_box(self):
        self.item_combo_box.currentIndexChanged.disconnect(self.__change_item)
        self.__fill_combo_box(self.item_combo_box, self.sidebar.main_controller.get_objects())
        self.item_combo_box.currentIndexChanged.connect(self.__change_item)

    def __reload_at_box(self):
        self.place_combo_box.currentIndexChanged.disconnect(self.__change_place)
        self.__fill_combo_box(self.place_combo_box, self.sidebar.main_controller.get_places())
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

    def __disconnect_message_signals(self):
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_item_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_item_box)
        self.sidebar.main_controller.item_deletion.disconnect(self.__reload_at_box)
        self.sidebar.main_controller.item_addition.disconnect(self.__reload_at_box)

    def split_cmd_text(self):
        split = self.cmd_text_txt_box.text().split(",")
        self.controller.set_cmd_text([txt.strip() for txt in split])

    def disconnect_all_signals(self):
        if self.controller.get_type() == OperationType.MESSAGE_OPERATION:
            self.__disconnect_message_signals()