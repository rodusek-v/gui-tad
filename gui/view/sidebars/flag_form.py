from PyQt6.QtWidgets import QHBoxLayout

from view.sidebars.form import Form


class FlagForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar=sidebar)
        layout = QHBoxLayout()
        self.setLayout(layout)