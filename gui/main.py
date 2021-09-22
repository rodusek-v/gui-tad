import sys
from PyQt6.QtGui import QFont
from view.windows import MainWindow, StartingDialog

from PyQt6.QtWidgets import QApplication

from config_loader import Config


if __name__ == '__main__':
    config = Config()

    app = QApplication(sys.argv)
    font = QFont("Futura", 10)
    QApplication.setFont(font)
    
    current_exit_code = 0
    if config.get_last_loaded() is None:
        starting = StartingDialog()
        starting.exec()
        if starting.closed():
            current_exit_code = -1

    if current_exit_code != -1:
        current_exit_code = MainWindow.EXIT_CODE_REBOOT
    while current_exit_code == MainWindow.EXIT_CODE_REBOOT:
        main_window = MainWindow()
        main_window.show()
        current_exit_code = app.exec()
        main_window.deleteLater()