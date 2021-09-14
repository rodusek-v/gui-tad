
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from view.sidebars.form import Form


class ObjectForm(Form):
    
    def __init__(self, model, parent=None) -> None:
        super().__init__(model, parent=parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.tab_widget)
        self.contains_widget = QWidget()
        self.props_widget = QWidget()
        self.tab_widget.addTab(self.props_widget, "Properties")
        self.tab_widget.addTab(self.contains_widget, "Object content")
