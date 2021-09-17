from PyQt6.QtWidgets import QWidget

from view.sidebars.form import Form


class CommandForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar=sidebar)
        self.props_widget = QWidget()
        self.layout().addWidget(self.props_widget)