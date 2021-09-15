from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QSpinBox, QWidget

from view.sidebars.form import Form
from view.fields import TextField, TextArea
from controller import PlaceController


class PlaceForm(Form):
    
    def __init__(self, model, parent=None) -> None:
        super().__init__(model, parent=parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.tab_widget)
        self.contains_widget = QWidget()
        self.props_widget = QWidget()
        self.tab_widget.addTab(self.props_widget, "Properties")
        self.tab_widget.addTab(self.contains_widget, "Place objects")

        self.controller = PlaceController(model)
        self.__init_prop_form()

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

        name_txt_box = TextField(self.controller.get_name())
        name_txt_box.editing_done.connect(self.controller.set_name)
        layout.addWidget(QLabel("Identification name", font=font))
        layout.addWidget(name_txt_box)

        name_desc_txt_box.editingFinished.connect(
            lambda: name_txt_box.editingFinished.emit()
        )
        name_desc_txt_box.textChanged.connect(
            lambda x: name_txt_box.setText(x.lower().replace(" ", "_"))
        )
        
        desc_txt_box = TextArea(self.controller.get_description())
        desc_txt_box.text_modified.connect(self.controller.set_description)
        layout.addWidget(QLabel("Description", font=font))
        layout.addWidget(desc_txt_box)

        turns_in = TextField(self.controller.get_turns_in())
        turns_in.setValidator(QIntValidator(bottom=0))
        turns_in.editing_done.connect(self.controller.set_turns_in)
        layout.addWidget(QLabel("Turns allowed", font=font))
        layout.addWidget(turns_in)
        
    