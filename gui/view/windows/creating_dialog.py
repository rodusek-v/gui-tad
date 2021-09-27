from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QFileDialog, QGridLayout, QLabel, QSizePolicy

from view.buttons import ToggleButton
from view.fields import TextField
from config_loader import Config
from model import World


class CreatingDialog(QDialog):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setFixedSize(600, 200)
        self.setWindowTitle('GUI TAD')
        self.setWindowIcon(QIcon('icons/logo.png'))
        self.logo = QIcon()
        self.logo.addFile('icons/map.png', mode=QIcon.Mode.Active)
        self.logo.addFile('icons/map.png', mode=QIcon.Mode.Selected)
        self.logo.addFile('icons/map.png', mode=QIcon.Mode.Disabled)
        
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

            QDialog QLineEdit {
                background: transparent;
                color: #bfbfbf;
            }
        """)

        font = self.font()
        font.setPointSize(35)

        pic = ToggleButton()
        pic.setEnabled(False)
        pic.setIcon(self.logo)
        pic.setIconSize(QSize(120, 120))
        pic.setFixedSize(120, 120)
        
        layout.addWidget(pic, 0, 0, 3, 1, Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(12)
        layout.addWidget(QLabel("World name:", font=font), 0, 1, 1, 2)
        
        self.name_txt = TextField()
        self.name_txt.textChanged.connect(self.enable_button)
        layout.addWidget(self.name_txt, 0, 3, 1, 3)

        self.folder_select = ToggleButton("Select folder")
        self.folder_select.setStyle("color", "#bfbfbf")
        self.folder_select.setStyle("background", "#121212")
        self.folder_select.setCheckable(False)
        self.folder_select.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.folder_select.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_select, 1, 1, 1, 2)

        self.folder_name = TextField()
        self.folder_name.textChanged.connect(self.enable_button)
        layout.addWidget(self.folder_name, 1, 3, 1, 3)

        self.create_button = ToggleButton("Create")
        self.create_button.setStyle("color", "#bfbfbf")
        self.create_button.setStyle("background", "#121212")
        self.create_button.setCheckable(False)
        self.enable_button()
        self.create_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.create_button.clicked.connect(self.create_world)
        layout.addWidget(self.create_button, 2, 5)

    def enable_button(self):
        name = self.name_txt.text()
        folder = self.folder_name.text()

        if name == "" or folder == "":
            self.create_button.setEnabled(False)
            self.create_button.setStyle("background", "#d1d1d1")
        else:
            self.create_button.setEnabled(True)
            self.create_button.setStyle("background", "#121212")

    def select_folder(self):
        fname = QFileDialog.getExistingDirectory(self, "Select folder")
        self.folder_name.setText(fname)

    def create_world(self):
        name = self.name_txt.text()
        folder = self.folder_name.text()
        path = "/".join([folder, f"{name}.wld"])
        self.config.set_last_loaded(path)
        world = World()
        world.name = name
        with open(path, "w") as file:
            lines = world.text_model().split("\n")
            new_text = "\n".join([line for line in lines if line.strip() != ""])
            file.write(new_text)
        self.accept()