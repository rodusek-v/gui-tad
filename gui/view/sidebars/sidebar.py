from types import FunctionType
from PyQt6.QtCore import QObject, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from view.buttons import ToggleButton
from view.sidebars.place_form import PlaceForm
from view.sidebars.object_form import ObjectForm
from view.sidebars.flag_form import FlagForm
from view.sidebars.command_form import CommandForm
from view.sidebars.player_form import PlayerForm
from view.sidebars.finish_form import FinishForm
from controller import WorldController
from model import Place, Object, Flag, Command, Player, Finish


class SideBar(QObject):

    def __init__(
        self,
        main_controller: WorldController,
        parent = None,
        hiding_func: FunctionType = None,
        side_bar_width: int = 300
    ) -> None:
        super().__init__()    
        self._holder = QWidget(parent=parent)
        self.widget = None
        self.main_controller = main_controller
        self.side_bar_width = side_bar_width

        self._holder.setLayout(QVBoxLayout())
        self._holder.layout().setContentsMargins(0, 0, 0, 0)
        self._holder.setStyleSheet("background-color: #262626;")
        self._holder.resize(0, 0)

        self.hide_btn = ToggleButton("")
        self.hide_btn.setFixedHeight(30)
        self.hide_btn.setCheckable(False)
        self.hide_btn.setIcon(QIcon("icons/hide.png"))
        self.hide_btn.setIconSize(QSize(40, 40))
        self.hide_btn.clicked.connect(lambda: hiding_func())
        self.hide_btn.setFixedWidth(60)
        self._holder.layout().addWidget(self.hide_btn)
        
    @property
    def holder(self):
        return self._holder

    def width(self):
        return self.holder.width()

    def setGeometry(self, x: int, y: int, width: int, height: int):
        self.holder.setGeometry(x, y, width, height)

    def set_form(self, model):
        self.hide_btn.show()
        form = None
        if isinstance(model, Place):
            form = PlaceForm(model, self)
        elif isinstance(model, Object):
            form = ObjectForm(model, self)
        elif isinstance(model, Flag):
            form = FlagForm(model, self)
        elif isinstance(model, Command):
            form = CommandForm(model, self)
        elif isinstance(model, Player):
            form = PlayerForm(model, self)
        elif isinstance(model, Finish):
            form = FinishForm(model, self)

        if form is not None:
            if self.widget is not None:
                if self.widget.model != model:
                    self.holder.layout().removeWidget(self.widget)
                    self.widget.disconnect_all_signals()
                    self.widget = form
                    self.holder.layout().addWidget(self.widget)
                    self.holder.update()
            else:
                self.widget = form
                self.holder.layout().addWidget(form)

    def remove_form(self):
        if self.widget is not None:
            self.holder.layout().removeWidget(self.widget)
        self.widget = None
        self.hide_btn.hide()

    def is_model_current(self, model):
        return self.widget.model == model if self.widget is not None else False
    