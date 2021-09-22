from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent, QIcon, QMouseEvent
from PyQt6.QtWidgets import QDialog, QFileDialog, QGridLayout, \
    QHBoxLayout, QLabel, QSizePolicy, QWidget

from view.buttons import ToggleButton
from view.fields import BasicList
from view.windows.creating_dialog import CreatingDialog
from view.windows.message_box import MessageBox
from config_loader import Config
from controller import WorldController


class StartingDialog(QDialog):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setFixedSize(400, 400)
        self.setWindowTitle('GUI TAD')
        self.logo = QIcon()
        self.logo.addFile('icons/logo.png', mode=QIcon.Mode.Active)
        self.logo.addFile('icons/logo.png', mode=QIcon.Mode.Selected)
        self.logo.addFile('icons/logo.png', mode=QIcon.Mode.Disabled)
        self.setWindowIcon(self.logo)
        
        self._closed = False
        self.config = Config()
        layout = QGridLayout()
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background: #262626;
            }
            QDialog QLabel, QRadioButton {
                color: #bfbfbf;
            }
        """)

        font = self.font()
        font.setPointSize(35)

        holder = QWidget()
        holder.setLayout(QHBoxLayout())
        layout.addWidget(holder, 0, 0, 1, 5, Qt.AlignmentFlag.AlignCenter)

        pic = ToggleButton()
        pic.setEnabled(False)
        pic.setIcon(self.logo)
        pic.setIconSize(QSize(120, 120))
        pic.setFixedSize(120, 120)
        holder.layout().addWidget(pic)
        
        title = QLabel("GUI TAD", font=font)
        title.setContentsMargins(30, 0, 0, 0)
        holder.layout().addWidget(title)
        
        self.recent_list = RecentList()
        self.recent_list.double_clicked.connect(self.open_main)
        self.recent_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.recent_list.addItems(self.config.get_recent())
        layout.addWidget(self.recent_list, 2, 0, 3, 3)

        self.load_button = ToggleButton("Open other")
        self.load_button.setStyle("color", "#bfbfbf")
        self.load_button.setStyle("background", "#121212")
        self.load_button.setCheckable(False)
        self.load_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.load_button.clicked.connect(self.open_other)
        layout.addWidget(self.load_button, 2, 3, 1, 2)

        self.create_button = ToggleButton("Create new")
        self.create_button.setStyle("color", "#bfbfbf")
        self.create_button.setStyle("background", "#121212")
        self.create_button.setCheckable(False)
        self.create_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.create_button.clicked.connect(self.create_new)
        layout.addWidget(self.create_button, 4, 3, 1, 2)

    def open_other(self):
        fname = QFileDialog.getOpenFileName(self, "Open project", filter="World files (*.wd)")
        if fname[0] != "":
            self.open_main(fname[0])

    def create_new(self):
        dlg = CreatingDialog(self)
        dlg.accepted.connect(self.accept)
        dlg.exec()

    def open_main(self, fname):
        old = self.config.get_last_loaded()
        self.config.set_last_loaded(fname)
        controller = WorldController()
        try:
            controller.load()
            self.accept()
        except:
            msg_box = MessageBox(self, "")
            msg_box.setText("Bad file format")
            msg_box.exec()
            self.config.remove_recent(fname)
            self.config.set_last_loaded(old)
            self.recent_list.clear()
            self.recent_list.addItems(self.config.get_recent())
            
    def closed(self) -> bool:
        return self._closed

    def closeEvent(self, event: QCloseEvent) -> None:
        self._closed = True
        super().closeEvent(event)


class RecentList(BasicList):

    double_clicked = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        style = self.list_style.format("2px solid #545454", "2px solid #545454")
        style = style.replace("padding: 0px;", "padding: 5px;")
        self.setStyleSheet(style)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
    
    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        self.double_clicked.emit(self.currentItem().text())
        super().mouseDoubleClickEvent(e)