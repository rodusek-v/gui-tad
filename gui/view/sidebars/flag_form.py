from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QColor, QRegularExpressionValidator
from PyQt6.QtWidgets import QFormLayout, QLabel, QScrollArea, QSizePolicy, QWidget

from view.sidebars.form import Form
from view.fields import TextField, CheckBox, ActionList
from view.worktop import GridScrollBar
from controller import FlagController


class FlagForm(Form):
    
    def __init__(self, model, sidebar) -> None:
        super().__init__(model, sidebar=sidebar)
        self.props_widget = QWidget()
        self.layout().addWidget(self.props_widget)

        self.controller = FlagController(model)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setVerticalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))
        scroll_area.setHorizontalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))
        scroll_area.setWidget(self.props_widget)
        self.layout().addWidget(scroll_area)
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

        msg_txt_bot = TextField(self.controller.get_true_message())
        msg_txt_bot.editing_done.connect(self.controller.set_true_message)
        layout.addWidget(QLabel("Message", font=font))
        layout.addWidget(msg_txt_bot)

        self.action_on_true_list = ActionList(controller=self.controller, type=True)
        self.action_on_true_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(QLabel("Action on true", font=font))
        layout.addWidget(self.action_on_true_list)

        msg_txt_bot = TextField(self.controller.get_false_message())
        msg_txt_bot.editing_done.connect(self.controller.set_false_message)
        layout.addWidget(QLabel("Message", font=font))
        layout.addWidget(msg_txt_bot)

        self.action_on_false_list = ActionList(controller=self.controller, type=False)
        self.action_on_false_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(QLabel("Action on false", font=font))
        layout.addWidget(self.action_on_false_list)

        self.refresh_list()
        name_txt_box.editing_done.connect(self.refresh_list)
        
        self.sidebar.main_controller.item_deletion.connect(self.refresh_list)
        self.sidebar.main_controller.item_addition.connect(self.refresh_list)

    def refresh_list(self):
        flags = self.sidebar.main_controller.get_flags()
        self.action_on_false_list.fill_combo_box(flags)
        self.action_on_false_list.fill_list_items()
        self.action_on_true_list.fill_combo_box(flags)
        self.action_on_true_list.fill_list_items()

    def pass_to_activated(self, value):
        self.controller.set_activated(bool(value))

    def disconnect_all_signals(self):
        self.sidebar.main_controller.item_deletion.disconnect(self.refresh_list)
        self.sidebar.main_controller.item_addition.disconnect(self.refresh_list)