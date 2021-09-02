from view.worktop import WorktopView
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QDockWidget, QMainWindow, QMenu, QMenuBar

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('GUI TAD')
        self.setWindowIcon(QIcon('icons/icon.png'))
        screen = QApplication.primaryScreen().size()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))

        self.side_dock = QDockWidget()
        self.side_dock.setFixedWidth(int(self.size().width() * 0.23))
        self.side_dock.setWindowTitle("Explorer")
        self.side_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.side_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.side_dock)
        self.__init_working_space()
        self.__init_top_side()

    def __init_working_space(self):
        temp = QWidget()
        temp.setStyleSheet("background-color: #c9c5c5;")
        
        self.working_space = WorktopView()
        self.working_space.setMinimumWidth(int(self.size().width() * 0.77))
        temp.setLayout(QHBoxLayout())
        temp.layout().addWidget(self.working_space)
        temp.layout().setContentsMargins(10, 10, 10, 10)

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
        a = QAction("Toggle", self)
        self.top_toolbar.addAction(a)
        a.triggered.connect(self.__toggle_toolbar)
        a = QAction("Add", self)
        self.top_toolbar.addAction(a)
        a.triggered.connect(self.working_space.toggle_addition)

    def __toggle_toolbar(self):
        if self.top_toolbar.height() == 100:
            self.top_toolbar.setFixedHeight(20)
        else:
            self.top_toolbar.setFixedHeight(100)
