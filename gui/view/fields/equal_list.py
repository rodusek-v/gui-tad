from PyQt6.QtWidgets import QButtonGroup, QGridLayout, QRadioButton, QSizePolicy, QWidget

from view.fields.combo_box import ComboBox
from view.fields.basic_list import BasicList
from view.buttons import ToggleButton


class EqualList(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)
        self._init_input()
        
    def _init_input(self):
        font = self.font()
        font.setPointSize(10)

        self.combo_box = ComboBox()
        self.combo_box.currentIndexChanged.connect(self.enable_add)
        self.grid.addWidget(self.combo_box, 0, 0, 1, 2)

        indicator_group = QButtonGroup()
        self.btn1 = QRadioButton("true")
        self.btn1.clicked.connect(self.enable_add)
        self.btn2 = QRadioButton("false")
        self.btn2.clicked.connect(self.enable_add)
        indicator_group.addButton(self.btn1)
        indicator_group.addButton(self.btn2)
        self.grid.addWidget(self.btn1, 1, 0)
        self.grid.addWidget(self.btn2, 2, 0)

        self.add_btn = ToggleButton("Add")
        self.add_btn.setCheckable(False)
        self.add_btn.setStyle("background", "#3d3d3d")
        self.add_btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.add_btn.setEnabled(False)
        self.enable_add()
        self.grid.addWidget(self.add_btn, 1, 1, 2, 1)

        self.basic_list = BasicList()
        self.grid.addWidget(self.basic_list, 3, 0, 1, 2)

    def set_buttons_text(self, text1, text2):
        self.btn1.setText(text1)
        self.btn2.setText(text2)

    def enable_add(self):
        data = self.combo_box.currentData()
        if (not self.btn1.isChecked() and not self.btn2.isChecked()) or data is None:
            self.add_btn.setStyle("background", "#878787")
            self.add_btn.setEnabled(False)
        else:
            self.add_btn.setStyle("background", "#3d3d3d")
            self.add_btn.setEnabled(True)
