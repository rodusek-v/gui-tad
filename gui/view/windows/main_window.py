from view.canvas.grid_scroll import GridScroll
from view.canvas.grid_widget import Grid
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QScrollArea, QSizePolicy, QTableView, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDockWidget, QMainWindow, QMenu, QMenuBar

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('GUI TAD')
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.resize(1200, 700)
        self.__init_top_side()

        self.side_dock = QDockWidget()
        self.side_dock.setFixedWidth(300)
        self.side_dock.setWindowTitle("Explorer")
        self.side_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.side_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.side_dock)
        self.__init_working_space()

    def __init_working_space(self):
        temp = QWidget()
        temp.setStyleSheet("background-color: #c9c5c5;")
        
        self.working_space = Grid()
        temp.setLayout(QHBoxLayout())
        temp.layout().addWidget(self.working_space)
        temp.layout().setContentsMargins(0, 0, 0, 0)

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
        self.top_toolbar.setMovable(True)
        self.top_toolbar.setFloatable(False)
