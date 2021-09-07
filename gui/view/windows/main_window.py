from PyQt6.QtWidgets import QApplication, QButtonGroup, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QStatusBar, QWidget
from PyQt6.QtCore import QEvent, QObject, QPoint, QSize, Qt
from PyQt6.QtGui import QEnterEvent, QIcon
from PyQt6.QtWidgets import QDockWidget, QMainWindow, QMenu, QMenuBar

from view.worktop import WorktopView, ActionSelector


class ToggleButton(QPushButton):
    def __init__(self, text: str = None, parent: QObject = None):
        super().__init__(text, parent)
        self.styles = {
            "border": "none",
            "padding": "10px",
            "margin": "0px",
            "background": "transparent"
        }
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(self.__get_style())
        self.setCheckable(True)

    def __get_style(self):
        return " ".join([f"{key}: {value};" for key, value in self.styles.items()])

    def select(self):
        if self.isChecked():
            self.styles["background"] = "#393f4f"
        else:
            self.styles["background"] = "transparent"
        self.setStyleSheet(self.__get_style())

    def enterEvent(self, event: QEnterEvent) -> None:
        if not self.isChecked():
            self.styles["background"] = "#363636"
            self.setStyleSheet(self.__get_style())
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        if not self.isChecked():
            self.styles["background"] = "transparent"
            self.setStyleSheet(self.__get_style())
        return super().leaveEvent(event)

    def setStyle(self, key, value):
        self.styles[key] = value
        self.setStyleSheet(self.__get_style())
        self.repaint()


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('GUI TAD')
        self.setWindowIcon(QIcon('icons/icon.png'))
        screen = QApplication.primaryScreen().size()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))

        self.action_selector = ActionSelector()

        self.side_dock = QDockWidget()
        self.side_dock.setFixedWidth(int(self.size().width() * 0.23))
        self.side_dock.setWindowTitle("Explorer")
        self.side_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.side_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.side_dock)
        self.__init_working_space()
        self.__init_top_side()

        
        style = """
            QMenuBar {
                background-color: #262626;
                color: #bfbfbf;
            }
            QMenuBar::item::selected {
                background-color: #363636;
            }
            QMenu {
                background-color: #262626;
                color: #bfbfbf;
            }
            QMenu::item::selected {
                background-color: #363636;
            }
            QStatusBar {
                background-color: #262626;
            }
        """
        self.setStyleSheet(style)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.location_label = QLabel()
        self.location_label.setStyleSheet("color: #bfbfbf")
        self.set_status_location(QPoint(0, 0))
        self.status_bar.addPermanentWidget(self.location_label)

    def __init_working_space(self):
        temp = QWidget()
        temp.setStyleSheet("background-color: #c9c5c5;")
        
        self.working_space = WorktopView(self.action_selector)
        self.working_space.setMinimumWidth(int(self.size().width() * 0.77))
        temp.setLayout(QHBoxLayout())
        temp.layout().addWidget(self.working_space)
        temp.layout().setContentsMargins(10, 10, 10, 10)
        self.working_space.viewport_change.connect(self.set_status_location)

        self.setCentralWidget(temp)

    def __init_top_side(self):
        menu_bar = QMenuBar()

        file_menu_item = QMenu("&File", self)
        
        settings_menu_item = QMenu("&Settings", self)

        help_menu_item = QMenu("&Help", self)

        menu_bar.addMenu(file_menu_item)
        menu_bar.addMenu(settings_menu_item)
        menu_bar.addMenu(help_menu_item)
        self.setMenuBar(menu_bar)

        self.top_toolbar = self.addToolBar("")
        self.top_toolbar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.top_toolbar.setMovable(False)
        self.top_toolbar.setFloatable(False)
        self.top_toolbar.setFixedHeight(60)
        self.top_toolbar.setStyleSheet("background-color: #262626; padding: 0px; border: none;")
        self.__set_up_toolbar()

    def __set_up_toolbar(self):
        grid = ToggleButton("", self)
        grid.setIcon(QIcon("icons/grid.png"))
        grid.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(grid)
        grid.clicked.connect(self.action_selector.toggle_grid)
        grid.clicked.connect(grid.select)

        self.top_toolbar.addSeparator()

        select = ToggleButton("", self)
        select.setIcon(QIcon("icons/arrow.png"))
        select.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(select)
        select.clicked.connect(lambda: self.action_selector.activate('select'))
        add = ToggleButton("", self)
        add.setIcon(QIcon("icons/box.png"))
        add.setIconSize(QSize(35, 35))
        self.top_toolbar.addWidget(add)
        add.clicked.connect(lambda: self.action_selector.activate('add'))
        drag = ToggleButton("", self)
        self.top_toolbar.addWidget(drag)
        drag.setIcon(QIcon("icons/filled_hand.png"))
        drag.setIconSize(QSize(35, 35))
        drag.clicked.connect(lambda: self.action_selector.activate('drag'))

        grp = QButtonGroup(self)
        grp.addButton(select)
        grp.addButton(add)
        grp.addButton(drag)
        grp.buttonClicked.connect(lambda btn: self.__toggle(grp.buttons(), btn))

        select.click()

    def set_status_location(self, point):
        self.location_label.setText(f"X: {point.x()} Y: {point.y()}")

    @staticmethod
    def __toggle(buttons, to_toggle):
        for btn in buttons:
            btn.setChecked(False)
            btn.setStyle("background", "transparent")

        to_toggle.setChecked(True)
        to_toggle.setStyle("background", "#393f4f")
