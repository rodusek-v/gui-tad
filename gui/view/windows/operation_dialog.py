from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QButtonGroup, QDialog, QLabel, QPushButton, QRadioButton, QVBoxLayout, QWidget

from view.buttons.toggle_button import ToggleButton
from model.operation import OperationType


class MaskWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("background: rgba(0, 0, 0, 102);")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def show(self):
        if self.parent() is None:
            return

        parent_rect = self.parent().geometry()
        self.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
        super().show()


class OperationDialog(QDialog):

    selected_operation = pyqtSignal(OperationType)

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.resize(350, 100)
        self.setFont(self.parent().font())
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("""
            QDialog {
                background: #262626;
            }
            QDialog QLabel, QRadioButton {
                color: #bfbfbf;
            }
        """)

        self.layout = QVBoxLayout()
        cancel_btn = QPushButton("")
        cancel_btn.setFixedSize(20, 20)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                image: url(icons/close.png)
            }
            :hover {
                image: url(icons/close_hover.png)
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        message = QLabel("Select operation type:")
        message.setFixedHeight(20)
        font = message.font()
        font.setPointSize(13)
        message.setFont(font)

        font.setPointSize(11)
        button_group = QButtonGroup()
        self.message_operation_btn = QRadioButton("Message operation", font=font)
        self.flag_operation_btn = QRadioButton("Flag operation", font=font)
        self.cdm_operation_btn = QRadioButton("CDM operation", font=font)
        self.relocation_operation_btn = QRadioButton("Relocation operation", font=font)
        button_group.addButton(self.message_operation_btn)
        button_group.addButton(self.flag_operation_btn)
        button_group.addButton(self.cdm_operation_btn)
        button_group.addButton(self.relocation_operation_btn)
        self.message_operation_btn.setChecked(True)

        self.ok_button = ToggleButton("OK")
        self.ok_button.setStyle("color", "#bfbfbf")
        self.ok_button.setFixedWidth(60)
        self.ok_button.setCheckable(False)
        self.ok_button.clicked.connect(self.accept)

        self.layout.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(message, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.message_operation_btn)
        self.layout.addWidget(self.flag_operation_btn)
        self.layout.addWidget(self.cdm_operation_btn)
        self.layout.addWidget(self.relocation_operation_btn)
        self.layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
    
    def accept(self) -> None:
        if self.relocation_operation_btn.isChecked():
            type = OperationType.RELOCATION_OPERATION
        elif self.flag_operation_btn.isChecked():
            type = OperationType.FLAG_OPERATION
        elif self.cdm_operation_btn.isChecked():
            type = OperationType.CDM_OPERATION
        else:
            type = OperationType.MESSAGE_OPERATION
        self.selected_operation.emit(type)
        super().accept()