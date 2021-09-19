from typing import List
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QColor, QRegularExpressionValidator
from PyQt6.QtWidgets import QFormLayout, QLabel, QScrollArea, QWidget

from view.sidebars.operation_forms.message_form import MessageForm
from view.sidebars.operation_forms.flag_form import FlagForm
from view.sidebars.operation_forms.cdm_form import CDMForm
from view.sidebars.operation_forms.relocation_form import RelocationForm
from view.sidebars.form import Form
from view.worktop import GridScrollBar
from view.fields import TextField
from controller import CommandController
from model.operation import OperationType


class CommandForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar=sidebar)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setVerticalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))
        scroll_area.setHorizontalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))
        self.props_widget = QWidget()
        scroll_area.setWidget(self.props_widget)
        self.layout().addWidget(scroll_area)

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
            self.current_form = MessageForm(self.controller, self.sidebar, layout, font)
        elif self.controller.get_type() == OperationType.FLAG_OPERATION:
            self.current_form = FlagForm(self.controller, self.sidebar, layout, font)
        elif self.controller.get_type() == OperationType.CDM_OPERATION:
            self.current_form = CDMForm(self.controller, self.sidebar, layout, font)
        elif self.controller.get_type() == OperationType.RELOCATION_OPERATION:
            self.current_form = RelocationForm(self.controller, self.sidebar, layout, font)

    def split_cmd_text(self):
        split = self.cmd_text_txt_box.text().split(",")
        self.controller.set_cmd_text([txt.strip() for txt in split])

    def disconnect_all_signals(self):
        self.current_form.disconnect_all_signals()