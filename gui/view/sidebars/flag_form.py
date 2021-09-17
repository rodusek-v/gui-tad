from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QFormLayout, QLabel, QWidget

from view.sidebars.form import Form
from view.fields import TextField, CheckBox, ActionWidget
from controller import FlagController


class FlagForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar=sidebar)
        self.props_widget = QWidget()
        self.layout().addWidget(self.props_widget)

        self.controller = FlagController(model)
        self.__init_prop_form()

    def __init_prop_form(self):
        layout = QFormLayout()
        self.props_widget.setLayout(layout)

        font = self.font()
        font.setPointSize(13)
        font.setBold(True)

        id_reg = QRegularExpressionValidator(QRegularExpression(r"[^\d\W]\w*\b"))
        name_txt_box = TextField(self.controller.get_name())
        name_txt_box.setValidator(id_reg)
        name_txt_box.editing_done.connect(self.controller.set_name)
        layout.addWidget(QLabel("Identification name", font=font))
        layout.addWidget(name_txt_box)

        activated_chkbox = CheckBox()
        activated_chkbox.setChecked(self.controller.get_activated())
        activated_chkbox.stateChanged.connect(self.pass_to_activated)
        layout.addWidget(QLabel("Activated", font=font))
        layout.addWidget(activated_chkbox)

        self.action_on_true_list = ActionWidget(controller=self.controller, type=True)
        layout.addWidget(QLabel("Action on true", font=font))
        layout.addWidget(self.action_on_true_list)

        self.action_on_false_list = ActionWidget(controller=self.controller, type=False)
        layout.addWidget(QLabel("Action on false", font=font))
        layout.addWidget(self.action_on_false_list)

        self.refresh_list()
        name_txt_box.editing_done.connect(self.refresh_list)

    def refresh_list(self):
        flags = self.sidebar.main_controller.get_flags()
        self.action_on_false_list.fill_combo_box(flags)
        self.action_on_false_list.fill_list_items()
        self.action_on_true_list.fill_combo_box(flags)
        self.action_on_true_list.fill_list_items()


    def pass_to_activated(self, value):
        self.controller.set_activated(bool(value))