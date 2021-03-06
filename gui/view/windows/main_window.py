from PyQt6.QtWidgets import QApplication, QButtonGroup, QHBoxLayout, QLabel, QStatusBar, QWidget
from PyQt6.QtCore import QPoint, QPropertyAnimation, QRect, QSize, Qt
from PyQt6.QtGui import QIcon, QResizeEvent, QStandardItemModel
from PyQt6.QtWidgets import QDockWidget, QMainWindow, QMenu, QMenuBar

from view.windows.operation_dialog import OperationDialog, MaskWidget
from view.windows.message_box import MessageBox
from view.buttons import ToggleButton
from view.worktop import WorktopView, ActionSelector
from view.worldtree import WorldTreeView
from view.sidebars import SideBar
from view.menus import FileMenu
from controller import WorldController
from model import Flag, Command
from constants import THIS_FOLDER


class MainWindow(QMainWindow):
    
    EXIT_CODE_REBOOT = -123456789

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('GUI TAD')
        self.setWindowIcon(QIcon('icons/logo.png'))
        screen = QApplication.primaryScreen().size()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))

        self.action_selector = ActionSelector()
        self.controller = WorldController()
        self.controller.load()

        self.__init_tree_view()
        self.__init_working_space()
        self.__init_top_side()

        style = """
            QMenuBar {
                background-color: #262626;
                color: #bfbfbf;
            }
            QMenuBar::item::selected {
                background-color: #3d3d3d;
            }
            QMenu {
                background-color: #262626;
                color: #bfbfbf;
            }
            QMenu::item::selected {
                background-color: #3d3d3d;
            }
            QStatusBar {
                background-color: #3d3d3d;
            }
            QMainWindow {
                background-color: #262626;
            }
            QDockWidget {
                background-color: transparent; 
                color: #bfbfbf;
            }
            QToolBar::separator {
                background-color: #262626;
                width: 2px;
            }
        """
        self.setStyleSheet(style)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.location_label = QLabel()
        self.location_label.setStyleSheet("color: #bfbfbf")
        self.set_status_location(QPoint(0, 0))

        self.selected_place = QLabel()
        self.selected_place.setStyleSheet("color: #bfbfbf")

        self.status_bar.addPermanentWidget(self.selected_place)
        self.status_bar.addPermanentWidget(self.location_label)

        self.side_bar_width = 300
        self.side_bar = SideBar(self.controller, self, self.hide_form, self.side_bar_width)
        self.showed = False
        self.__connect_signals()

    def __animate(self):
        current_width = self.side_bar.width()
        if self.showed:
            width = 0
            self.showed = False
        else:
            width = self.side_bar_width
            self.showed = True
        self.animation = QPropertyAnimation(self.side_bar.holder, b'geometry')
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(self.width() - current_width, 0, current_width, self.height()))
        self.animation.setEndValue(QRect(self.width() - width, 0, width, self.height()))
        self.animation.start()
        self.animation.finished.connect(self.update)

    def __init_tree_view(self):
        self.side_dock = QDockWidget()
        self.side_dock.setFixedWidth(int(self.size().width() * 0.23))
        self.side_dock.setWindowTitle("Explorer")
        font = self.side_dock.font()
        font.setPointSize(13)
        self.side_dock.setFont(font)
        self.side_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.side_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.side_dock)

        self.tree_view = WorldTreeView()
        self.tree_view.setHeaderHidden(True)
        font.setPointSize(12)
        self.tree_view.setFont(font)
        self.side_dock.setWidget(self.tree_view)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        
        rootNode.appendRow(self.controller.model)

        self.tree_view.setModel(treeModel)
        self.tree_view.expandAll()

    def __init_working_space(self):
        temp = QWidget()
        temp.setStyleSheet("background-color: #575757;")
        
        self.working_space = WorktopView(self.controller, self.action_selector, side=120)
        self.working_space.setMinimumWidth(int(self.size().width() * 0.77))
        temp.setLayout(QHBoxLayout())
        temp.layout().addWidget(self.working_space)
        temp.layout().setContentsMargins(10, 10, 10, 10)

        self.setCentralWidget(temp)

    def __connect_signals(self):
        self.working_space.viewport_change.connect(self.set_status_location)
        self.working_space.selection_change.connect(self.set_selected_text)
        self.working_space.dispatch_event.connect(self.show_form)
        self.working_space.item_remove_start.connect(self.tree_view.deactivate_selection)
        self.working_space.item_remove_end.connect(self.tree_view.activate_selection)
        
        self.tree_view.selected_place.connect(lambda x: self.working_space.selecting_place(x.rect.center()))
        self.tree_view.selected_object.connect(lambda x: self.working_space.selecting_object(x))
        self.tree_view.remove_place_signal.connect(self.working_space.delete_selected)
        self.tree_view.remove_container_object_signal.connect(self.working_space.delete_object)
        self.tree_view.remove_object_signal.connect(self.controller.remove_object)
        self.tree_view.remove_flag_signal.connect(self.controller.remove_flag)
        self.tree_view.remove_command_signal.connect(self.controller.remove_cmd)
        self.tree_view.selected_item.connect(self.show_form)

        self.working_space.selection_change.connect(
            lambda x: self.tree_view.setCurrentIndex(x.index()) if x else self.tree_view.clearSelection()
        )
        
        self.working_space.deselect.connect(self.hide_form)
        self.working_space.deselect.connect(self.tree_view.clearSelection)
        self.tree_view.deselect.connect(self.hide_form)
        self.tree_view.deselect.connect(self.working_space.clear_selection)
        self.tree_view.no_container_object.connect(self.working_space.clear_selection)

        self.tree_view.add_object.triggered.connect(self.object_edit)
        self.tree_view.add_flag.triggered.connect(self.flag_edit)
        self.tree_view.add_command.triggered.connect(self.open_operation_dialog)

        self.controller.item_deletion.connect(self.hide_form)
        self.controller.not_allowed_delete.connect(self.open_message_box)

    def __init_top_side(self):
        menu_bar = QMenuBar()
        font = self.font()
        font.setPointSize(13)
        menu_bar.setFont(font)

        self.file_menu_item = FileMenu(self, self.controller)
        self.file_menu_item.new_object_item.triggered.connect(self.object_edit)
        self.file_menu_item.new_flag_item.triggered.connect(self.flag_edit)
        self.file_menu_item.new_command_item.triggered.connect(self.open_operation_dialog)

        help_menu_item = QMenu("&Help", self)

        menu_bar.addMenu(self.file_menu_item)
        menu_bar.addMenu(help_menu_item)
        self.setMenuBar(menu_bar)

        self.top_toolbar = self.addToolBar("World toolbar")
        self.top_toolbar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.top_toolbar.setMovable(False)
        self.top_toolbar.setFloatable(False)
        self.top_toolbar.setFixedHeight(60)
        self.top_toolbar.setStyleSheet("background-color: #3d3d3d; padding: 0px; border: none;")
        self.__set_up_toolbar()

    def __set_up_toolbar(self):
        generate = ToggleButton("", self)
        generate.setCheckable(False)
        generate.setIcon(QIcon("/".join([THIS_FOLDER, "icons/generate.png"])))
        generate.setIconSize(QSize(50, 50))
        self.top_toolbar.addWidget(generate)
        generate.clicked.connect(self.file_menu_item.save_func)

        grid = ToggleButton("", self)
        grid.setIcon(QIcon("/".join([THIS_FOLDER, "icons/grid.png"])))
        grid.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(grid)
        grid.clicked.connect(self.action_selector.toggle_grid)
        grid.clicked.connect(grid.select)

        self.top_toolbar.addSeparator()

        select = ToggleButton("", self)
        select.setIcon(QIcon("/".join([THIS_FOLDER, "icons/arrow.png"])))
        select.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(select)
        select.clicked.connect(lambda: self.action_selector.activate('select'))

        drag = ToggleButton("", self)
        self.top_toolbar.addWidget(drag)
        drag.setIcon(QIcon("/".join([THIS_FOLDER, "icons/filled_hand.png"])))
        drag.setIconSize(QSize(35, 35))
        drag.clicked.connect(lambda: self.action_selector.activate('drag'))

        add_place = ToggleButton("", self)
        add_place.setIcon(QIcon("/".join([THIS_FOLDER, "icons/box.png"])))
        add_place.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(add_place)
        add_place.clicked.connect(lambda: self.action_selector.activate('add_place'))

        add_object = ToggleButton("", self)
        add_object.setIcon(QIcon("/".join([THIS_FOLDER, "icons/object.png"])))
        add_object.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(add_object)
        add_object.clicked.connect(lambda: self.action_selector.activate('add_object'))

        self.top_toolbar.addSeparator()

        flag = ToggleButton("", self)
        flag.setCheckable(False)
        flag.setIcon(QIcon("/".join([THIS_FOLDER, "icons/flag.png"])))
        flag.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(flag)
        flag.clicked.connect(self.flag_edit)

        command = ToggleButton("", self)
        command.setCheckable(False)
        command.setIcon(QIcon("/".join([THIS_FOLDER, "icons/command.png"])))
        command.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(command)
        command.clicked.connect(self.open_operation_dialog)

        self.top_toolbar.addSeparator()

        player = ToggleButton("", self)
        player.setCheckable(False)
        player.setIcon(QIcon("/".join([THIS_FOLDER, "icons/player.png"])))
        player.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(player)
        player.clicked.connect(self.player_edit)

        finish = ToggleButton("", self)
        finish.setCheckable(False)
        finish.setIcon(QIcon("/".join([THIS_FOLDER, "icons/finish.png"])))
        finish.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(finish)
        finish.clicked.connect(self.finish_edit)
        
        grp = QButtonGroup(self)
        grp.addButton(select)
        grp.addButton(drag)
        grp.addButton(add_place)
        grp.addButton(add_object)
        grp.buttonClicked.connect(lambda btn: self.__toggle(grp.buttons(), btn))

        select.click()

    def open_operation_dialog(self):
        mask = MaskWidget(self)
        mask.show()
        dlg = OperationDialog(self)
        dlg.selected_operation.connect(self.command_edit)
        dlg.exec()
        dlg.selected_operation.disconnect(self.command_edit)
        mask.hide()

    def open_message_box(self, item):
        mask = MaskWidget(self)
        mask.show()
        dlg = MessageBox(self, item.name)
        dlg.exec()
        mask.hide()

    def flag_edit(self):
        self.working_space.clear_selection()
        self.tree_view.clearSelection()
        flag = self.controller.add_flag()
        self.show_form(flag)
        self.tree_view.setCurrentIndex(flag.index())

    def object_edit(self):
        self.working_space.clear_selection()
        self.tree_view.clearSelection()
        object = self.controller.add_object()
        self.show_form(object)
        self.tree_view.setCurrentIndex(object.index())

    def command_edit(self, type):
        self.working_space.clear_selection()
        self.tree_view.clearSelection()
        cmd = self.controller.add_command(type)
        self.show_form(cmd)
        self.tree_view.setCurrentIndex(cmd.index())

    def player_edit(self):
        self.working_space.clear_selection()
        self.tree_view.clearSelection()
        player = self.controller.get_player()
        self.show_form(player)

    def finish_edit(self):
        self.working_space.clear_selection()
        self.tree_view.clearSelection()
        finish = self.controller.get_finish()
        self.show_form(finish)

    def set_status_location(self, point):
        self.location_label.setText(f"X: {point.x()} Y: {point.y()}")

    def set_selected_text(self, item):
        title = "" if item is None else item.name
        class_name = item.__class__.__name__
        self.selected_place.setText(title)
        if title != "":
            self.selected_place.setText(f"{class_name}: {title}")

    def show_form(self, model):
        self.side_bar.set_form(model)
        if isinstance(model, Flag) or isinstance(model, Command):
            self.working_space.clear_selection()

        if not self.showed:
            self.__animate()

    def hide_form(self, deleted_model=None):
        if deleted_model is not None:
            if self.side_bar.is_model_current(deleted_model):
                self.side_bar.remove_form()
                if self.showed:
                    self.__animate()
        else:
            if self.showed:
                self.__animate()

    def generating_func(self):
        try:
            self.controller.generate()
            mask = MaskWidget(self)
            mask.show()
            dlg = MessageBox(self, "")
            dlg.setIcon(MessageBox.Icon.Information)
            dlg.setText("World model is successfully generated.")
            dlg.exec()
            mask.hide()
        except Exception as ex:
            mask = MaskWidget(self)
            mask.show()
            dlg = MessageBox(self, "")
            ex_msg = str(ex)
            error_msg = f"Not a valid project.\n{ex_msg}" 
            dlg.setText(error_msg)
            dlg.exec()
            mask.hide()

    def resizeEvent(self, event: QResizeEvent) -> None:
        current_width = self.side_bar.width()
        self.side_bar.setGeometry(event.size().width() - current_width, 0, current_width, event.size().height())
        return super().resizeEvent(event)

    @staticmethod
    def __toggle(buttons, to_toggle):
        for btn in buttons:
            btn.setChecked(False)
            btn.setStyle("background", "transparent")

        to_toggle.setChecked(True)
        to_toggle.setStyle("background", "#5e5eff")
