from typing import List
from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QKeyEvent, QRegularExpressionValidator
from PyQt6.QtWidgets import QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QListWidget, QSizePolicy, QSpinBox, QWidget

from view.sidebars.form import Form
from controller import FinishController


class FinishForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar.side_bar_width, sidebar=sidebar)
        self.props_widget = QWidget()

        self.controller = FinishController(model)